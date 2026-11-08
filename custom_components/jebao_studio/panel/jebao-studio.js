import {command, offline, labels, groupDevices} from './model.js';
const element = (tag, text, cls) => {
  const node = document.createElement(tag);
  if (text != null) node.textContent = text;
  if (cls) node.className = cls;
  return node;
};
class JebaoStudioPanel extends HTMLElement {
  constructor() {
    super(); this.attachShadow({mode:'open'}); this.devices = []; this.tab = 'flow';
    this.loading = true; this.error = ''; this.busy = false; this.loaded = false;
  }
  set hass(value) {
    this._hass = value;
    if (!this.loaded) { this.loaded = true; this.load(); }
    else if (!this.shadowRoot.activeElement?.matches('input,select')) this.render();
  }
  async load() {
    this.loading = true; this.error = ''; this.render();
    try { this.devices = await this._hass.callWS({type:'jebao_studio/catalog'}); }
    catch (err) { this.error = err.message || String(err); }
    finally { this.loading = false; this.render(); }
  }
  button(text, action, cls = '') {
    const b = element('button', text, cls); b.type = 'button'; b.disabled = this.busy;
    b.addEventListener('click', action); return b;
  }
  async change(id, value) {
    this.busy = true; this.error = ''; this.render();
    try { await this._hass.callService(...command(id, value, this._hass.states[id])); }
    catch (err) { this.error = err.message || String(err); }
    finally { this.busy = false; this.render(); }
  }
  async inspect(device) {
    this.busy = true; this.error = ''; this.render();
    try {
      const report = await this._hass.callWS({type:'jebao_studio/ble_inspect', entry_id:device.id});
      const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], {type:'application/json'}));
      const a = element('a'); a.href = url; a.download = 'jebao-bluetooth-diagnose.json';
      a.click(); setTimeout(() => URL.revokeObjectURL(url), 30000);
      this.notice = `${report.services.length} GATT-Dienste erfasst. Diagnose wurde heruntergeladen.`;
    } catch (err) { this.error = err.message || String(err); }
    finally { this.busy = false; this.render(); }
  }
  entityRow(entity) {
    const state = this._hass.states[entity.entity_id];
    const row = element('div', null, 'row'); const desc = element('div');
    desc.append(element('span', state?.attributes.friendly_name || entity.name, 'label'));
    const domain = entity.entity_id.split('.')[0];
    const unavailable = offline(state);
    const disabled = unavailable || this.busy;
    if (domain === 'number' && !unavailable) {
      const input = element('input'); input.type = 'number';
      input.min = state.attributes.min; input.max = state.attributes.max; input.step = state.attributes.step || 1;
      input.value = state.state; input.disabled = disabled;
      input.setAttribute('aria-label', state.attributes.friendly_name || entity.name);
      input.addEventListener('change', () => this.change(entity.entity_id, input.valueAsNumber));
      const wrap = element('div', null, 'numeric'); wrap.append(input, element('span', state.attributes.unit_of_measurement || ''));
      row.append(desc, wrap);
    } else if (domain === 'switch') {
      const b = this.button(unavailable ? 'Nicht erreichbar' : state.state === 'on' ? 'Ein' : 'Aus', () => this.change(entity.entity_id, state.state !== 'on'), state?.state === 'on' ? 'toggle on' : 'toggle');
      b.disabled = disabled; b.setAttribute('role', 'switch'); b.setAttribute('aria-checked', String(state?.state === 'on'));
      b.setAttribute('aria-label', state?.attributes.friendly_name || entity.name); row.append(desc, b);
    } else if (domain === 'select') {
      const select = element('select'); select.disabled = disabled;
      select.setAttribute('aria-label', state?.attributes.friendly_name || entity.name);
      for (const value of state?.attributes.options || []) { const option = element('option', labels[value] || value); option.value = value; option.selected = value === state.state; select.append(option); }
      if (unavailable || !(state?.attributes.options || []).includes(state.state)) {
        const option = element('option', '—'); option.selected = true; option.disabled = true; select.prepend(option);
      }
      select.addEventListener('change', () => this.change(entity.entity_id, select.value)); row.append(desc, select);
    } else {
      const value = unavailable ? '—' : domain === 'binary_sensor' ? (state.state === 'on' ? 'Aktiv' : 'OK') : `${state.state} ${state.attributes.unit_of_measurement || ''}`;
      const reading = element('span', value, domain === 'binary_sensor' && state?.state === 'on' ? 'fault' : 'reading');
      row.append(desc, reading);
    }
    return row;
  }
  deviceCard(device) {
    const card = element('article', null, 'card');
    const header = element('div', null, 'card-head'); header.append(element('h2', device.name));
    const entities = device.entities.map(e => this._hass.states[e.entity_id]).filter(Boolean);
    const available = entities.length ? entities.some(s => !offline(s)) : device.available;
    header.append(element('span', device.transport === 'ble_probe' ? 'Vorbereitet' : available ? 'Verbunden' : 'Offline', available ? 'badge live' : 'badge'));
    card.append(header, element('p', `${labels[device.kind] || device.kind} · ${labels[device.transport] || 'Bluetooth'}`, 'muted'));
    if (device.transport === 'ble_probe') {
      card.append(element('p', 'DMP-Steuerung noch nicht implementiert. Für den Treiber fehlen das bestätigte GATT-Protokoll und App-Mitschnitte.'));
      card.append(element('p', 'Jebao Aqua schließen. Diese Abfrage erfasst nur Dienste und Eigenschaften; sie sendet keine Pumpenbefehle.', 'muted'));
      card.append(this.button(this.busy ? 'Bitte warten …' : 'Bluetooth-Schnittstellen auslesen', () => this.inspect(device), 'primary'));
    } else {
      if (device.kind === 'doser') card.append(element('p', 'Dosierpumpen sind für die spätere Erweiterung vorbereitet. Manuelles Dosieren, Kalibrierung und Zeitplanänderungen sind noch nicht freigegeben.', 'note'));
      for (const entity of device.entities) card.append(this.entityRow(entity));
      if (!device.entities.length) card.append(element('p', 'Noch keine Entitäten verfügbar. Einrichtung und Produktprofil prüfen.', 'muted'));
      const detail = element('details'); detail.append(element('summary', 'Controller-Profil'), element('code', device.product_key)); card.append(detail);
    }
    return card;
  }
  render() {
    if (!this._hass) return;
    const root = this.shadowRoot; root.replaceChildren();
    const style = element('style'); style.textContent = `
      :host{display:block;min-height:100vh;background:var(--primary-background-color,#f4f7fa);color:var(--primary-text-color,#17324a);font-family:var(--paper-font-body1_-_font-family,system-ui);--accent:#087e8b}
      *{box-sizing:border-box}header{display:flex;align-items:center;gap:12px;padding:16px 24px;background:var(--card-background-color,#fff);border-bottom:1px solid var(--divider-color,#dde5ec)}header strong{font-size:18px;flex:1}ha-menu-button{display:block}main{max-width:1120px;padding:40px 24px 80px;margin:auto}.eyebrow{font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);font-weight:700}h1{font-size:clamp(30px,5vw,46px);letter-spacing:-.04em;margin:10px 0}h2{font-size:20px;margin:0}.intro{max-width:650px;line-height:1.6}.muted{color:var(--secondary-text-color,#677b8c);font-size:14px;line-height:1.6}nav{display:flex;gap:8px;margin:28px 0;flex-wrap:wrap}button,select,input{font:inherit;color:inherit;border:1px solid var(--divider-color,#d5dfe5);border-radius:10px;background:var(--card-background-color,#fff);padding:10px 14px}button{cursor:pointer}button:disabled,select:disabled,input:disabled{opacity:.5;cursor:default}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #20b5ba;outline-offset:3px}.selected,.primary{background:var(--accent);border-color:var(--accent);color:white}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:20px}.card{background:var(--card-background-color,#fff);padding:24px;border:1px solid var(--divider-color,#dde5ec);border-radius:20px;box-shadow:0 8px 24px #13364d05}.card-head{display:flex;align-items:center;justify-content:space-between;gap:12px}.badge{font-size:12px;white-space:nowrap;padding:6px 10px;border-radius:20px;background:var(--secondary-background-color,#edf2f5)}.live{background:#087e8b18;color:var(--accent)}.row{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:16px 0;border-bottom:1px solid var(--divider-color,#eaf0f4)}.label{font-size:14px}.numeric{display:flex;align-items:center;gap:8px}input{width:95px}select{max-width:55%}.toggle{min-width:75px}.toggle.on{background:var(--accent);color:white}.fault,.error{color:var(--error-color,#b5263b)}.error,.note,.notice{border-radius:12px;padding:16px;background:var(--secondary-background-color,#eaf2f5);line-height:1.6;margin-bottom:20px}details{margin-top:20px;color:var(--secondary-text-color,#677b8c);font-size:12px}summary{cursor:pointer;margin-bottom:10px}code{overflow-wrap:anywhere}.empty{padding:40px;text-align:center;border:1px dashed var(--divider-color,#beced8);border-radius:20px}a{color:var(--accent)}footer{margin-top:28px;font-size:12px;color:var(--secondary-text-color,#677b8c)}@media(max-width:600px){main{padding:24px 16px}.card{padding:18px}header{padding:12px 16px}.row{gap:10px}}
    `; root.append(style);
    const header = element('header'); const menu = element('ha-menu-button'); menu.hass = this._hass;
    header.append(menu, element('strong', 'Jebao Studio'), this.button('Aktualisieren', () => this.load())); root.append(header);
    const main = element('main'); main.append(element('div', 'Dein Aquarium · Deine Strömung', 'eyebrow'), element('h1', 'Wasser in Bewegung.'), element('p', 'Pumpen, Wellenmodi und Controller an einem Ort. Die verfügbaren Regler richten sich nach dem erkannten Controller-Profil.', 'intro muted'));
    const nav = element('nav'); nav.setAttribute('aria-label', 'Geräteart');
    for (const [id, name] of [['flow','Strömung & Pumpen'],['dosing','Dosierung'],['ble','Bluetooth / DMP']]) {
      const b = this.button(name, () => {this.tab=id;this.render();}, this.tab === id ? 'selected' : ''); b.setAttribute('aria-pressed',String(this.tab===id)); nav.append(b);
    } main.append(nav);
    if (this.error) { const error = element('div',this.error,'error'); error.setAttribute('role','alert');main.append(error); }
    if (this.notice) { const notice = element('div',this.notice,'notice'); notice.setAttribute('role','status');main.append(notice); }
    const shown = groupDevices(this.devices,this.tab);
    if (this.loading) main.append(element('p','Controller werden geladen …','muted'));
    else if (!shown.length) {
      const empty=element('div',null,'empty');empty.append(element('h2','Noch kein Controller in dieser Ansicht'),element('p',this.tab==='ble'?'DMP über „Bluetooth-Diagnose“ in der Integration hinzufügen. Die Steuerung wird nach Protokollprüfung ergänzt.':'Füge deine Jebao-Controller unter Geräte & Dienste hinzu.'));
      const a=element('a','Integration einrichten');a.href='/config/integrations/dashboard/add?domain=jebao_studio';empty.append(a);main.append(empty);
    } else {const grid=element('div',null,'grid');for (const device of shown)grid.append(this.deviceCard(device));main.append(grid);}
    main.append(element('footer','Jebao Studio 0.1.0 · Experimentell · Hardwareprüfung steht aus')); root.append(main);
  }
}
customElements.define('jebao-studio-panel', JebaoStudioPanel);
