// ===== BLACK CROWN — INDEX EXTRA JS =====

// ── Animated counters ──────────────────────────────
function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        let current = 0;
        const step = Math.ceil(target / 40);
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current;
            if (current >= target) clearInterval(timer);
        }, 40);
    });
}
// Fire on load
window.addEventListener('load', () => setTimeout(animateCounters, 400));

// ── Scroll reveal ──────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const delay = entry.target.style.getPropertyValue('--delay') || '0ms';
            setTimeout(() => {
                entry.target.classList.add('revealed');
            }, parseInt(delay));
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Gallery filter ─────────────────────────────────
document.querySelectorAll('.gtab').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.gtab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.gallery-item').forEach(item => {
            const cats = item.dataset.cat || '';
            if (filter === 'all' || cats.includes(filter)) {
                item.style.display = '';
                item.style.animation = 'fadeScaleIn 0.4s ease forwards';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// ── Before/After slider ────────────────────────────
function initBASlider(sliderId) {
    const slider = document.getElementById(sliderId);
    if (!slider) return;
    const container = slider.closest('.ba-container');
    const afterEl = container.querySelector('.ba-after');
    let dragging = false;

    function setPos(x) {
        const rect = container.getBoundingClientRect();
        let pct = ((x - rect.left) / rect.width) * 100;
        pct = Math.max(5, Math.min(95, pct));
        afterEl.style.clipPath = `inset(0 0 0 ${pct}%)`;
        slider.style.left = pct + '%';
    }

    // Init at 50%
    afterEl.style.clipPath = 'inset(0 0 0 50%)';
    slider.style.left = '50%';

    slider.addEventListener('mousedown', e => { dragging = true; e.preventDefault(); });
    slider.addEventListener('touchstart', e => { dragging = true; }, { passive: true });
    document.addEventListener('mousemove', e => { if (dragging) setPos(e.clientX); });
    document.addEventListener('touchmove', e => { if (dragging) setPos(e.touches[0].clientX); }, { passive: true });
    document.addEventListener('mouseup', () => dragging = false);
    document.addEventListener('touchend', () => dragging = false);
    container.addEventListener('click', e => setPos(e.clientX));
}

initBASlider('baSlider1');
initBASlider('baSlider2');

// ── Reviews carousel ───────────────────────────────
(function initReviews() {
    const track = document.getElementById('reviewsTrack');
    const dotsContainer = document.getElementById('reviewDots');
    if (!track) return;

    const cards = track.querySelectorAll('.review-card');
    let current = 0;
    const total = cards.length;

    // Build dots
    cards.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = 'rnav-dot' + (i === 0 ? ' active' : '');
        dot.addEventListener('click', () => goTo(i));
        dotsContainer.appendChild(dot);
    });

    function goTo(idx) {
        current = (idx + total) % total;
        track.style.transform = `translateX(-${current * 100}%)`;
        dotsContainer.querySelectorAll('.rnav-dot').forEach((d, i) => {
            d.classList.toggle('active', i === current);
        });
    }

    document.getElementById('reviewPrev')?.addEventListener('click', () => goTo(current - 1));
    document.getElementById('reviewNext')?.addEventListener('click', () => goTo(current + 1));

    // Auto-advance
    setInterval(() => goTo(current + 1), 5000);
})();

