// ============================================================
// GARANT SUN ENERGY — Электр энергиясы калькуляторы
// ============================================================

(function () {
  const ELECTRICITY_PRICE = 700;   // 1 кВт·с баҳасы (сум)
  const SUN_HOURS_PER_DAY = 5.5;   // Нукус ушын орта күн саатлары
  const PANEL_EFFICIENCY  = 0.80;  // Система ПӘК-и (80%)
  const PANEL_PRICE_PER_KW = 1_800_000; // 1 кВт орнатыў баҳасы

  const fields = {
    monthlyUsage:    document.getElementById('calc-monthly-usage'),
    panelCount:      document.getElementById('calc-panel-count'),
    panelPower:      document.getElementById('calc-panel-power'),

    // Нәтийжелер
    resSystemKw:     document.getElementById('res-system-kw'),
    resPanelCount:   document.getElementById('res-panel-count'),
    resMonthlyGen:   document.getElementById('res-monthly-gen'),
    resMonthlySave:  document.getElementById('res-monthly-save'),
    resYearlySave:   document.getElementById('res-yearly-save'),
    resInstallCost:  document.getElementById('res-install-cost'),
    resPayback:      document.getElementById('res-payback'),
    resCo2:          document.getElementById('res-co2'),
  };

  function formatNum(n) {
    return Math.round(n).toLocaleString('ru-RU');
  }

  function calculate() {
    const monthly  = parseFloat(fields.monthlyUsage?.value)  || 0;
    const panels   = parseFloat(fields.panelCount?.value)    || 0;
    const panelKw  = parseFloat(fields.panelPower?.value)     || 0.545;

    if (monthly <= 0 && panels <= 0) return;

    let systemKw, panelCount, monthlyGen;

    if (monthly > 0) {
      // Айлық тутынысқа негизлеп есаплаў
      const dailyUsage = monthly / 30;
      systemKw   = dailyUsage / (SUN_HOURS_PER_DAY * PANEL_EFFICIENCY);
      panelCount = Math.ceil(systemKw / panelKw);
      systemKw   = panelCount * panelKw;
    } else {
      // Панель санына негизлеп есаплаў
      panelCount = Math.round(panels);
      systemKw   = panelCount * panelKw;
    }

    monthlyGen = systemKw * SUN_HOURS_PER_DAY * PANEL_EFFICIENCY * 30;

    const actualSave = Math.min(monthlyGen, monthly > 0 ? monthly : monthlyGen);
    const monthlySave  = actualSave * ELECTRICITY_PRICE;
    const yearlySave   = monthlySave * 12;
    const installCost  = systemKw * PANEL_PRICE_PER_KW;
    const payback      = installCost / yearlySave;
    const co2          = monthlyGen * 12 * 0.0005; // тонна CO₂/жыл

    // Нәтийжелерди жазыў
    if (fields.resSystemKw)    fields.resSystemKw.textContent    = systemKw.toFixed(2) + ' кВт';
    if (fields.resPanelCount)  fields.resPanelCount.textContent  = panelCount + ' дана';
    if (fields.resMonthlyGen)  fields.resMonthlyGen.textContent  = formatNum(monthlyGen) + ' кВт·с';
    if (fields.resMonthlySave) fields.resMonthlySave.textContent = formatNum(monthlySave) + ' сум';
    if (fields.resYearlySave)  fields.resYearlySave.textContent  = formatNum(yearlySave) + ' сум';
    if (fields.resInstallCost) fields.resInstallCost.textContent = formatNum(installCost) + ' сум';
    if (fields.resPayback)     fields.resPayback.textContent     = payback.toFixed(1) + ' жыл';
    if (fields.resCo2)         fields.resCo2.textContent         = co2.toFixed(2) + ' т/жыл';

    // Нәтийже карточкасын көрсетиў
    const resultCard = document.querySelector('.calc-result-card');
    if (resultCard) {
      resultCard.style.display = 'block';
      resultCard.style.animation = 'fadeInUp 0.4s ease';
    }
  }

  // Барлық input өзгергенде есаплаў
  Object.values(fields).forEach(el => {
    if (el && el.tagName === 'INPUT') {
      el.addEventListener('input', calculate);
      el.addEventListener('change', calculate);
    }
  });

  // Баслапқы есаплаў
  calculate();

  // Глобаль функция (батырма ушын)
  window.calculateSolar = calculate;
})();
