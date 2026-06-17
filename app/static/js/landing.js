/* landing.js — Landing page interactivity | Carousel, chatbot, particles, contact form */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sticky navbar ─────────────────────────────────────────
  const nav = document.getElementById('lnav');
  window.addEventListener('scroll', () => {
    nav?.classList.toggle('scrolled', window.scrollY > 50);
  }, { passive: true });


  // ── Mobile hamburger ──────────────────────────────────────
  const ham    = document.getElementById('hamburger');
  const mobMenu= document.getElementById('mobileMenu');
  ham?.addEventListener('click', () => mobMenu?.classList.toggle('open'));


  // ── 3D Carousel ──────────────────────────────────────────
  const track  = document.getElementById('carouselTrack');
  const cards  = track ? [...track.querySelectorAll('.c-card')] : [];
  const dotsWrap = document.getElementById('carDots');
  const dots   = dotsWrap ? [...dotsWrap.querySelectorAll('.car-dot')] : [];
  let current  = 0;
  const VISIBLE= 3;  // cards visible at once

  function getCardWidth() {
    return cards[0] ? cards[0].offsetWidth + 20 : 340; // width + gap
  }

  function updateCarousel() {
    const cw = getCardWidth();
    // Center the current card
    const viewportW = track?.parentElement?.offsetWidth || 800;
    const offset    = current * cw - (viewportW / 2 - cards[0]?.offsetWidth / 2);
    track.style.transform = `translateX(${-offset}px)`;

    // Apply center/side classes
    cards.forEach((card, i) => {
      card.classList.remove('is-center', 'is-side');
      if (i === current)                                    card.classList.add('is-center');
      else if (Math.abs(i - current) <= 2)                 card.classList.add('is-side');
    });

    // Update dots
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
  }

  function goTo(i) {
    current = Math.max(0, Math.min(i, cards.length - 1));
    updateCarousel();
  }

  function next() { goTo(current < cards.length - 1 ? current + 1 : 0); }
  function prev() { goTo(current > 0 ? current - 1 : cards.length - 1); }

  document.getElementById('carNext')?.addEventListener('click', next);
  document.getElementById('carPrev')?.addEventListener('click', prev);

  // Dot click
  dots.forEach((d, i) => d.addEventListener('click', () => goTo(i)));

  // Auto-advance every 4s
  let autoSlide = setInterval(next, 4000);
  track?.addEventListener('mouseenter', () => clearInterval(autoSlide));
  track?.addEventListener('mouseleave', () => { autoSlide = setInterval(next, 4000); });

  // Touch/swipe support
  let touchX = 0;
  track?.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
  track?.addEventListener('touchend',   e => {
    const diff = touchX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) diff > 0 ? next() : prev();
  });

  // Init
  if (cards.length) updateCarousel();
  window.addEventListener('resize', updateCarousel, { passive: true });


  // ── Chatbot float popup ───────────────────────────────────
  const toggle  = document.getElementById('chatbotToggle');
  const win     = document.getElementById('chatbotWin');
  const cwInput = document.getElementById('cwInput');
  const cwSend  = document.getElementById('cwSend');
  const cwClose = document.getElementById('cwClose');

  function openChat() {
    if (!win) return;
    win.classList.add('open');
  }

  function closeChat() {
    if (!win) return;
    win.classList.remove('open');
  }

  toggle?.addEventListener('click', () => {
    if (!win) return;
    if (win.classList.contains('open')) {
      closeChat();
    } else {
      openChat();
    }
  });

  cwClose?.addEventListener('click', closeChat);

  // Quick tip buttons handler
  const quickBtns = document.querySelectorAll('.cw-quick-btn');
  quickBtns?.forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.textContent.trim();
      cwChat(text);
      const quickSection = win?.querySelector('.cw-quick');
      if (quickSection) quickSection.style.display = 'none';
    });
  });

  function appendCWMsg(text, isUser = false) {
    if (!win) return;
    const body = win.querySelector('.cw-body');
    const div  = document.createElement('div');
    div.className = `cw-msg ${isUser ? 'cb-user' : 'cb-bot'}`;
    div.style.marginTop = '.65rem';
    div.innerHTML = `
      <div class="cw-msg-av"><i data-lucide="${isUser ? 'user' : 'message-circle'}"></i></div>
      <div class="cw-bubble">${text}</div>
    `;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    lucide.createIcons();
  }

  async function cwChat(msg) {
    if (!msg.trim()) return;
    appendCWMsg(msg, true);
    if (cwInput) cwInput.value = '';

    // Simple quick replies for landing page (not logged in)
    const lc = msg.toLowerCase();
    let reply = "That's a great question! Sign up to get personalized AI health advice from VitaPulse.";
    if (lc.includes('workout') || lc.includes('exercise'))
      reply = "For fitness goals, try 3-4 sessions/week mixing cardio and strength. Sign up for a personalized plan!";
    else if (lc.includes('sleep'))
      reply = "Aim for 7-9 hours nightly. Keep consistent sleep/wake times. VitaPulse tracks your sleep patterns!";
    else if (lc.includes('diet') || lc.includes('eat') || lc.includes('nutrition'))
      reply = "Focus on whole foods, adequate protein (0.8-1g/lb bodyweight), and hydration. Track with VitaPulse!";
    else if (lc.includes('bmi') || lc.includes('weight'))
      reply = "BMI = weight(kg) / height(m)². Normal range is 18.5-24.9. Use our BMI calculator to check yours!";

    setTimeout(() => appendCWMsg(reply), 600);
  }

  cwSend?.addEventListener('click', () => cwChat(cwInput?.value || ''));
  cwInput?.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); cwChat(cwInput.value); } });


  // ── Particle generator (team section) ────────────────────
  const particlesEl = document.getElementById('particles');
  if (particlesEl) {
    for (let i = 0; i < 20; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      const size = Math.random() * 4 + 2;
      const colors = ['rgba(0,200,151,.6)', 'rgba(74,158,255,.5)', 'rgba(139,92,246,.5)', 'rgba(255,214,0,.4)'];
      Object.assign(p.style, {
        width:  size + 'px',
        height: size + 'px',
        left:   Math.random() * 100 + '%',
        top:    Math.random() * 100 + '%',
        background: colors[Math.floor(Math.random() * colors.length)],
        animationDuration:  (Math.random() * 8 + 6) + 's',
        animationDelay:     (Math.random() * 6) + 's',
      });
      particlesEl.appendChild(p);
    }
  }

  // ========== CONTACT FORM HANDLER ==========
  // (fixed: no nested DOMContentLoaded)
  const contactForm = document.getElementById('contactFormSimple');
  if (contactForm) {
    // Create toast container (if not exists)
    let toast = document.querySelector('.contact-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'contact-toast';
      toast.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="toast-icon">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
        <span>Message sent successfully! We'll get back to you within 24 hours.</span>
      `;
      document.body.appendChild(toast);
    }

    contactForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      const submitBtn = contactForm.querySelector('.contact-submit-simple');
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '<span>Sending...</span>';
      submitBtn.disabled = true;

      // Collect form data (for future backend)
      const formData = new FormData(contactForm);
      
      // Simulate sending (replace with actual fetch when backend is ready)
      setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 4000);
        contactForm.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }, 800);

      // When you have a backend endpoint, uncomment and replace the setTimeout above:
      /*
      try {
        const response = await fetch('/api/contact', { method: 'POST', body: formData });
        if (response.ok) {
          toast.querySelector('span').innerText = 'Message sent successfully! We\'ll contact you within 24 hours.';
          toast.classList.remove('error');
          toast.classList.add('show');
          setTimeout(() => toast.classList.remove('show'), 4000);
          contactForm.reset();
        } else {
          throw new Error('Server error');
        }
      } catch (err) {
        toast.querySelector('span').innerText = 'Failed to send. Please try again later.';
        toast.classList.add('error', 'show');
        setTimeout(() => toast.classList.remove('show'), 4000);
      } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
      }
      */
    });
  }

});