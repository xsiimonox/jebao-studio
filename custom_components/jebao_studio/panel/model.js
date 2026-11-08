export const offline = state => !state || ['unknown', 'unavailable'].includes(state.state);
export const labels = {
  wavemaker: 'Strömungspumpe', returnpump: 'Förderpumpe', doser: 'Dosierpumpe',
  bluetooth: 'Bluetooth-Diagnose', unknown: 'Controller', local: 'Lokales WLAN', cloud: 'Gizwits Cloud',
  constant_flow: 'Konstant', sine_wave: 'Sinuswelle', square_wave: 'Rechteckwelle',
  random_wave: 'Zufall', pulse_wave: 'Puls', feeding: 'Fütterung', off: 'Aus',
  independent: 'Unabhängig', primary: 'Master', secondary: 'Slave', auto: 'Automatisch', manual: 'Manuell',
  synchronous_secondary: 'Synchroner Slave', asynchronous_secondary: 'Asynchroner Slave',
  tide: 'Gezeiten', nutrient_transport: 'Nährstofftransport', circulation: 'Zirkulation', custom_wave: 'Eigene Welle',
};
export function command(entityId, value, state) {
  if (offline(state)) throw new Error('Der Controller ist gerade nicht erreichbar.');
  const domain = entityId.split('.')[0];
  if (domain === 'switch' && typeof value === 'boolean')
    return [domain, value ? 'turn_on' : 'turn_off', {entity_id: entityId}];
  if (domain === 'select' && state.attributes.options?.includes(value))
    return [domain, 'select_option', {entity_id: entityId, option: value}];
  if (domain === 'number' && Number.isFinite(value) && value >= state.attributes.min && value <= state.attributes.max &&
      Math.abs((value-state.attributes.min)/(state.attributes.step||1)-Math.round((value-state.attributes.min)/(state.attributes.step||1)))<1e-8)
    return [domain, 'set_value', {entity_id: entityId, value}];
  throw new Error('Dieser Wert wird vom Controller nicht unterstützt.');
}
export function groupDevices(devices, tab) {
  return devices.filter(d => tab === 'ble' ? d.transport === 'ble_probe' :
    tab === 'dosing' ? d.kind === 'doser' : d.kind !== 'doser' && d.transport !== 'ble_probe');
}

export function controllable(device, states) {
  return device.entities.some(entity => !offline(states[entity.entity_id]) && ['number', 'switch', 'select'].includes(entity.entity_id.split('.')[0]));
}

// Registry metadata is stable even when users rename entities or translate HA.
export function controlsForDevice(device, states) {
  const active = device.entities.filter(e => !offline(states[e.entity_id]));
  const pick = (attribute, domain, pattern) => active.find(e => e.attribute === attribute) ||
    active.find(e => !e.attribute && e.entity_id.startsWith(domain + '.') && pattern.test(
      e.entity_id + ' ' + (e.name || '') + ' ' + (states[e.entity_id]?.attributes.friendly_name || '')));
  return {
    power: pick('SwitchON','switch',/switchon|power|pumpe|ein.?aus/i),
    feed: pick('FeedSwitch','switch',/feed|fütter/i),
    intensity: pick('Flow','number',/flow|leistung|intensit/i),
    frequency: pick('Frequency','number',/frequency|frequenz/i),
    feedTime: pick('FeedTime','number',/feedtime|fütter.*zeit/i),
    timer: pick('TimerON','switch',/timeron|zeitplan/i),
    linkage: pick('Linkage','select',/linkage|kopplung/i),
    mode: pick('Mode','select',/mode|modus/i),
  };
}

export function controlsForGroup(devices, states) {
  const online = devices.filter(device => controllable(device, states));
  const entities = online.flatMap(device => device.entities.map(entity => ({...entity, state:states[entity.entity_id], device}))).filter(item => item.state);
  const first = prefix => entities.find(item => item.entity_id.startsWith(prefix));
  return {
    online,
    power: entities.find(item => item.entity_id.startsWith('switch.') && !/feed|fütter/i.test(item.state.attributes.friendly_name || item.name)),
    feed: entities.find(item => item.entity_id.startsWith('switch.') && /feed|fütter/i.test(item.state.attributes.friendly_name || item.name)),
    flow: first('number.'),
    mode: first('select.'),
  };
}
