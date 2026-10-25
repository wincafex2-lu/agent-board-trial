// session_id: DOT-87261efa
(function () {
  'use strict';

  function computeProgress(stages, realm, layer, current, perHour) {
    if (!['煉氣', '築基', '金丹', '元嬰'].includes(realm)) {
      throw new Error('境界不合法');
    }
    if (realm === '煉氣' ? !Number.isInteger(layer) || layer < 1 || layer > 9 : layer !== null) {
      throw new Error('層數不合法：煉氣需為 1 到 9，其他境界需為 null');
    }
    if (!Number.isFinite(current) || current < 0) {
      throw new Error('目前修為必須是非負有限數字');
    }
    if (!Number.isFinite(perHour) || perHour < 0) {
      throw new Error('每小時修為必須是非負有限數字');
    }
    const stage = Array.isArray(stages) && stages.find(item => item && item.realm === realm && item.layer === layer);
    if (!stage || !Number.isFinite(stage.required) || stage.required < 0 ||
        !Number.isFinite(stage.success_rate) || stage.success_rate < 0 || stage.success_rate > 1) {
      throw new Error('境界數值資料不完整或不合法');
    }
    const remaining = Math.max(0, stage.required - current);
    // session_id: DOT-b2104360 — scale before dividing to round half-tenths correctly.
    const hours = remaining === 0 ? 0 : perHour === 0 ? null : Math.round(remaining * 10 / perHour) / 10;
    return {
      remaining,
      hours,
      successRate: Math.round(stage.success_rate * 100),
      required: stage.required,
      label: realm === '煉氣' ? `${realm} ${layer} 層` : realm
    };
  }

  const api = { computeProgress };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof window !== 'undefined') window.Calc = api;
}());
