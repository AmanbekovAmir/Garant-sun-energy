// ============================================================
// GARANT SUN ENERGY — Баслы JavaScript
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Навигация scroll эффекти ─────────────────────────────
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // ── Hamburger Menu ────────────────────────────────────────
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
      }
    });
  }

  // ── Sidebar (Дашбоард) ────────────────────────────────────
  const sidebarToggle = document.querySelector('#sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // ── Хабарламаларды автоматик жабыў ────────────────────────
  const alerts = document.querySelectorAll('.message-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.animation = 'slideInRight 0.3s ease reverse';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
    alert.addEventListener('click', () => alert.remove());
  });

  // ── Scroll to Top батырмасы ───────────────────────────────
  const scrollBtn = document.querySelector('.scroll-top');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        scrollBtn.classList.add('visible');
      } else {
        scrollBtn.classList.remove('visible');
      }
    });
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Жүклениў экраны ───────────────────────────────────────
  const loader = document.querySelector('.loading-overlay');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 500);
      }, 300);
    });
  }

  // ── Санаўыш анимация ──────────────────────────────────────
  function animateCounter(element, target, duration = 1500) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        element.textContent = Math.round(target).toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.round(start).toLocaleString();
      }
    }, 16);
  }

  const counters = document.querySelectorAll('[data-counter]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.dataset.counter);
        animateCounter(entry.target, target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));

  // ── Fade-in анимация (Scroll) ─────────────────────────────
  const fadeEls = document.querySelectorAll('.fade-in');
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  fadeEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    fadeObserver.observe(el);
  });

  // ── Форма жиберилгенде жүктениў ───────────────────────────
  const forms = document.querySelectorAll('form[data-loading]');
  forms.forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Жиберилмекте...';
      }
    });
  });

  // ── Жеткерилим баҳасын есаплаў (Заказ формасы) ───────────
  const quantityInput = document.querySelector('#id_quantity');
  const productSelect = document.querySelector('#id_product');
  const priceDisplay = document.querySelector('#total-price-display');

  if (quantityInput && productSelect && priceDisplay) {
    const prices = JSON.parse(document.getElementById('product-prices').textContent || '{}');

    function updatePrice() {
      const productId = productSelect.value;
      const qty = parseInt(quantityInput.value) || 1;
      const price = prices[productId] || 0;
      const total = price * qty;
      priceDisplay.textContent = total > 0
        ? total.toLocaleString('kk-KZ') + ' сум'
        : '—';
    }

    productSelect.addEventListener('change', updatePrice);
    quantityInput.addEventListener('input', updatePrice);
    updatePrice();
  }

});
