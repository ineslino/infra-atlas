const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

// Exercise the page's actual scoring and presentation functions without network requests.
const html = fs.readFileSync('equivalent-sku/index.html', 'utf8');
const script = html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({});
vm.runInContext(script.slice(0, script.indexOf('// ─── Events')), context);
vm.runInContext(`
  const source = {n:'m5.xlarge', v:4, m:16, cat:'general', arch:'x86'};
  const partial = {n:'c4d-highcpu-4', v:4, m:null, cat:'general', arch:'x86'};
  const complete = {n:'D4_v3', v:4, m:16, cat:'general', arch:'x86'};
  state.cur = {};
  globalThis.partialScore = scoreCandidate(source, partial).score;
  globalThis.partialCard = renderMatch({inst:partial, ...scoreCandidate(source, partial)}, 0, 'gcp');
  globalThis.completeCard = renderMatch({inst:complete, ...scoreCandidate(source, complete)}, 0, 'azure');
  globalThis.overview = renderOverview(source, 'aws', {
    gcp:[{inst:partial, ...scoreCandidate(source, partial)}],
    azure:[{inst:complete, ...scoreCandidate(source, complete)}],
  });
  globalThis.escapedOverview = renderOverview({...source, n:'<script>unsafe</script>', m:null}, 'aws', {});
`, context);

// A perfect score with missing memory must be visibly qualified without changing ranking.
assert.equal(context.partialScore, 100);
assert.match(context.partialCard, /Partial match/);
assert.doesNotMatch(context.partialCard, /tier-high/);
assert.match(context.completeCard, /tier-high/);
assert.doesNotMatch(context.completeCard, /Partial match/);

// Unknown values, empty catalogues and untrusted names remain explicit and safe.
assert.match(context.overview, /<caption>Top matches at a glance<\/caption>/);
assert.match(context.overview, /<td>Unknown<\/td>/);
assert.match(context.overview, /memory unavailable/);
assert.match(context.overview, /No scorable instance types/);
assert.match(context.escapedOverview, /&lt;script&gt;unsafe&lt;\/script&gt;/);
assert.doesNotMatch(context.escapedOverview, /<script>/);
assert.match(html, /id="result-title" role="status" aria-live="polite"/);

// Generation dates must remain honest for old, absent and future timestamps.
const dateInfo = value => vm.runInContext(`catalogueDateInfo(${JSON.stringify(value)}, new Date('2026-10-20T00:15:00Z'))`, context);
assert.equal(dateInfo('2026-10-17T23:59:00Z').age, 3);
assert.match(dateInfo('2026-10-20T00:00:00Z').label, /today/);
assert.match(dateInfo(null).label, /unavailable/);
assert.match(dateInfo('invalid').label, /unavailable/);
assert.match(dateInfo('2026-10-21').label, /future date/);
console.log('PASS: scores, comparison, missing data, escaping, result status and catalogue dates');
