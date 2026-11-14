/**
 * @file header.js
 * Shared sticky header behaviour and Call & Consultation dialogue for
 * IToldYouSo Computing.
 *
 * Purpose:
 * 1. Keeps body top padding aligned with the fixed header height.
 * 2. Hides the header on scroll down and reveals it on scroll up.
 * 3. Injects and manages a single shared Call & Consultation <dialog>
 *    across index.html, 404.html, and all services/*.html pages, so every
 *    phone button or telephone link on desktop opens the same dialogue and
 *    updating it in one place updates the whole site.
 *
 * Deliberately not for:
 * - Injecting the <header> markup itself (handled statically or by
 *   header-loader.js).
 * - Making network requests or loading third-party scripts.
 *
 * Invariants:
 * - Requires header.css for dialogue styling.
 * - Mobile phone browsers (Android, iPhone, iPad, etc.) are never
 *   intercepted so native one-tap tel: dialling keeps working.
 */

// Dynamically sets body padding-top to match the actual height of the fixed
// header, ensuring content is never obscured regardless of screen size.
function adjustBodyPadding() {
    var header = document.querySelector('header');
    if (header) {
        document.body.style.paddingTop = (header.offsetHeight + 20) + 'px';
    }
}

document.addEventListener('DOMContentLoaded', adjustBodyPadding);
window.addEventListener('resize', adjustBodyPadding);

