// Dynamically sets body padding-top to match the actual height of the fixed header.
// This ensures content is never obscured regardless of screen size or font scaling.
function adjustBodyPadding() {
    var header = document.querySelector('header');
    if (header) {
        document.body.style.paddingTop = (header.offsetHeight + 20) + 'px';
    }
}

document.addEventListener('DOMContentLoaded', adjustBodyPadding);
window.addEventListener('resize', adjustBodyPadding);

// Hide header on scroll down, show on scroll up
let lastScrollTop = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    
    if (currentScroll > lastScrollTop && currentScroll > 100) {
        // Scrolling DOWN - hide header
        header.classList.add('hide');
    } else {
        // Scrolling UP - show header
        header.classList.remove('hide');
    }
    
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

