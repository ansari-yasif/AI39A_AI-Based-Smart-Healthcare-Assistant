/* dashboard.js — Dashboard animations & dropdowns */
document.addEventListener('DOMContentLoaded', () => {

  // Animate calorie progress rings
  document.querySelectorAll('.ring-path').forEach(ring => {
    const da = parseFloat(ring.getAttribute('stroke-dasharray') || 213.6);
    const target = ring.getAttribute('stroke-dashoffset');
    ring.style.strokeDashoffset = da;
    setTimeout(() => {
      ring.style.transition = 'stroke-dashoffset 1.3s cubic-bezier(.4,0,.2,1)';
      ring.style.strokeDashoffset = target;
    }, 300);
  });

  // ========== USER DROPDOWN ==========
  const userDropdown = document.getElementById('userDropdown');
  const userBtn = document.getElementById('userDropdownBtn');

  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('open');
    });
    // Close dropdown when clicking anywhere outside
    document.body.addEventListener('click', () => {
      userDropdown.classList.remove('open');
    });
    // Prevent clicks inside dropdown from closing it
    userDropdown.addEventListener('click', (e) => e.stopPropagation());
  }

  // ========== NOTIFICATION DROPDOWN ==========
  const notifyContainer = document.getElementById('notifyDropdown');
  const notifyBtn = document.getElementById('notifyBtn');
  const notifyBadge = document.getElementById('notifyBadge');
  const notifyList = document.getElementById('notifyList');
  const markAllBtn = document.getElementById('markAllRead');

  if (notifyBtn && notifyContainer) {
    notifyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      notifyContainer.classList.toggle('open');
    });
    document.body.addEventListener('click', () => {
      if (notifyContainer) notifyContainer.classList.remove('open');
    });
    notifyContainer.addEventListener('click', (e) => e.stopPropagation());
  }

  // ── REAL notifications from DB via API ──────────────────────────────
  let notifications = [];

  async function fetchNotifications() {
    try {
      const res = await fetch('/dashboard/notifications/json');
      if (!res.ok) return;
      const data = await res.json();
      notifications = data.notifications || [];
      renderNotifications(data.unread || 0);
    } catch (e) { /* silent fail */ }
  }

  function renderNotifications(unreadCount) {
    if (!notifyBadge || !notifyList) return;
    const cnt = (unreadCount !== undefined) ? unreadCount : notifications.filter(n => !n.read).length;
    notifyBadge.textContent = cnt;
    notifyBadge.style.display = cnt > 0 ? 'block' : 'none';

    if (!notifications.length) {
      notifyList.innerHTML = '<div class="notify-empty"><i data-lucide="bell-off" style="width:28px;height:28px;opacity:.3"></i><p>No notifications</p></div>';
      if (window.lucide) lucide.createIcons();
      return;
    }

    const typeIcon = { info:'info', success:'check-circle', health:'heart-pulse', tip:'lightbulb', warning:'alert-triangle' };
    notifyList.innerHTML = notifications.map(n => `
      <div class="notify-item ${n.read ? '' : 'unread'}" data-id="${n.id}" data-link="${n.link||''}">
        <div style="display:flex;gap:.6rem;align-items:flex-start">
          <i data-lucide="${typeIcon[n.type]||'bell'}" style="width:14px;height:14px;flex-shrink:0;margin-top:2px;color:${n.type==='health'?'#ef4444':n.type==='success'?'#22c55e':'#4A9EFF'}"></i>
          <div>
            <div class="notify-title">${n.title}</div>
            ${n.body ? `<div style="font-size:.72rem;color:#64748b;margin-top:.2rem">${n.body.substring(0,80)}${n.body.length>80?'...':''}</div>` : ''}
            <div class="notify-time">${n.time_ago}</div>
          </div>
        </div>
      </div>
    `).join('');

    if (window.lucide) lucide.createIcons();

    document.querySelectorAll('.notify-item').forEach(item => {
      item.addEventListener('click', async () => {
        const id = parseInt(item.dataset.id);
        const link = item.dataset.link;
        if (!item.classList.contains('unread')) {
          if (link) window.location.href = link;
          return;
        }
        item.classList.remove('unread');
        await fetch('/dashboard/notifications/mark-read', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({id})
        });
        // update badge
        const cnt = document.querySelectorAll('.notify-item.unread').length;
        notifyBadge.textContent = cnt;
        notifyBadge.style.display = cnt > 0 ? 'block' : 'none';
        if (link) window.location.href = link;
      });
    });

    // ── Medicine dose notifications (check every 60s) ──────────────────
    checkMedicineDue();
  }

  if (markAllBtn) {
    markAllBtn.addEventListener('click', async () => {
      await fetch('/dashboard/notifications/mark-all-read', { method: 'POST' });
      await fetchNotifications();
    });
  }

  fetchNotifications();
  // Refresh notifications every 90 seconds
  setInterval(fetchNotifications, 90000);

  // ── Medicine reminder notifications ────────────────────────────────────
  function checkMedicineDue() {
    fetch('/wellness/medicine/due-check')
      .then(r => r.json())
      .then(data => {
        if (!data.due || !data.due.length) return;
        // Show each due medicine as a browser notification if permission granted
        if (Notification && Notification.permission === 'granted') {
          data.due.forEach(m => {
            new Notification('💊 Medicine Reminder — VitaPulse', {
              body: `Time to take ${m.name}${m.dosage ? ' — ' + m.dosage : ''} (${m.time})`,
              icon: '/static/img/logo.svg'
            });
          });
        }
        // Also inject into the notification dropdown so it's visible even without browser perms
        data.due.forEach(m => {
          const exists = notifications.find(n => n.title.includes(m.name) && n.type === 'medicine-due');
          if (!exists) {
            notifications.unshift({
              id: 'med-' + m.id + '-' + m.time,
              title: `💊 Time to take ${m.name}`,
              body: m.dosage ? m.dosage + ` (${m.time})` : `Scheduled at ${m.time}`,
              type: 'health',
              read: false,
              link: '/wellness/medicine',
              time_ago: 'now',
            });
            renderNotifications();
          }
        });
      }).catch(() => {});
  }

  // Request browser notification permission on load
  if (typeof Notification !== 'undefined' && Notification.permission === 'default') {
    Notification.requestPermission();
  }
  // Check medicine due every 60 seconds
  setInterval(checkMedicineDue, 60000);
});