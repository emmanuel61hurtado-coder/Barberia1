// Scroll Animations and Section Detection
document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.querySelector('.scroll-container');
    const scrollSections = document.querySelectorAll('.scroll-section');
    const progressDots = document.querySelectorAll('.scroll-progress-dot');
    
    // Intersection Observer for section detection
    const observerOptions = {
        root: scrollContainer,
        threshold: 0.5,
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
    }, 300);
});
