/* main.js — Global VitaPulse JS | Sidebar, scroll animations, flash */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sidebar mobile toggle ─────────────────────────────────
  const sidebar  = document.getElementById('sidebar');
  const sbOpen   = document.getElementById('sbOpen');
  const sbClose  = document.getElementById('sbClose');
  const overlay  = document.getElementById('sbOverlay');

  const openSB  = () => { sidebar?.classList.add('open'); overlay?.classList.add('show'); document.body.style.overflow='hidden'; };
  const closeSB = () => { sidebar?.classList.remove('open'); overlay?.classList.remove('show'); document.body.style.overflow=''; };

  sbOpen?.addEventListener('click',  openSB);
  sbClose?.addEventListener('click', closeSB);
  overlay?.addEventListener('click', closeSB);


  // ── Flash auto-dismiss after 5s ──────────────────────────
  const flashWrap = document.getElementById('flashWrap');
  if (flashWrap) {
    setTimeout(() => {
      flashWrap.querySelectorAll('.flash').forEach(f => {
        f.style.transition = 'opacity .4s ease, transform .4s ease';
        f.style.opacity    = '0';
        f.style.transform  = 'translateX(20px)';
        setTimeout(() => f.remove(), 400);
      });
    }, 5000);
  }


  // ── Scroll-triggered animations (IntersectionObserver) ───
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const delay = e.target.dataset.delay || 0;
        setTimeout(() => e.target.classList.add('visible'), parseInt(delay));
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('[data-anim]').forEach(el => observer.observe(el));


  // ── Topnav date ───────────────────────────────────────────
  const dateEl = document.getElementById('topDate');
  if (dateEl) {
    dateEl.textContent = new Date().toLocaleDateString('en-US', {
      weekday:'short', month:'short', day:'numeric'
    });
  }


  // ── Auto-expand textarea ──────────────────────────────────
  document.querySelectorAll('textarea').forEach(el => {
    el.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 180) + 'px';
    });
  });

});
