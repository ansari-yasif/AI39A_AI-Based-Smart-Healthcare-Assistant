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

  // Mock notifications (replace with real API later)
  let notifications = [
    { id: 1, title: 'Welcome to VitaPulse!', time_ago: 'just now', read: false },
    { id: 2, title: 'Your calorie goal updated', time_ago: '2 hours ago', read: false },
    { id: 3, title: 'New AI insights available', time_ago: 'yesterday', read: true },
  ];

  function renderNotifications() {
    if (!notifyBadge || !notifyList) return;
    const unreadCount = notifications.filter(n => !n.read).length;
    notifyBadge.textContent = unreadCount;
    notifyBadge.style.display = unreadCount ? 'block' : 'none';

    if (notifications.length === 0) {
      notifyList.innerHTML = '<div class="notify-empty">No notifications</div>';
      return;
    }
    notifyList.innerHTML = notifications.map(n => `
      <div class="notify-item ${n.read ? '' : 'unread'}" data-id="${n.id}">
        <div class="notify-title">${n.title}</div>
        <div class="notify-time">${n.time_ago}</div>
      </div>
    `).join('');

    document.querySelectorAll('.notify-item').forEach(item => {
      item.addEventListener('click', (e) => {
        const id = parseInt(item.dataset.id);
        const notif = notifications.find(n => n.id === id);
        if (notif && !notif.read) {
          notif.read = true;
          renderNotifications();
        }
      });
    });
  }

  if (markAllBtn) {
    markAllBtn.addEventListener('click', () => {
      notifications.forEach(n => n.read = true);
      renderNotifications();
    });
  }

  renderNotifications();
});