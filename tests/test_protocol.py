"""LAN regressions against independently captured official app packets."""
import asyncio
import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'custom_components' / 'jebao_studio'))
from gizwits_lan.device import Device
from gizwits_lan.device_manager import DeviceManager
from gizwits_lan.errors import ProtocolError
from gizwits_lan.protocol import build_prefix_and_command


def make_device():
    model = json.loads((ROOT / 'custom_components/jebao_studio/models/54114ccdac1e41c0bb17e222887c07ba.json').read_text())
    return Device('192.0.2.1', attributes=model['entities'][0]['attrs'])


class ProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_power_writes_match_official_app_capture_prefix(self):
        for value, name in ((False, 'false'), (True, 'true')):
            with self.subTest(value=value):
                device = make_device()
                device._connected = True
                sent = []
                async def send(cmd, response, seq, payload, timeout):
                    sent.append(payload[4:])
                    return b'\x00'
                device._send_command_with_seq = send
                await device.set_device_attribute('SwitchON', value)
                capture = (ROOT / f'tests/fixtures/switchon_{name}.bin').read_bytes()[13:]
                self.assertEqual(sent[0], capture)

    async def test_flow_write_uses_the_compact_live_control_block(self):
        """MLW ignores numeric controls when the 400-byte timer block is sent."""
        device = make_device(); device._connected = True
        sent = []
        async def send(cmd, response, seq, payload, timeout):
            sent.append(payload[4:])
            return b'\x00'
        device._send_command_with_seq = send
        await device.set_multiple_attributes({'Flow': 73})
        # action + eight datapoint flags + ten live-control bytes.
        self.assertEqual(len(sent[0]), 19)
        self.assertEqual(sent[0][0], 1)
        self.assertEqual(sent[0][1:9], b'\x00\x00\x00\x00\x00\x00\x01\x00')
        self.assertEqual(sent[0][11], 73)

    async def test_concurrent_writes_have_distinct_sequences(self):
        device = make_device(); device._connected = True
        sequences = []
        async def send(cmd, response, seq, payload, timeout):
            sequences.append(seq)
            await asyncio.sleep(0)
            return b'\x00'
        device._send_command_with_seq = send
        await asyncio.gather(*(device.set_multiple_attributes({'Flow': value}) for value in (30, 40, 50)))
        self.assertEqual(len(set(sequences)), 3)

    async def test_write_ack_applies_the_controller_status_to_entities(self):
        device = make_device(); device._connected = True
        updates = []
        device.add_status_callback(lambda status: updates.append(status.data.copy()))
        status_bytes = bytearray(device.max_status_len)
        # Flow is byte 2 in this MLW profile. The acknowledgement includes
        # an action byte before the resulting status data.
        status_bytes[2] = 73
        async def send(cmd, response, seq, payload, timeout):
            return b'\x00' + bytes(status_bytes)
        device._send_command_with_seq = send
        await device.set_device_attribute('Flow', 73)
        self.assertEqual(device.get_attribute('Flow'), 73)
        self.assertEqual(updates[-1]['Flow'], 73)

    async def test_disconnected_write_fails(self):
        with self.assertRaises(RuntimeError):
            await make_device().set_device_attribute('SwitchON', True)

    async def test_retries_numeric_write_until_full_ack_matches(self):
        device = make_device(); device._connected = True
        calls = []
        async def send(cmd, response, seq, payload, timeout):
            calls.append(seq)
            status = bytearray(device.max_status_len)
            status[2] = 73 if len(calls) == 2 else 40
            return b'\x00' + status
        async def readback(timeout=3):
            return False
        device._send_command_with_seq = send
        device.request_status_update = readback
        await device.set_device_attribute('Flow', 73)
        self.assertEqual(len(calls), 2)
        self.assertNotEqual(calls[0], calls[1])
        self.assertEqual(device.get_attribute('Flow'), 73)

    async def test_delayed_readback_prevents_duplicate_write(self):
        device = make_device(); device._connected = True
        calls = []
        async def send(*args):
            calls.append(args)
            return b'\x00'
        async def readback(timeout=3):
            status = bytearray(device.max_status_len); status[3] = 61
            device._apply_status_data(status)
            return True
        device._send_command_with_seq = send
        device.request_status_update = readback
        await device.set_device_attribute('Frequency', 61)
        self.assertEqual(len(calls), 1)

    async def test_program_mode_stops_manual_write_before_sending(self):
        device = make_device(); device._connected = True
        status = bytearray(device.max_status_len); status[1] = 8
        device._apply_status_data(status)
        with self.assertRaisesRegex(ProtocolError, 'Manual'):
            await device.set_device_attribute('Flow', 73)

    async def test_mode_preserves_neighbouring_power_and_linkage(self):
        device = make_device(); device._connected = True
        initial = bytearray(device.max_status_len)
        initial[:4] = bytes.fromhex('00814b3d')  # on, primary, flow 75, frequency 61
        device._apply_status_data(initial)
        sent = []
        async def send(cmd, response, seq, payload, timeout):
            sent.append(payload[4:])
            return b'\x00'
        device._send_command_with_seq = send
        for mode in range(4):
            await device.set_multiple_attributes({'Mode': mode})
            self.assertEqual(sent[-1][1:9], bytes.fromhex('0000000000000020'))
            self.assertEqual(sent[-1][9:13], bytes([0, 0x81 | (mode << 5), 75, 61]))

    async def test_actual_socket_ack_rejection_reaches_caller(self):
        device = make_device(); device._connected = True
        class Writer:
            def write(self, packet):
                self.packet = packet
            async def drain(self):
                seq = device._sequence.to_bytes(4, 'big')
                # Full controller status still says Flow=0, rejecting Flow=73.
                await device._handle_incoming_packet(b'\x00\x94', seq + b'\x00' + bytes(device.max_status_len))
        device.writer = Writer()
        async def no_readback(timeout=3):
            return False
        device.request_status_update = no_readback
        with self.assertRaisesRegex(ProtocolError, 'Flow'):
            await device.set_device_attribute('Flow', 73)
        self.assertTrue(device.writer.packet.startswith(b'\x00\x00\x00\x03'))
        self.assertEqual(device.get_attribute('Flow'), 0)

    async def test_product_key_cannot_escape_models_directory(self):
        manager = DeviceManager(ROOT / 'custom_components/jebao_studio/models')
        for key in ('../manifest', '', 'A' * 32):
            with self.assertRaises(FileNotFoundError):
                await manager._load_device_definition(key)

    async def test_tcp_fragmentation_and_coalescing(self):
        device = make_device()
        packet = build_prefix_and_command(b'\x00\x16', b'')
        buffer = bytearray(packet[:5])
        self.assertIsNone(device._try_extract_one_packet(buffer))
        buffer.extend(packet[5:] + packet)
        self.assertEqual(device._try_extract_one_packet(buffer), packet)
        self.assertEqual(device._try_extract_one_packet(buffer), packet)
        self.assertEqual(buffer, b'')

    async def test_oversized_packet_length_rejected(self):
        with self.assertRaises(ProtocolError):
            make_device()._try_extract_one_packet(bytearray(b'\x00\x00\x00\x03\xff\xff\xff\xff'))
