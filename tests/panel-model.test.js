import {test} from 'node:test';
import assert from 'node:assert/strict';
import {command, groupDevices, controlsForGroup, controllable, controlsForDevice} from '../custom_components/jebao_studio/panel/model.js';

test('native services receive validated values and entity targets', () => {
  assert.deepEqual(command('number.flow', 45, {state:'40',attributes:{min:30,max:100}}), ['number','set_value',{entity_id:'number.flow',value:45}]);
  assert.deepEqual(command('switch.pump', false, {state:'on',attributes:{}}), ['switch','turn_off',{entity_id:'switch.pump'}]);
  assert.deepEqual(command('select.mode', 'constant_flow', {state:'random_wave',attributes:{options:['constant_flow','random_wave']}}), ['select','select_option',{entity_id:'select.mode',option:'constant_flow'}]);
});
test('offline, non-finite, out-of-range and unsupported writes fail', () => {
  assert.throws(()=>command('number.flow', 45.5, {state:'40',attributes:{min:0,max:100,step:1}}));
  for (const value of [NaN, Infinity, 29, 101]) assert.throws(()=>command('number.flow',value,{state:'40',attributes:{min:30,max:100}}));
  assert.throws(()=>command('switch.pump',true,{state:'unavailable',attributes:{}}));
  assert.throws(()=>command('select.mode','invented',{state:'off',attributes:{options:['off']}}));
  assert.throws(()=>command('sensor.fault',false,{state:'off',attributes:{}}));
});

test('registry attributes identify renamed controls and never select FeedTime as flow', () => {
  const device={entities:[{entity_id:'number.dinner',attribute:'FeedTime'}, {entity_id:'number.renamed',attribute:'Flow'}, {entity_id:'switch.schedule',attribute:'TimerON'}, {entity_id:'select.bond',attribute:'Linkage'}]};
  const states=Object.fromEntries(device.entities.map(e=>[e.entity_id,{state:'40',attributes:{}}]));
  const result=controlsForDevice(device,states);
  assert.equal(result.intensity.entity_id,'number.renamed');
  assert.equal(result.feedTime.entity_id,'number.dinner');
  assert.equal(result.power,undefined);
  assert.equal(result.mode,undefined);
});
test('dosing and BLE diagnostics are separate from flow controls', () => {
  const devices=[{id:'a',kind:'wavemaker',transport:'local'},{id:'b',kind:'doser',transport:'local'},{id:'c',kind:'bluetooth',transport:'ble_probe'}];
  assert.deepEqual(groupDevices(devices,'flow').map(d=>d.id),['a']);
  assert.deepEqual(groupDevices(devices,'dosing').map(d=>d.id),['b']);
  assert.deepEqual(groupDevices(devices,'ble').map(d=>d.id),['c']);
});

test('group controls only expose reachable compatible pump controls', () => {
  const devices = [
    {id:'left',entities:[{entity_id:'switch.left_power',name:'Pumpe'},{entity_id:'number.left_flow',name:'Leistung'},{entity_id:'select.left_mode',name:'Modus'}]},
    {id:'right',entities:[{entity_id:'switch.right_power',name:'Pumpe'},{entity_id:'number.right_flow',name:'Leistung'}]},
    {id:'offline',entities:[{entity_id:'switch.offline_power',name:'Pumpe'}]},
  ];
  const states = {
    'switch.left_power':{state:'on',attributes:{}}, 'number.left_flow':{state:'45',attributes:{}}, 'select.left_mode':{state:'random_wave',attributes:{}},
    'switch.right_power':{state:'on',attributes:{}}, 'number.right_flow':{state:'50',attributes:{}},
    'switch.offline_power':{state:'unavailable',attributes:{}},
  };
  assert.equal(controllable(devices[0],states),true);
  assert.equal(controllable(devices[2],states),false);
  const controls=controlsForGroup(devices,states);
  assert.equal(controls.online.length,2);
  assert.equal(controls.power.entity_id,'switch.left_power');
  assert.equal(controls.flow.entity_id,'number.left_flow');
  assert.equal(controls.mode.entity_id,'select.left_mode');
});
