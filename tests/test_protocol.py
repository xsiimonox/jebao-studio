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
                self.assertEqual(sent[0][:len(capture)], capture)

    async def test_concurrent_writes_have_distinct_sequences(self):
        device = make_device(); device._connected = True
        sequences = []
        async def send(cmd, response, seq, payload, timeout):
            sequences.append(seq)
            await asyncio.sleep(0)
            return b'\x00'
        device._send_command_with_seq = send
        await asyncio.gather(*(device.set_device_attribute('Flow', value) for value in (30, 40, 50)))
        self.assertEqual(len(set(sequences)), 3)

    async def test_disconnected_write_fails(self):
        with self.assertRaises(RuntimeError):
            await make_device().set_device_attribute('SwitchON', True)

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
