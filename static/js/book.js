// ===== BLACK CROWN — BOOK JS =====

let currentStep = 1;

function nextStep(step) {
  // Validate current step
  if (currentStep === 1) {
    const service = document.querySelector('input[name="service_id"]:checked');
    if (!service) { showAlert('Por favor selecciona un servicio.'); return; }
  }
  if (currentStep === 2) {
    const barber = document.querySelector('input[name="barber_id"]:checked');
    if (!barber) { showAlert('Por favor selecciona un barbero.'); return; }
  }
  if (currentStep === 3) {
    const date = document.getElementById('appointmentDate').value;
    const time = document.getElementById('appointmentTime').value;
    if (!date) { showAlert('Por favor selecciona una fecha.'); return; }
    if (!time) { showAlert('Por favor selecciona una hora.'); return; }
  }
  goToStep(step);
}

function prevStep(step) {
  goToStep(step);
}

function goToStep(step) {
  document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
  document.getElementById('step' + step).classList.add('active');
  currentStep = step;
  updateProgress(step);
  updateSummary();
}

function updateProgress(step) {
  for (let i = 1; i <= 4; i++) {
    const prog = document.getElementById('prog' + i);
    const line = document.getElementById('pline' + (i));
    if (prog) {
      prog.classList.remove('active', 'done');
      if (i < step) prog.classList.add('done');
      else if (i === step) prog.classList.add('active');
    }
    if (line) {
      line.classList.remove('done');
      if (i < step) line.classList.add('done');
    }
  }
}

function updateSummary() {
  const serviceInput = document.querySelector('input[name="service_id"]:checked');
  const barberInput = document.querySelector('input[name="barber_id"]:checked');
  const dateInput = document.getElementById('appointmentDate');
  const timeInput = document.getElementById('appointmentTime');

  if (serviceInput && servicesData[serviceInput.value]) {
    const svc = servicesData[serviceInput.value];
    document.getElementById('sum-service-val').textContent = svc.name;
    document.getElementById('sum-price-val').textContent = svc.price;
  }
  if (barberInput && barbersData[barberInput.value]) {
    document.getElementById('sum-barber-val').textContent = barbersData[barberInput.value].name;
  }
  if (dateInput && dateInput.value) {
    const d = new Date(dateInput.value + 'T12:00:00');
    document.getElementById('sum-date-val').textContent = d.toLocaleDateString('es-CO', { weekday: 'short', day: 'numeric', month: 'short' });
  }
  if (timeInput && timeInput.value) {
    document.getElementById('sum-time-val').textContent = timeInput.value;
  }
}

function showAlert(msg) {
  const existing = document.querySelector('.book-alert');
  if (existing) existing.remove();
  const alert = document.createElement('div');
  alert.className = 'book-alert';
  alert.textContent = msg;
  alert.style.cssText = 'background:rgba(217,83,79,0.1);border:1px solid rgba(217,83,79,0.3);color:#f08080;padding:12px 16px;border-radius:3px;margin-bottom:16px;font-size:14px;animation:fadeUp 0.3s ease;';
  const activeStep = document.querySelector('.form-step.active');
  activeStep.insertBefore(alert, activeStep.querySelector('.step-header').nextSibling);
  setTimeout(() => alert.remove(), 4000);
}

async function loadSlots() {
  const barberId = document.querySelector('input[name="barber_id"]:checked')?.value;
  const date = document.getElementById('appointmentDate').value;
  const grid = document.getElementById('slotsGrid');
  const timeInput = document.getElementById('appointmentTime');

  if (!barberId || !date) {
    grid.innerHTML = '<p class="slots-hint">Selecciona fecha y barbero primero</p>';
    return;
  }

  grid.innerHTML = '<p class="slots-loading">Cargando horarios...</p>';
  timeInput.value = '';
  updateSummary();

  try {
    const res = await fetch(`/api/horarios-disponibles?barber_id=${barberId}&date=${date}`);
    const data = await res.json();

    if (data.slots.length === 0) {
      grid.innerHTML = '<p class="slots-hint">No hay horarios disponibles para esta fecha.</p>';
      return;
    }

    grid.innerHTML = '';
    data.slots.forEach(slot => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'slot-btn';
      btn.textContent = slot;
      btn.addEventListener('click', () => {
        document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        timeInput.value = slot;
        updateSummary();
      });
      grid.appendChild(btn);
    });
  } catch (e) {
    grid.innerHTML = '<p class="slots-hint">Error al cargar horarios. Intenta de nuevo.</p>';
  }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Service selection updates summary
  document.querySelectorAll('input[name="service_id"]').forEach(r => {
    r.addEventListener('change', updateSummary);
  });
  document.querySelectorAll('input[name="barber_id"]').forEach(r => {
    r.addEventListener('change', () => {
      updateSummary();
      loadSlots();
    });
  });
  document.getElementById('appointmentDate')?.addEventListener('change', () => {
    updateSummary();
    loadSlots();
  });

  // Set min date to today
  const today = new Date().toISOString().split('T')[0];
  const dateInput = document.getElementById('appointmentDate');
  if (dateInput) dateInput.min = today;

  updateSummary();
  updateProgress(1);
});
