import {readFile} from 'node:fs/promises';
import {createContext, SourceTextModule} from 'node:vm';
import test from 'node:test';
import assert from 'node:assert/strict';

const base = new URL('../custom_components/jebao_studio/panel/', import.meta.url);
const source = await readFile(new URL('jebao-studio.js', base), 'utf8');
const model = await readFile(new URL('model.js', base), 'utf8');
// The pre-update URL is already in the browser's module cache.
const cachedModel = 'export const command=()=>{},offline=()=>{},labels={},groupDevices=()=>[];';

async function boot(panelSource = source) {
  const registry = new Map();
  const context = createContext({setTimeout: () => {}, Date, document: {createElement: tag => ({
    tag, children: [], style: {setProperty() {}}, setAttribute() {},
    append(...items) { this.children.push(...items); },
    checkValidity() { return this.value !== '' && Number(this.value) >= Number(this.min) && Number(this.value) <= Number(this.max); },
    get valueAsNumber() { return this.value === '' ? NaN : Number(this.value); },
    reportValidity() {},
  })}, HTMLElement: class {
    attachShadow() { this.shadowRoot = {}; }
  }, customElements: {get: key => registry.get(key), define: (key, value) => registry.set(key, value)}});
  const module = new SourceTextModule(panelSource, {context});
  await module.link(specifier => new SourceTextModule(
    specifier === './model.js' ? cachedModel : model, {context},
  ));
  await module.evaluate();
  const Panel = registry.get('jebao-studio-panel');
  Panel.prototype.render = function() {};
  return new Panel();
}

test('upgrade bypasses the cached pre-groups model which breaks module startup', async () => {
  const oldImport = source.replace(/from '\.\/model\.js\?[^']+'/, "from './model.js'");
  await assert.rejects(boot(oldImport), /does not provide an export named/);
  const panel = await boot();
  assert.equal(panel.devices.length, 0);
});

test('pump cards are ready while the groups request is still pending', async () => {
  const panel = await boot();
  const devices = [{id:'pump', kind:'wavemaker', entities:[]}];
  let release;
  const pending = new Promise(resolve => { release=resolve; });
  panel._hass = {callWS: async msg => msg.type.endsWith('/catalog') ? devices : pending};
  const loading = panel.load();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(panel.loading, false);
  assert.equal(panel.devices, devices);
  release([]);
  await loading;
});

test('groups API failure preserves pump cards and explains the problem', async () => {
  const panel = await boot();
  const devices = [{id:'pump', entities:[]}];
  panel._hass = {callWS: async msg => {
    if (msg.type.endsWith('/catalog')) return devices;
    throw new Error('unknown_command');
  }};
  await panel.load();
  assert.equal(panel.devices, devices);
  assert.equal(panel.loading, false);
  assert.match(panel.notice, /unknown_command/);
});

test('status renders preserve pointer edits and writes', async () => {
  const panel = await boot();
  let draws = 0;
  panel.render = () => { draws++; };
  panel.connectedCallback();
  panel._interacting = true;
  panel.render();
  panel._interacting = false;
  panel.busy = true;
  panel.render();
  assert.equal(draws, 0);
  panel.busy = false;
  panel.render();
  assert.equal(draws, 1);
});

test('numeric entry and slider stay synchronized and send once on commit', async () => {
  const panel = await boot();
  panel._hass = {states: {'number.flow': {state:'40', attributes:{min:0,max:100,step:1}}}};
  const sent = [];
  const control = panel.slider({entity_id:'number.flow'}, 'Intensität', async next => sent.push(next));
  const number = control.children[0].children[1].children[0];
  const range = control.children[1];
  number.value = '73'; number.oninput();
  assert.equal(range.value, '73');
  assert.equal(sent.length, 0);
  await number.onchange();
  await number.onblur();
  assert.deepEqual(sent, [73]);
  const redraw = panel.slider({entity_id:'number.flow'}, 'Intensität', () => {});
  assert.equal(Number(redraw.children[1].value), 73);
  number.value = '101';
  await number.onchange();
  assert.deepEqual(sent, [73]);
});
