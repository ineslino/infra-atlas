const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

// Run the page's event handlers and renderer with an offline catalogue and minimal DOM.
const html = fs.readFileSync('tools/tco/index.html', 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const handlers = {};
const fields = {};
function element(value = '') {
  return {value, innerHTML:'', textContent:'', hidden:false, disabled:false, attributes:{},
    setAttribute(name, value) { this.attributes[name] = value; },
    removeAttribute(name) { delete this.attributes[name]; },
    addEventListener() {}, contains() { return false; }, querySelector() { return null; }};
}
for (const [id, value, min, max, integer] of [
  ['count','1',1,10000,true], ['hours','730',1,744,true], ['egress','1',0,Infinity,false],
]) {
  const field = element(value);
  field.id = id;
  Object.defineProperty(field, 'valueAsNumber', {get: () => field.value === '' ? NaN : Number(field.value)});
  Object.defineProperty(field, 'validity', {get: () => ({valid:
    Number.isFinite(field.valueAsNumber) && field.valueAsNumber >= min && field.valueAsNumber <= max
    && (!integer || Number.isInteger(field.valueAsNumber))})});
  fields['#'+id] = field;
  fields['#'+id+'-error'] = element();
}
for (const id of ['#results','#input-status','[data-share]']) fields[id] = element();
const context = vm.createContext({
  document:{activeElement:null, querySelector:s => fields[s], querySelectorAll:() => [],
    addEventListener:(name, handler) => { handlers[name] = handler; }},
  HTMLSelectElement:class {}, URLSearchParams,
  location:{pathname:'/tools/tco/',hash:''}, history:{replaceState() {}},
});
vm.runInContext(script.slice(0, script.indexOf('// ─── Boot')), context);
const run = code => vm.runInContext(code, context);
run(`
  const source = {n:'m5.xlarge',v:4,m:16,p:0.192,cat:'general',arch:'x86',inCodes:null};
  state.srcName = source.n;
  ORDER.forEach(cid => {
    const inst = {...source, m:cid === 'gcp' ? null : 16, p:cid === 'gcp' ? null : 0.192};
    state.data[cid] = {list:[inst],regions:[],currency:cid === 'ovh' ? 'EUR' : 'USD',generated:'2026-06-17'};
    state.chosen[cid] = inst.n;
  });
  render();
`);
const results = fields['#results'];
assert.match(results.innerHTML, /140\.16/);

// Reproduce the silent 0-to-730 substitution through the actual input event.
fields['#hours'].value = '0';
handlers.input({target:fields['#hours']});
assert.equal(results.innerHTML, '', 'Invalid hours must suspend all estimates');
assert.equal(fields['[data-share]'].disabled, true);
assert.equal(fields['#hours'].attributes['aria-invalid'], 'true');
assert.match(fields['#hours-error'].textContent, /1.*744/);

// Reject empty, fractional, out-of-range and overflowing input; valid correction restores results.
for (const [id, values] of [['hours',['','-1','745','1.5']], ['count',['0','10001','1.5']], ['egress',['','-1','1e309','1e308']]]) {
  fields['#hours'].value = '730'; fields['#count'].value = '1'; fields['#egress'].value = '1';
  for (const value of values) {
    fields['#'+id].value = value;
    handlers.input({target:fields['#'+id]});
    assert.equal(results.innerHTML, '', `${id}=${value} must suspend estimates`);
  }
}
fields['#egress'].value = '0'; fields['#hours'].value = '1e2';
handlers.input({target:fields['#hours']});
assert.equal(fields['[data-share]'].disabled, false);
assert.match(results.innerHTML, /100h/);
assert.match(results.innerHTML, /Partial match.*memory unavailable/);
assert.match(results.innerHTML, /Compute file: 2026-06-17/);
assert.match(results.innerHTML, /Egress verified: 2026-05-19/);
assert.match(results.innerHTML, /Egress: not mapped/);
assert.match(run("sourceDateLabel(null)"), /unavailable/);
assert.match(run("sourceDateLabel('invalid')"), /unavailable/);
assert.match(run("sourceDateLabel('2026-10-21', new Date('2026-10-20T12:00:00Z'))"), /future date/);
assert.match(run("sourceDateLabel('2026-10-17T23:59:00Z', new Date('2026-10-20T00:01:00Z'))"), /3 days old/);

// A shared fragment must replace previous field values before validation reads them.
run(`location.hash = '#src=azure/m5.xlarge&n=2&h=100&gb=0'; applyHash(); syncWorkloadInputs(); render();`);
assert.equal(Number(fields['#count'].value), 2);
assert.equal(Number(fields['#hours'].value), 100);
assert.equal(Number(fields['#egress'].value), 0);
assert.equal(run('state.count'), 2);
assert.equal(run('state.hours'), 100);
assert.equal(run('state.gb'), 0);
run(`location.hash = '#src=aws/m5.xlarge'; applyHash(); syncWorkloadInputs(); render();`);
assert.equal(run('state.count'), 1);
assert.equal(run('state.hours'), 730);
assert.equal(run('state.gb'), 1024);
console.log('PASS: invalid inputs, recovery, exact numeric values, partial matches and per-total dates');
