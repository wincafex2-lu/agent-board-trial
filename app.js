// session_id: DOT-b2104360
(function () {
  'use strict';
  const form = document.getElementById('calculator');
  const realm = document.getElementById('realm');
  const layer = document.getElementById('layer');
  const current = document.getElementById('current');
  const perHour = document.getElementById('per-hour');
  const result = document.getElementById('result');
  const error = document.getElementById('error');

  function clearOutput() {
    result.hidden = true;
    error.hidden = true;
    error.textContent = '';
  }

  function syncLayer() {
    const isQi = realm.value === '煉氣';
    document.getElementById('layer-field').hidden = !isQi;
    layer.disabled = !isQi;
  }

  function readNumber(input, label) {
    if (input.value.trim() === '' || !Number.isFinite(input.valueAsNumber) || input.valueAsNumber < 0) {
      throw new Error(label + '請輸入大於或等於 0 的有限數字');
    }
    return input.valueAsNumber;
  }

  function calculate(event) {
    if (event) event.preventDefault();
    clearOutput();
    try {
      if (!window.REALMS || !window.Calc) throw new Error('計算資料載入失敗，請確認頁面所需檔案完整');
      const progress = window.Calc.computeProgress(
        window.REALMS.stages, realm.value, realm.value === '煉氣' ? Number(layer.value) : null,
        readNumber(current, '目前修為：'), readNumber(perHour, '每小時修為產量：')
      );
      document.getElementById('result-title').textContent = progress.label + ' · 突破進度';
      document.getElementById('remaining').textContent = String(progress.remaining);
      document.getElementById('hours').textContent = progress.hours === null || !Number.isFinite(progress.hours)
        ? '無法估算' : '約 ' + progress.hours + ' 小時';
      document.getElementById('success-rate').textContent = progress.successRate + '%';
      result.hidden = false;
    } catch (problem) {
      error.textContent = problem.message || '無法計算，請檢查輸入與資料';
      error.hidden = false;
    }
  }

  realm.addEventListener('change', syncLayer);
  form.addEventListener('input', clearOutput);
  form.addEventListener('change', clearOutput);
  form.addEventListener('submit', calculate);
  syncLayer();
  calculate();
}());