// ── Live Booking Widget ────────────────────────────
(function initLiveBooking() {
    const panel = document.getElementById('lbwPanel');
    const slotsWrap = document.getElementById('lbwSlotsWrap');
    const slotsGrid = document.getElementById('lbwSlotsGrid');
    const selectedInfo = document.getElementById('lbwSelectedInfo');
    const summary = document.getElementById('lbwSummary');
    const submitBtn = document.getElementById('lbwSubmit');
    const datePicker = document.getElementById('lbwDatePicker');

    // Set default date to today
    if (datePicker) {
        const today = new Date().toISOString().split('T')[0];
        datePicker.value = today;
        document.getElementById('lbwDate').value = today;
    }

    let state = {
        barberId: null,
        barberName: '',
        serviceId: null,
        serviceName: '',
        servicePrice: '',
        date: datePicker ? datePicker.value : '',
        time: ''
    };

    function updateSubmitState() {
        const hasAll = state.barberId && state.serviceId && state.date && state.time;
        submitBtn.disabled = !hasAll;
        if (hasAll) {
            summary.style.display = 'block';
            document.getElementById('sumBarber').textContent = state.barberName;
            document.getElementById('sumService').textContent = state.serviceName;
            document.getElementById('sumDateTime').textContent =
                new Date(state.date + 'T12:00').toLocaleDateString('es-CO', {weekday:'short', day:'numeric', month:'short'})
                + ' · ' + state.time;
            document.getElementById('sumPrice').textContent = state.servicePrice;
        }
    }

    async function loadSlots() {
        if (!state.barberId || !state.date) return;
        slotsGrid.innerHTML = '<span class="lbw-loading">Cargando horarios...</span>';
        slotsWrap.style.display = 'block';

        try {
            const url = `/api/horarios-disponibles?barber_id=${state.barberId}&date=${state.date}&service_id=${state.serviceId || ''}`;
            const res = await fetch(url);
            const data = await res.json();

            // Update panel info
            const booked = data.total_slots - data.slots.length;
            panel.innerHTML = `
                <div class="lbw-stats">
                    <div class="lbw-stat">
                        <span class="lbw-stat-num">${data.slots.length}</span>
                        <span class="lbw-stat-label">Disponibles</span>
                    </div>
                    <div class="lbw-stat">
                        <span class="lbw-stat-num">${booked}</span>
                        <span class="lbw-stat-label">Ocupadas</span>
                    </div>
                    <div class="lbw-stat">
                        <span class="lbw-stat-num">${data.duration || 30}min</span>
                        <span class="lbw-stat-label">Duración</span>
                    </div>
                </div>
            `;

            slotsGrid.innerHTML = '';
            if (data.slots.length === 0) {
                slotsGrid.innerHTML = '<p class="lbw-no-slots">No hay horarios disponibles para esta fecha.</p>';
                return;
            }

            data.slots.forEach(slot => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'lbw-slot';
                btn.textContent = slot;
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.lbw-slot').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    state.time = slot;
                    document.getElementById('lbwTime').value = slot;

                    // Show confirmation info
                    selectedInfo.innerHTML = `
                        <div class="lbw-sel-info">
                            ✓ Seleccionado: <strong>${state.barberName}</strong> a las <strong>${slot}</strong>
                            ${data.duration ? `· Duración aprox: <strong>${data.duration} min</strong>` : ''}
                        </div>`;
                    updateSubmitState();
                });
                slotsGrid.appendChild(btn);
            });

        } catch (e) {
            slotsGrid.innerHTML = '<p class="lbw-no-slots">Error al cargar. Intenta de nuevo.</p>';
        }
    }

    // Barber buttons
    document.querySelectorAll('.lbw-barber-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.lbw-barber-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.barberId = btn.dataset.barber;
            state.barberName = btn.dataset.name;
            document.getElementById('lbwBarberId').value = state.barberId;
            state.time = '';
            loadSlots();
        });
    });

    // Exposed functions for inline onchange handlers
    window.lbwOnDateChange = function(val) {
        state.date = val;
        document.getElementById('lbwDate').value = val;
        state.time = '';
        loadSlots();
        updateSubmitState();
    };

    window.lbwOnServiceChange = function(val) {
        const opt = document.querySelector(`#lbwServicePicker option[value="${val}"]`);
        state.serviceId = val;
        state.serviceName = opt ? opt.textContent.split(' — ')[0] : '';
        state.servicePrice = opt ? '$' + parseInt(opt.dataset.price).toLocaleString('es-CO') : '';
        document.getElementById('lbwServiceId').value = val;
        loadSlots();
        updateSubmitState();
    };
})();

// ── Interactive 3D mouse tilt effect on cards ──
document.querySelectorAll('.barber-card, .showcase-card, .visual-card').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const xc = rect.width / 2;
        const yc = rect.height / 2;
        const dx = x - xc;
        const dy = y - yc;
        card.style.transform = `perspective(1000px) rotateY(${dx / 20}deg) rotateX(${-dy / 20}deg) translateY(-4px)`;
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
    });
});

// ── Service Details Modal ──────────────────────────
(function initServiceModal() {
    const modal = document.getElementById('serviceModal');
    if (!modal) return;
    
    const closeBtn = document.getElementById('smClose');
    const cards = document.querySelectorAll('.showcase-card');
    
    // Category image map
    const categoryImages = {
        'corte': 'https://images.unsplash.com/photo-1599351431202-1e0f0137899a?q=80&w=800&auto=format&fit=crop',
        'barba': 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?q=80&w=800&auto=format&fit=crop',
        'ritual': 'https://images.unsplash.com/photo-1503951914875-452162b0f3f1?q=80&w=800&auto=format&fit=crop',
        'tratamiento': 'https://images.unsplash.com/photo-1534224039826-c7a0c02176f3?q=80&w=800&auto=format&fit=crop',
        'default': 'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?q=80&w=800&auto=format&fit=crop'
    };

    function openModal(data) {
        document.getElementById('smTitle').textContent = data.name;
        document.getElementById('smDesc').textContent = data.desc;
        document.getElementById('smDuration').textContent = `⏱ ${data.duration} min`;
        document.getElementById('smCategory').textContent = data.category;
        document.getElementById('smPriceVal').textContent = data.price;
        
        // Update booking link to select this service
        const bookBtn = document.getElementById('smBookBtn');
        const url = new URL(bookBtn.href, window.location.origin);
        url.searchParams.set('service', data.id);
        bookBtn.href = url.toString();
        
        // Set image
        const imgUrl = categoryImages[data.category.toLowerCase()] || categoryImages['default'];
        document.getElementById('smImage').style.backgroundImage = `url('${imgUrl}')`;
        
        modal.style.display = 'flex';
        // Trigger reflow for transition
        modal.offsetHeight; 
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 400); // Matches CSS transition duration
    }

    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Prevent opening if the user clicked the inner "Reservar" button directly
            if (e.target.closest('.sc-btn')) return;
            
            openModal(card.dataset);
        });
    });

    closeBtn.addEventListener('click', closeModal);
    
    // Close on clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();

