/* auth.js — Auth page validation | Feature: Registration/Login */

document.addEventListener('DOMContentLoaded', () => {

  // Password visibility toggles
  document.querySelectorAll('.pwd-eye').forEach(btn => {
    btn.addEventListener('click', () => {
      const inp  = btn.closest('.auth-input-wrap').querySelector('input');
      const ico  = btn.querySelector('i[data-lucide]');
      if (!inp || !ico) return;
      const show = inp.type === 'password';
      inp.type   = show ? 'text' : 'password';
      ico.setAttribute('data-lucide', show ? 'eye-off' : 'eye');
      lucide.createIcons();
    });
  });

  // Live email validation colour
  const emailInp = document.querySelector('input[type="email"]');
  if (emailInp) {
    emailInp.addEventListener('blur', () => {
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInp.value);
      emailInp.style.borderColor = emailInp.value.length === 0 ? '' :
        ok ? 'rgba(16,185,129,.5)' : 'rgba(239,68,68,.4)';
    });
  }

  // Confirm password match
  const pwd1 = document.getElementById('regPwd');
  const pwd2 = document.querySelector('input[name="confirm_password"]');
  if (pwd1 && pwd2) {
    const check = () => {
      if (!pwd2.value) return;
      const match = pwd1.value === pwd2.value;
      pwd2.style.borderColor = match ? 'rgba(16,185,129,.5)' : 'rgba(239,68,68,.4)';
    };
    pwd1.addEventListener('input', check);
    pwd2.addEventListener('input', check);
  }

});
