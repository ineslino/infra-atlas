// Exercise the generated browser scoring code, including its reset path.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const cases = [];
for (const slug of fs.readdirSync('decisions')) {
  const path = `decisions/${slug}/index.html`;
  if (!fs.existsSync(path)) continue;
  const html = fs.readFileSync(path, 'utf8');
  const match = html.match(/const WIZ = (.*);/);
  if (!match) continue;
  const data = JSON.parse(match[1]);
  data.qs.forEach((q, qi) => q.a.forEach((answer, ai) => {
    (answer.exclude || []).forEach(i => cases.push([slug, qi, ai, data.cols[i]]));
  }));
}
assert.ok(cases.length > 0);
let checked = 0;
for (const [slug, question, answer, excluded] of cases) {
  const html = fs.readFileSync(`decisions/${slug}/index.html`, 'utf8');
  const script = html.match(/<script>\s*(\(function \(\) \{\s*const WIZ = [\s\S]*?)<\/script>/)[1];
  const data = JSON.parse(script.match(/const WIZ = (.*);/)[1]);
  const combinations = data.qs.reduce((n, q) => n * q.a.length, 1);
  for (let code = 0; code < combinations; code++) {
    let remaining = code;
    const answers = data.qs.map(q => {
      const value = remaining % q.a.length;
      remaining = Math.floor(remaining / q.a.length);
      return value;
    });
    if (answers[question] !== answer) continue;
    const output = {hidden:true, innerHTML:''};
    const reset = {hidden:true, addEventListener(_, fn) {this.click = fn;}};
    const form = {
      querySelector(selector) {return {value:answers[Number(selector.match(/q(\d+)/)[1])]};},
      addEventListener(_, fn) {this.change = fn;},
      reset() {this.didReset = true;},
    };
    vm.runInNewContext(script, {document:{getElementById:id => ({'wiz-form':form,'wiz-result':output,'wiz-reset':reset}[id])}});
    form.change();
    assert.equal(output.hidden, false);
    assert.ok(!output.innerHTML.split('</div>')[0].includes(`<strong>${excluded}</strong>`));
    assert.ok(output.innerHTML.includes('Excluded by requirements'));
    const excludedOptions = new Set(answers.flatMap((a, q) => data.qs[q].a[a].exclude || []));
    if (excludedOptions.size === data.cols.length) {
      assert.ok(output.innerHTML.startsWith('<div class="wiz__call">No option meets all requirements.'));
    }
    reset.click();
    assert.ok(form.didReset && output.hidden && reset.hidden);
    checked++;
  }
}
console.log(`PASS: ${checked} incompatible combinations and resets`);
