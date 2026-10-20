const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

// Load the real renderer without bootstrapping DOM or network interactions.
const html = fs.readFileSync('egress/index.html', 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({});
vm.runInContext(script.slice(0, script.lastIndexOf('bootstrap();')), context);
const evaluate = code => vm.runInContext(code, context);

// Reproduce the mixed-unit scale using the actual committed internet rates.
const maximum = evaluate("routeMaxUsd(TRANSFERS.find(t => t.id === 'internet-egress'))");
assert.ok(Math.abs(maximum - 0.12 * 1e9 / 2 ** 30) < 1e-10);

// The same byte volume must cost the same before and after unit normalization.
const converted = evaluate("ratePerGb(0.12, 'GiB')");
assert.ok(Math.abs(converted * 100 - 0.12 * (100e9 / 2 ** 30)) < 1e-10);
assert.equal(evaluate("ratePerGb(0.09, 'GB')"), 0.09);
assert.equal(evaluate("ratePerGb(0, 'GiB')"), 0);
assert.equal(evaluate("ratePerGb(1, 'TB')"), null);

// Real internet rates share one decimal-GB scale while retaining billing labels.
assert.ok(Math.abs(maximum - converted) < 1e-10);
const aws = evaluate("routeCard(TRANSFERS.find(t => t.id === 'internet-egress'))");
assert.match(aws, /width:81%/);
assert.match(aws, /\$0\.12 \/GiB/);
assert.match(aws, /\$0\.09 \/GB/);

// Unsupported units do not acquire a visual bar that suggests comparability.
const unknown = evaluate(`providerPanel({id:'unknown', rates:{aws:{level:'rate',unit:'TB',tiers:[{band:'Any volume',usd:1}]}}}, PROVIDERS[0], true, 1)`);
assert.doesNotMatch(unknown, /class="rung__bar"/);
console.log('PASS: byte-equivalent costs, common bar scale, billing labels and unknown units');
