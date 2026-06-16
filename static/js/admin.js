// ===== BLACK CROWN — ADMIN JS =====

// Sidebar toggle for mobile
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 &&
        !sidebar.contains(e.target) &&
        !sidebarToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// Auto-dismiss flash messages
document.querySelectorAll('.admin-flash').forEach(flash => {
  setTimeout(() => {
    flash.style.transition = 'opacity 0.5s ease';
    flash.style.opacity = '0';
    setTimeout(() => flash.remove(), 500);
  }, 4000);
});

// Confirm delete prompts
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', (e) => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// Highlight active table rows on hover
document.querySelectorAll('.admin-table tbody tr').forEach(row => {
  row.style.transition = 'background 0.2s';
});

// Status select color feedback
document.querySelectorAll('.status-select').forEach(sel => {
  const colorMap = {
    pendiente: '#f0ad4e',
    confirmada: '#5bc0de',
    completada: '#5cb85c',
    cancelada: '#d9534f'
  };
  function updateColor() {
    sel.style.color = colorMap[sel.value] || '#f0f0ec';
    sel.style.borderColor = colorMap[sel.value] || 'rgba(255,255,255,0.07)';
  }
  updateColor();
  sel.addEventListener('change', updateColor);
});

// Animate stat numbers
document.querySelectorAll('.stat-number').forEach(el => {
  const raw = el.textContent.replace(/[^0-9]/g, '');
  const target = parseInt(raw);
  if (!target || target > 100000) return; // skip large currency numbers

  let current = 0;
  const step = Math.ceil(target / 30);
  const prefix = el.textContent.replace(/[0-9,]/g, '').trim();

  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString('es-CO');
    if (current >= target) clearInterval(timer);
  }, 30);
});
