// Verify the heading offset follows the wrapped subject navigation.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
const source = html.match(/function updateSubjectOffset\(\) \{[\s\S]*?\n  \}/)[0];
let result;
const subjectIndex = { offsetHeight: 132 };
const context = {
  subjectIndex,
  getComputedStyle: () => ({ top: '54px' }),
  document: { documentElement: { style: { setProperty: (name, value) => { result = value; } } } }
};
vm.createContext(context);
vm.runInContext(source, context);
for (const height of [78, 132, 186]) {
  subjectIndex.offsetHeight = height;
  vm.runInContext('updateSubjectOffset()', context);
  assert.equal(result, `${54 + height + 16}px`);
}
assert.match(html, /top: var\(--subject-sticky-top, 202px\)/);
assert.match(html, /scroll-margin-top: var\(--subject-sticky-top, 202px\)/);
assert.match(html, /ResizeObserver\(updateSubjectOffset\)/);
console.log('PASS: subject heading and anchor offsets follow navigation height');
