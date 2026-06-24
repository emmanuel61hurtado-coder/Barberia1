// ===== BLACK CROWN — CLIENT JS (URBAN-ELEGANT) =====

// ── DomReady helper ──────────────────────────────────
function domReady(fn) {
  if (document.readyState !== 'loading') { fn(); }
  else { document.addEventListener('DOMContentLoaded', fn); }
}

domReady(function() {

  // Navbar scroll effect with smooth transition
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (y > 40) navbar.classList.add('scrolled');
      else navbar.classList.remove('scrolled');
    }, { passive: true });
  }

  // ── Mobile menu toggle ─────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const body = document.body;

  function openMobileMenu() {
    if (mobileMenu) mobileMenu.classList.add('open');
    if (navToggle) navToggle.classList.add('active');
    body.style.overflow = 'hidden';
  }
  function closeMobileMenu() {
    if (mobileMenu) mobileMenu.classList.remove('open');
    if (navToggle) navToggle.classList.remove('active');
    body.style.overflow = '';
  }

  if (navToggle) {
    navToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      if (mobileMenu && mobileMenu.classList.contains('open')) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });
  }

  // Close on link click
  if (mobileMenu) {
    mobileMenu.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (link) closeMobileMenu();
    });
    // Close on backdrop click
    const backdrop = mobileMenu.querySelector('.mm-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', closeMobileMenu);
    }
  }

  // Close on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) {
      closeMobileMenu();
    }
  });

  // ── Smooth scroll for anchor links ─────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
  // ── Scroll reveal animation ────────────────────────
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(el) {
      if (el.isIntersecting) {
        const delay = el.target.dataset.delay || 0;
        setTimeout(function() {
          el.target.style.opacity = '1';
          el.target.style.transform = 'translateY(0) scale(1)';
        }, parseInt(delay));
        observer.unobserve(el.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

  document.querySelectorAll('[data-delay]').forEach(function(el) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(28px) scale(0.97)';
    el.style.transition = 'opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1)';
    observer.observe(el);
  });

  // ── Parallax effect on hero orbs ───────────────────
  window.addEventListener('scroll', function() {
    const y = window.scrollY;
    document.querySelectorAll('.hero-orb').forEach(function(orb, i) {
      const speed = i === 0 ? 0.15 : 0.1;
      orb.style.transform = 'translateY(' + (y * speed) + 'px)';
    });
  }, { passive: true });

  // ── Hero title tilt on mouse move ──────────────────
  const heroTitle = document.querySelector('.hero-title-inner');
  const heroSection = document.querySelector('.hero');
  if (heroTitle && heroSection) {
    heroSection.addEventListener('mousemove', function(e) {
      const rect = heroSection.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      heroTitle.style.transform =
        'rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 4) + 'deg) translateZ(0)';
    });
    heroSection.addEventListener('mouseleave', function() {
      heroTitle.style.transform = 'rotateY(0deg) rotateX(0deg) translateZ(0)';
    });
    heroTitle.style.transition = 'transform 0.35s cubic-bezier(0.16, 1, 0.3, 1)';
    heroTitle.style.transformStyle = 'preserve-3d';
  }

});
