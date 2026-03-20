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
