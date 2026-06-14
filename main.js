/* ═══════════════════════════════════════════════
   STUDENT PORTFOLIO - MAIN JS
═══════════════════════════════════════════════ */

// ── Theme Toggle ──────────────────────────────
const themeToggle = document.getElementById('themeToggle');
const themeIcon   = document.getElementById('themeIcon');
const html        = document.documentElement;

let isDark = localStorage.getItem('theme') !== 'light';
applyTheme(isDark);

function applyTheme(dark) {
  html.setAttribute('data-theme', dark ? 'dark' : 'light');
  if (themeIcon) themeIcon.className = dark ? 'fas fa-moon' : 'fas fa-sun';
  localStorage.setItem('theme', dark ? 'dark' : 'light');
}
if (themeToggle) themeToggle.addEventListener('click', () => { isDark = !isDark; applyTheme(isDark); });

// ── Navbar Scroll ─────────────────────────────
const navbar = document.getElementById('navbar');
const backToTop = document.getElementById('backToTop');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const scroll = window.scrollY;
  if (navbar) navbar.classList.toggle('scrolled', scroll > 20);
  if (backToTop) backToTop.classList.toggle('visible', scroll > 400);
  // Active nav link
  document.querySelectorAll('.nav-link').forEach(link => {
    const section = document.querySelector(link.getAttribute('href'));
    if (section) {
      const top = section.offsetTop - 100;
      const bottom = top + section.offsetHeight;
      link.classList.toggle('active', scroll >= top && scroll < bottom);
    }
  });
  lastScroll = scroll;
});

if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// ── Hamburger / Mobile Menu ────────────────────
const hamburger   = document.getElementById('hamburger');
const mobileMenu  = document.getElementById('mobileMenu');
const mobileClose = document.getElementById('mobileClose');

function closeMobile() { mobileMenu?.classList.remove('open'); }
hamburger?.addEventListener('click', () => mobileMenu?.classList.add('open'));
mobileClose?.addEventListener('click', closeMobile);
document.querySelectorAll('.mobile-link').forEach(l => l.addEventListener('click', closeMobile));

// ── Cursor Glow (desktop only) ────────────────
const cursorGlow = document.getElementById('cursorGlow');
if (window.innerWidth > 768 && cursorGlow) {
  document.addEventListener('mousemove', e => {
    cursorGlow.style.left = e.clientX + 'px';
    cursorGlow.style.top  = e.clientY + 'px';
  });
}

