const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

// Exercise the actual page calculation without network or catalogue fixtures.
const html = fs.readFileSync('tools/egress-cost/index.html', 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({});
vm.runInContext(script.slice(script.indexOf('const RATES ='), script.indexOf('const state =')), context);
vm.runInContext(script.slice(script.indexOf('function computeCost('), script.indexOf('function render(')), context);
const cost = (cloud, gb, transfer = 'internet-egress') => vm.runInContext(`computeCost(${JSON.stringify(transfer)}, ${JSON.stringify(cloud)}, ${gb}).total`, context);
const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-8, `${actual} != ${expected}`);

// GCP uses GiB billing, North America Premium tiers and an unused monthly SKU allowance.
const gibInGb = 2 ** 30 / 1e9;
close(cost('gcp', 1), 0);
close(cost('gcp', gibInGb), 0);
close(cost('gcp', 2 * gibInGb), 0.12);
close(cost('gcp', 1024 * gibInGb), 1023 * 0.12);
close(cost('gcp', 1025 * gibInGb), 1023 * 0.12 + 0.11);
close(cost('gcp', 10240 * gibInGb), 1023 * 0.12 + 9216 * 0.11);
close(cost('gcp', 10241 * gibInGb), 1023 * 0.12 + 9216 * 0.11 + 0.08);
close(cost('gcp', 1, 'cross-az'), 1e9 / 2 ** 30 * 0.01);
close(cost('aws', 100), 0);
close(cost('aws', 101), 0.09);
close(cost('azure', 101), 0.087);

// User GB/TB are decimal; changing display unit must preserve the transferred bytes.
const field = {value: '1'};
const unitsContext = vm.createContext({document: {querySelector: () => field}});
vm.runInContext('const state = {unit:"TB", volumeGB:10240}; const $ = s => document.querySelector(s);', unitsContext);
vm.runInContext(script.slice(script.indexOf('function readVolume('), script.indexOf('function syncDOMFromState(')), unitsContext);
assert.equal(vm.runInContext('readVolume()', unitsContext), 1000);
vm.runInContext('applyUnitToInput()', unitsContext);
assert.equal(field.value, '10.24');
assert.equal(vm.runInContext('readVolume()', unitsContext), 10240);
// TCO must price the same workload using the same native GCP boundaries.
const tco = fs.readFileSync('tools/tco/index.html', 'utf8');
const tcoContext = vm.createContext({});
vm.runInContext('const EGRESS = ' + tco.match(/const EGRESS = ([\s\S]*?);\n/)[1] + ';', tcoContext);
vm.runInContext(tco.match(/function egressCost\([\s\S]*?\n\}/)[0], tcoContext);
for (const gb of [0, 1, gibInGb, 2 * gibInGb, 1000, 1024 * gibInGb, 1025 * gibInGb, 10240 * gibInGb, 10241 * gibInGb]) {
  close(vm.runInContext(`egressCost('gcp', ${gb})`, tcoContext), cost('gcp', gb));
}
console.log('PASS: calculator/TCO free tier, billing-unit conversion, tier boundaries and decimal GB/TB');
