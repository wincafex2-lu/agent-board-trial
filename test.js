// session_id: DOT-87261efa
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { computeProgress } = require('./calc.js');
const { stages } = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/realms.json'), 'utf8'));
let passed = 0;
function test(name, run) {
  run(); // Assertion failures remain uncaught so Node exits nonzero.
  passed++;
  console.log(`PASS ${name}`);
}

for (const [realm, layer, current, rate, expected] of [
  ['煉氣', 1, 10, 30, { remaining: 90, hours: 3, successRate: 95, required: 100, label: '煉氣 1 層' }],
  ['煉氣', 3, 120, 30, { remaining: 180, hours: 6, successRate: 95, required: 300, label: '煉氣 3 層' }],
  ['煉氣', 9, 100, 100, { remaining: 800, hours: 8, successRate: 95, required: 900, label: '煉氣 9 層' }],
  ['築基', null, 500, 100, { remaining: 1500, hours: 15, successRate: 80, required: 2000, label: '築基' }],
  ['金丹', null, 5000, 700, { remaining: 3000, hours: 4.3, successRate: 60, required: 8000, label: '金丹' }],
  ['元嬰', null, 5000, 1000, { remaining: 25000, hours: 25, successRate: 40, required: 30000, label: '元嬰' }]
]) test(`${realm} ${layer ?? ''}`, () => assert.deepEqual(computeProgress(stages, realm, layer, current, rate), expected));

for (const current of [100, 150]) for (const rate of [0, 10]) {
  test(`達標修為 ${current}，產量 ${rate}`, () => {
    const result = computeProgress(stages, '煉氣', 1, current, rate);
    assert.equal(result.remaining, 0);
    assert.equal(result.hours, 0);
  });
}
test('零產量無法估算', () => assert.equal(computeProgress(stages, '煉氣', 1, 0, 0).hours, null));
test('小數四捨五入', () => {
  assert.equal(computeProgress(stages, '煉氣', 1, 0, 80).hours, 1.3);
  assert.equal(computeProgress(stages, '煉氣', 1, 0, 30).hours, 3.3);
});
// session_id: DOT-b2104360 — regression cases from the v1 review.
test('0.35 小時四捨五入為 0.4', () => assert.equal(computeProgress(stages, '煉氣', 1, 93, 20).hours, 0.4));
test('0.15 小時四捨五入為 0.2', () => assert.equal(computeProgress(stages, '煉氣', 1, 97, 20).hours, 0.2));
test('接受小數修為與產量', () => assert.equal(computeProgress(stages, '煉氣', 1, 99.5, 0.25).hours, 2));
const chineseError = error => error instanceof Error && /[\u3400-\u9fff]/u.test(error.message);
for (const realm of ['未知', '', null, 1]) test(`拒絕境界 ${realm}`, () => assert.throws(() => computeProgress(stages, realm, null, 0, 1), chineseError));
for (const layer of [0, 10, -1, 1.5, '1', null, undefined, NaN, Infinity]) test(`拒絕煉氣層數 ${layer}`, () => assert.throws(() => computeProgress(stages, '煉氣', layer, 0, 1), chineseError));
for (const realm of ['築基', '金丹', '元嬰']) for (const layer of [0, 1, undefined]) test(`拒絕 ${realm} 層數 ${layer}`, () => assert.throws(() => computeProgress(stages, realm, layer, 0, 1), chineseError));
for (const value of [-1, NaN, Infinity, -Infinity, '10', null, undefined, true, {}]) {
  test(`拒絕修為 ${String(value)}`, () => assert.throws(() => computeProgress(stages, '煉氣', 1, value, 1), chineseError));
  test(`拒絕產量 ${String(value)}`, () => assert.throws(() => computeProgress(stages, '煉氣', 1, 0, value), chineseError));
}
test('拒絕缺失數值表', () => assert.throws(() => computeProgress([], '煉氣', 1, 0, 1), chineseError));
test('不修改輸入資料', () => {
  const before = JSON.stringify(stages);
  computeProgress(stages, '煉氣', 1, 0, 1);
  assert.equal(JSON.stringify(stages), before);
});
test('瀏覽器 script 載入：無 require、module、DOM', () => {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'calc.js'), 'utf8'), context);
  const result = context.window.Calc.computeProgress(stages, '金丹', null, 5000, 700);
  assert.equal(result.hours, 4.3);
  assert.equal(result.successRate, 60);
});
console.log(`全部通過：${passed} 項測試`);
