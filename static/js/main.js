document.addEventListener('DOMContentLoaded', () => {
    // Hamburger menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const body = document.body;
    
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            body.classList.toggle('menu-open');
        });
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        const sideNav = document.getElementById('side-nav');
        
        // If the click is outside the menu and the toggle button, and the menu is open
        if (sideNav && menuToggle && 
            !sideNav.contains(e.target) && 
            !menuToggle.contains(e.target) && 
            body.classList.contains('menu-open')) {
            body.classList.remove('menu-open');
        }
    });
    
    // Add animation classes on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.stat-item, .project-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight * 0.85) {
                element.classList.add('visible');
            }
        });
    };

    // Back to Home button functionality
    const backButton = document.querySelector('.back-button');
    if (backButton) {
        backButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = '/'; // Redirects to home route
        });
    }

    // Initial check for elements in view
    animateOnScroll();
    
    // Check on scroll
    window.addEventListener('scroll', animateOnScroll);
});