// Hide header on scroll down, show on scroll up.
let lastScrollTop = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', function () {
    let currentScroll =
        window.pageYOffset || document.documentElement.scrollTop;

    if (header) {
        if (currentScroll > lastScrollTop && currentScroll > 100) {
            // Scrolling DOWN - hide header
            header.classList.add('hide');
        } else {
            // Scrolling UP - show header
            header.classList.remove('hide');
        }
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

/**
 * Initialises the shared Call & Consultation dialogue for desktop and
 * Chromebook browsers lacking a configured tel: protocol handler.
 *
 * Narrative walkthrough:
 * Step 1: Locate or inject the single canonical #call-dialog element into
 *         document.body so every page shares identical dialogue markup.
 * Step 2: Detect mobile dialer user agents so mobile phones keep direct
 *         one-tap native tel: calling.
 * Step 3: Delegate clicks on any telephone link (a[href^="tel:"]) outside
 *         the dialogue itself to open #call-dialog on desktop browsers.
 * Step 4: Wire close, backdrop-dismiss, and clipboard copy controls with
 *         an execCommand fallback for older browsers.
 *
 * @returns {void}
 */
(function initCallDialog() {
    var PHONE_DISPLAY = '020 4520 9114';
    var PHONE_URI = 'tel:02045209114';
    var EMAIL_URI =
        'mailto:contactus@itoldyouso.tech?subject=Free%20Initial%20Consultation';

    /**
     * Builds and appends the canonical #call-dialog element if absent.
     *
     * @returns {HTMLDialogElement|null} The dialogue element, or null.
     */
    function ensureDialog() {
        var existing = document.getElementById('call-dialog');
        if (existing) {
            return existing;
        }
        if (!document.body) {
            return null;
        }

        var wrapper = document.createElement('div');
        wrapper.innerHTML =
            '<dialog id="call-dialog" class="call-dialog" ' +
                'aria-labelledby="call-dialog-title">' +
            '  <div class="call-dialog-panel">' +
            '    <div class="call-dialog-header">' +
            '      <span class="call-dialog-badge">' +
                     'Free Initial Consultation</span>' +
            '      <button type="button" class="call-dialog-close" ' +
                     'id="call-dialog-close" ' +
                     'aria-label="Close call dialogue">×</button>' +
            '    </div>' +
            '    <h2 id="call-dialog-title">Speak With an Engineer</h2>' +
            '    <p class="call-dialog-lead">' +
                   'Call our Hampstead engineering desk directly for Greater ' +
                   'London Information Technology (IT), networking, or ' +
                   'Point of Sale (POS) support, or email your requirements ' +
                   'for a fixed, no-obligation statement of work.' +
                 '</p>' +
            '    <div class="call-dialog-box">' +
            '      <div class="call-dialog-row">' +
            '        <a href="' + PHONE_URI + '" class="call-dialog-tel">' +
                       PHONE_DISPLAY + '</a>' +
            '        <button type="button" class="call-dialog-copy" ' +
                       'id="copy-phone-btn" data-phone="' + PHONE_DISPLAY +
                       '">Copy Number</button>' +
            '      </div>' +
            '      <p class="call-dialog-meta">' +
                     'Hours: Mon–Sat, 08:30–19:00 · Out-of-hours commercial ' +
                     'POS cutovers available' +
                   '</p>' +
            '    </div>' +
            '    <p class="call-dialog-status" id="copy-phone-status" ' +
                   'aria-live="polite"></p>' +
            '    <div class="call-dialog-actions">' +
            '      <a href="' + PHONE_URI + '" class="btn-primary">Call ' +
                     PHONE_DISPLAY + '</a>' +
            '      <a href="' + EMAIL_URI + '" class="btn-outline">' +
                     'Email for a Quote</a>' +
            '    </div>' +
            '    <p class="call-dialog-promise">' +
                   'Zero follow-up chasing, cold callbacks, or aggressive ' +
                   'sales tactics.' +
                 '</p>' +
            '  </div>' +
            '</dialog>';

        var dialogNode = wrapper.firstElementChild;
        document.body.appendChild(dialogNode);
        return dialogNode;
    }

    function setup() {
        // Step 1: Ensure the shared dialogue exists in the DOM.
        var dialog = ensureDialog();
        if (!dialog || typeof dialog.showModal !== 'function') {
            return;
        }

        var closeBtn = document.getElementById('call-dialog-close');
        var copyBtn = document.getElementById('copy-phone-btn');
        var statusEl = document.getElementById('copy-phone-status');

        // Step 2: Preserve native one-tap tel: calling on mobile dialers.
        var isMobileDialer =
            /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
                navigator.userAgent || ''
            );

        function resetCopyFeedback() {
            if (copyBtn) {
                copyBtn.removeAttribute('data-copied');
                copyBtn.textContent = 'Copy Number';
            }
            if (statusEl) {
                statusEl.textContent = '';
            }
        }

        // Step 3: Intercept clicks on any telephone link outside the dialogue.
        document.addEventListener('click', function (event) {
            if (isMobileDialer) {
                return;
            }
            var link = event.target.closest(
                'a[href^="tel:"], #speak-engineer-trigger, ' +
                '#header-phone-trigger'
            );
            if (!link || link.closest('#call-dialog')) {
                return;
            }
            event.preventDefault();
            resetCopyFeedback();
            if (!dialog.open) {
                dialog.showModal();
            }
        });

        // Step 4: Wire close, backdrop click, and copy-to-clipboard actions.
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                dialog.close();
            });
        }

        dialog.addEventListener('click', function (event) {
            if (event.target === dialog) {
                dialog.close();
            }
        });

        function fallbackCopy(text, onDone) {
            var input = document.createElement('input');
            input.value = text;
            input.setAttribute('readonly', '');
            input.style.position = 'fixed';
            input.style.opacity = '0';
            dialog.appendChild(input);
            input.select();
            try {
                if (document.execCommand('copy')) {
                    onDone();
                } else if (statusEl) {
                    statusEl.textContent =
                        'Please dial ' + text + ' manually.';
                }
            } finally {
                dialog.removeChild(input);
            }
        }

        if (copyBtn) {
            copyBtn.addEventListener('click', function () {
                var phone =
                    copyBtn.getAttribute('data-phone') || PHONE_DISPLAY;

                function markCopied() {
                    copyBtn.setAttribute('data-copied', 'true');
                    copyBtn.textContent = 'Copied';
                    if (statusEl) {
                        statusEl.textContent =
                            'Copied ' + phone + ' to your clipboard.';
                    }
                }

                if (
                    navigator.clipboard &&
                    typeof navigator.clipboard.writeText === 'function'
                ) {
                    navigator.clipboard
                        .writeText(phone)
                        .then(markCopied)
                        .catch(function () {
                            fallbackCopy(phone, markCopied);
                        });
                } else {
                    fallbackCopy(phone, markCopied);
                }
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setup);
    } else {
        setup();
    }
})();
