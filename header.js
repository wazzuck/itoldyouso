/**
 * @file header.js
 * Shared sticky header behaviour, Call & Consultation dialogue, and Google
 * Analytics 4 (GA4) conversion and interaction event instrumentation for
 * IToldYouSo Computing.
 *
 * Purpose:
 * 1. Keeps body top padding aligned with the fixed header height.
 * 2. Hides the header on scroll down and reveals it on scroll up.
 * 3. Injects and manages a single shared Call & Consultation <dialog>
 *    across index.html, 404.html, and all services/*.html pages, so every
 *    phone button or telephone link on desktop opens the same dialogue and
 *    updating it in one place updates the whole site.
 * 4. Sends first-party interaction and conversion events via window.gtag
 *    (measurement ID G-XP0QRKTWKZ) without loading any extra scripts.
 *
 * Deliberately not for:
 * - Injecting the <header> markup itself (handled statically or by
 *   header-loader.js).
 * - Making custom fetch/XHR network requests outside the existing Google Tag.
 *
 * Invariants:
 * - Requires header.css for dialogue styling.
 * - Mobile phone browsers (Android, iPhone, iPad, etc.) are never
 *   intercepted so native one-tap tel: dialling keeps working.
 * - Analytics helper degrades silently whenever window.gtag is unavailable.
 */

/**
 * Emit a Google Analytics 4 (GA4) interaction or conversion event safely.
 *
 * @param {string} eventName - Lower-snake-case GA4 event identifier.
 * @param {Object} [params] - Flat scalar key-value reporting parameters.
 * @returns {void}
 */
function trackAnalyticsEvent(eventName, params) {
    if (typeof window.gtag === 'function') {
        window.gtag('event', eventName, params || {});
    }
}

/**
 * Collapse inner whitespace and truncate element copy for reporting labels.
 *
 * @param {HTMLElement|null} el - Element whose label text should be read.
 * @returns {string} Trimmed label truncated to 80 characters.
 */
function cleanAnalyticsLabel(el) {
    if (!el || !el.textContent) {
        return '';
    }
    return el.textContent.replace(/\s+/g, ' ').trim().slice(0, 80);
}

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

        // Step 3: Intercept clicks on any telephone link outside the dialogue
        // and emit call_dialog_open vs direct phone_call_click events.
        document.addEventListener('click', function (event) {
            var telOrTrigger = event.target.closest(
                'a[href^="tel:"], #speak-engineer-trigger, ' +
                '#header-phone-trigger'
            );
            if (!telOrTrigger) {
                return;
            }
            var pagePath = window.location.pathname;
            var triggerText = cleanAnalyticsLabel(telOrTrigger);

            if (isMobileDialer || telOrTrigger.closest('#call-dialog')) {
                trackAnalyticsEvent('phone_call_click', {
                    page_path: pagePath,
                    link_text: triggerText
                });
                return;
            }
            event.preventDefault();
            resetCopyFeedback();
            if (!dialog.open) {
                dialog.showModal();
            }
            trackAnalyticsEvent('call_dialog_open', {
                page_path: pagePath,
                trigger_text: triggerText
            });
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
                    trackAnalyticsEvent('phone_number_copy', {
                        page_path: window.location.pathname
                    });
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

/**
 * Attaches site-wide Google Analytics 4 (GA4) conversion and engagement
 * listeners across index.html, 404.html, and all service pages.
 *
 * Narrative walkthrough:
 * Step 1: Delegate email enquiry clicks (`mailto:`) as `email_quote_click`.
 * Step 2: Delegate outbound clicks to sister domains (`tillswift.com`,
 *         `heathandcity.com`) as `outbound_sister_click`.
 * Step 3: Delegate directory card clicks (`.service-card`, `.related-card`)
 *         as `service_card_click`.
 * Step 4: Track any collapsible `<details class="faq-item">` expansions as
 *         `faq_expand`.
 * Step 5: Track 50% and 90% scroll depth milestones once per page load.
 *
 * @returns {void}
 */
(function initSiteAnalytics() {
    /**
     * Binds delegated click, FAQ toggle, and passive scroll depth handlers.
     *
     * @returns {void}
     */
    function bind() {
        var pagePath = window.location.pathname;

        // Steps 1-3: Single delegated listener for mailto, sister, and card
        // navigation interactions.
        document.addEventListener('click', function (event) {
            var link = event.target.closest('a[href]');
            if (!link) {
                return;
            }
            var href = link.getAttribute('href') || '';
            var label = cleanAnalyticsLabel(link);

            // Step 1: Direct email enquiry link clicked.
            if (href.indexOf('mailto:') === 0) {
                trackAnalyticsEvent('email_quote_click', {
                    page_path: pagePath,
                    link_text: label
                });
                return;
            }

            // Step 2: Outbound navigation to sister practice domains.
            if (
                href.indexOf('tillswift.com') !== -1 ||
                href.indexOf('heathandcity.com') !== -1
            ) {
                trackAnalyticsEvent('outbound_sister_click', {
                    destination_url: href.slice(0, 120),
                    page_path: pagePath,
                    link_text: label
                });
                return;
            }

            // Step 3: Directory or related service card clicked.
            if (
                link.classList.contains('service-card') ||
                link.classList.contains('related-card')
            ) {
                trackAnalyticsEvent('service_card_click', {
                    target_service: href.slice(0, 120),
                    page_path: pagePath,
                    link_text: label
                });
            }
        });

        // Step 4: Record FAQ expansions where collapsible <details> are used.
        document.querySelectorAll('details.faq-item').forEach(function (item) {
            item.addEventListener('toggle', function () {
                if (!item.open) {
                    return;
                }
                var summary = item.querySelector('summary');
                trackAnalyticsEvent('faq_expand', {
                    faq_question: cleanAnalyticsLabel(summary),
                    page_path: pagePath
                });
            });
        });

        // Step 5: Emit 50% and 90% scroll depth milestones once per page view.
        var milestonesReached = { 50: false, 90: false };
        function checkScrollMilestones() {
            var doc = document.documentElement;
            var scrollRange = doc.scrollHeight - window.innerHeight;
            if (scrollRange <= 0) {
                return;
            }
            var pct = ((window.scrollY || doc.scrollTop) / scrollRange) * 100;
            [50, 90].forEach(function (mark) {
                if (!milestonesReached[mark] && pct >= mark) {
                    milestonesReached[mark] = true;
                    trackAnalyticsEvent('scroll_depth', {
                        percent_scrolled: mark,
                        page_path: pagePath
                    });
                }
            });
        }

        window.addEventListener('scroll', checkScrollMilestones, {
            passive: true
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