// ── Particles ─────────────────────────────────
const particlesContainer = document.getElementById('particles');
if (particlesContainer) {
  const count = window.innerWidth < 768 ? 15 : 30;
  for (let i = 0; i < count; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 6 + 2;
    p.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random()*100}%;
      animation-duration:${Math.random()*15+10}s;
      animation-delay:${Math.random()*15}s;
      background:${['#6C63FF','#F7971E','#06D6A0','#FF6B9D'][Math.floor(Math.random()*4)]};
    `;
    particlesContainer.appendChild(p);
  }
}

// ── Intersection Observer (Reveal) ────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Animate progress bars
      entry.target.querySelectorAll('.prog-bar-fill').forEach(bar => {
        bar.style.width = bar.dataset.width + '%';
      });
      entry.target.querySelectorAll('.skill-fill').forEach(bar => {
        bar.style.width = bar.dataset.width + '%';
      });
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── Counter Animation ─────────────────────────
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target);
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach(el => counterObserver.observe(el));

function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const isDecimal = target % 1 !== 0;
  const duration = 2000;
  const step = 16;
  const increment = target / (duration / step);
  let current = 0;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = isDecimal ? current.toFixed(1) : Math.floor(current);
  }, step);
}

// ── Radar Chart (Academics) ───────────────────
const radarCanvas = document.getElementById('radarChart');
if (radarCanvas && typeof ACADEMICS_DATA !== 'undefined') {
  const labels = ACADEMICS_DATA.map(a => a.subject);
  const data   = ACADEMICS_DATA.map(a => a.marks);
  new Chart(radarCanvas, {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: 'Marks',
        data,
        backgroundColor: 'rgba(108,99,255,0.15)',
        borderColor: '#6C63FF',
        pointBackgroundColor: '#F7971E',
        pointBorderColor: '#fff',
        pointRadius: 5,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          min: 70, max: 100,
          ticks: { display: false },
          grid: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: { color: '#b0b0d0', font: { size: 11, family: 'Outfit' } }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
}

// ── Skills Tabs ───────────────────────────────
const tabBtns   = document.querySelectorAll('.skills-tab');
const tabPanels = document.querySelectorAll('.skills-panel');
let donutCharts = {};

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    tabBtns.forEach(b => b.classList.remove('active'));
    tabPanels.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    const panel = document.querySelector(`.skills-panel[data-panel="${tab}"]`);
    if (panel) {
      panel.classList.add('active');
      // Animate skill bars
      panel.querySelectorAll('.skill-fill').forEach(bar => {
        bar.style.width = '0%';
        setTimeout(() => bar.style.width = bar.dataset.width + '%', 50);
      });
    }
  });
});

// Init skill bars on first panel
document.querySelectorAll('.skills-panel.active .skill-fill').forEach(bar => {
  setTimeout(() => bar.style.width = bar.dataset.width + '%', 500);
});

// Draw donut charts for skills
if (typeof SKILLS_DATA !== 'undefined') {
  const categories = Object.keys(SKILLS_DATA);
  categories.forEach((cat, idx) => {
    const canvas = document.getElementById(`donut${idx + 1}`);
    if (!canvas) return;
    const skills = SKILLS_DATA[cat];
    const labels = skills.map(s => s.name);
    const data   = skills.map(s => s.level);
    const colors = ['#6C63FF','#F7971E','#06D6A0','#FF6B9D','#4facfe'];
    donutCharts[cat] = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{ data, backgroundColor: colors.slice(0, data.length), borderWidth: 0, hoverOffset: 6 }]
      },
      options: {
        responsive: true, cutout: '70%',
        plugins: {
          legend: { position: 'bottom', labels: { color: '#b0b0d0', font: { family: 'Outfit', size: 11 }, padding: 12 } }
        }
      }
    });
  });
}

// ── Testimonials Slider ───────────────────────
const track   = document.getElementById('testimonialsTrack');
const dots    = document.querySelectorAll('.dot');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let currentSlide = 0;
const totalSlides = dots.length;

function goToSlide(idx) {
  currentSlide = (idx + totalSlides) % totalSlides;
  if (track) track.style.transform = `translateX(-${currentSlide * 100}%)`;
  dots.forEach((d, i) => d.classList.toggle('active', i === currentSlide));
}

prevBtn?.addEventListener('click', () => goToSlide(currentSlide - 1));
nextBtn?.addEventListener('click', () => goToSlide(currentSlide + 1));
dots.forEach(dot => dot.addEventListener('click', () => goToSlide(+dot.dataset.idx)));

// Auto-rotate testimonials
let autoSlide = setInterval(() => goToSlide(currentSlide + 1), 5000);
document.getElementById('testimonialsSlider')?.addEventListener('mouseenter', () => clearInterval(autoSlide));
document.getElementById('testimonialsSlider')?.addEventListener('mouseleave', () => {
  autoSlide = setInterval(() => goToSlide(currentSlide + 1), 5000);
});

// ── Contact Form ──────────────────────────────
const contactForm  = document.getElementById('contactForm');
const formFeedback = document.getElementById('formFeedback');
const submitBtn    = document.getElementById('submitBtn');

contactForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name:    document.getElementById('name').value,
    email:   document.getElementById('email').value,
    subject: document.getElementById('subject').value,
    message: document.getElementById('message').value,
  };

  if (submitBtn) { submitBtn.disabled = true; submitBtn.querySelector('span').textContent = 'Sending...'; }
  if (formFeedback) formFeedback.className = 'form-feedback hidden';

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if (formFeedback) {
      formFeedback.className = result.success ? 'form-feedback success' : 'form-feedback error';
      formFeedback.textContent = result.success ? result.message : result.error;
    }
    if (result.success) {
      contactForm.reset();
      showToast('✅ Message sent successfully!');
    }
  } catch (err) {
    if (formFeedback) {
      formFeedback.className = 'form-feedback error';
      formFeedback.textContent = 'Network error. Please try again.';
    }
  } finally {
    if (submitBtn) { submitBtn.disabled = false; submitBtn.querySelector('span').textContent = 'Send Message'; }
  }
});

// ── Toast Notification ────────────────────────
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

// ── Smooth scroll on mobile menu links ────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── Progress bars on page load ─────────────────
window.addEventListener('load', () => {
  // Trigger prog bars that are already in view
  document.querySelectorAll('.prog-bar-fill').forEach(bar => {
    const rect = bar.getBoundingClientRect();
    if (rect.top < window.innerHeight) bar.style.width = bar.dataset.width + '%';
  });
});

console.log('✨ Student Portfolio loaded!');
