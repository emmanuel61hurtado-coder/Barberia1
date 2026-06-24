// Scroll Animations and Section Detection
document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.scroll-container');
    const scrollSections = document.querySelectorAll('.scroll-section');
    const progressDots = document.querySelectorAll('.scroll-progress-dot');
    
    // Intersection Observer for section detection
    const observerOptions = {
        root: scrollContainer,
        threshold: 0.2,
        rootMargin: '0px'
    };
    
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                
                // Update progress dots
                const sectionId = entry.target.id;
                progressDots.forEach(dot => {
                    dot.classList.remove('active');
                    if (dot.dataset.target === sectionId) {
                        dot.classList.add('active');
                    }
                });
            } else {
                entry.target.classList.remove('in-view');
            }
        });
    }, observerOptions);
    
    // Observe all sections
    scrollSections.forEach(section => {
        sectionObserver.observe(section);
    });
    
    // Click on progress dots to scroll to section
    progressDots.forEach(dot => {
        dot.addEventListener('click', () => {
            const targetId = dot.dataset.target;
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Parallax effect on scroll
    let ticking = false;
    
    scrollContainer.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrollPos = scrollContainer.scrollTop;
                
                scrollSections.forEach((section, index) => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.offsetHeight;
                    const relativePos = (scrollPos - sectionTop) / sectionHeight;
                    
                    // Apply parallax to background elements
                    const beforeElement = section.querySelector('::before');
                    if (beforeElement) {
                        beforeElement.style.transform = `translateY(${relativePos * 50}px)`;
                    }
                });
                
                ticking = false;
            });
            
            ticking = true;
        }
    });
    
    // Add smooth scroll behavior to navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initial animation for first section
    setTimeout(() => {
        const firstSection = scrollSections[0];
        if (firstSection) {
            firstSection.classList.add('in-view');
        }
    }, 100);
    
    // Wheel event for TikTok-like instant snap
    scrollContainer.addEventListener('wheel', (e) => {
        e.preventDefault();
        
        const delta = e.deltaY;
        const currentScroll = scrollContainer.scrollTop;
        const sectionHeight = window.innerHeight;
        
        if (delta > 0) {
            // Scroll down - instant snap to next section
            const targetScroll = Math.ceil(currentScroll / sectionHeight) * sectionHeight;
            scrollContainer.scrollTo({
                top: targetScroll,
                behavior: 'auto' // Instant, no animation
            });
        } else {
            // Scroll up - instant snap to previous section
            const targetScroll = Math.floor(currentScroll / sectionHeight) * sectionHeight;
            scrollContainer.scrollTo({
                top: targetScroll,
                behavior: 'auto' // Instant, no animation
            });
        }
    }, { passive: false });
    
    // Keyboard navigation for even faster control
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
            e.preventDefault();
            const currentScroll = scrollContainer.scrollTop;
            const sectionHeight = window.innerHeight;
            const targetScroll = Math.ceil(currentScroll / sectionHeight) * sectionHeight;
            scrollContainer.scrollTo({
                top: targetScroll,
                behavior: 'auto'
            });
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            e.preventDefault();
            const currentScroll = scrollContainer.scrollTop;
            const sectionHeight = window.innerHeight;
            const targetScroll = Math.floor(currentScroll / sectionHeight) * sectionHeight;
            scrollContainer.scrollTo({
                top: targetScroll,
                behavior: 'auto'
            });
        }
    });
    
    // Touch swipe for TikTok-like mobile experience
    let touchStartY = 0;
    let touchEndY = 0;
    
    scrollContainer.addEventListener('touchstart', (e) => {
        touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });
    
    scrollContainer.addEventListener('touchend', (e) => {
        touchEndY = e.changedTouches[0].screenY;
        handleSwipe();
    }, { passive: true });
    
    function handleSwipe() {
        const swipeThreshold = 30; // Very sensitive - like TikTok
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > swipeThreshold) {
            const currentScroll = scrollContainer.scrollTop;
            const sectionHeight = window.innerHeight;
            
            if (diff > 0) {
                // Swipe up - scroll down to next section
                const targetScroll = Math.ceil(currentScroll / sectionHeight) * sectionHeight;
                scrollContainer.scrollTo({
                    top: targetScroll,
                    behavior: 'auto' // Instant
                });
            } else {
                // Swipe down - scroll up to previous section
                const targetScroll = Math.floor(currentScroll / sectionHeight) * sectionHeight;
                scrollContainer.scrollTo({
                    top: targetScroll,
                    behavior: 'auto' // Instant
                });
            }
        }
    }
});
