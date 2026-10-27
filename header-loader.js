/**
 * @file header-loader.js
 * Unified header loader script for IToldYouSo Computing service pages.
 *
 * Purpose:
 * Injects the standard website navigation header into service subpages so that
 * all pages share a single consistent header without manual duplication.
 *
 * Deliberately not for:
 * - Managing headers on the root landing page (index.html), which includes its
 *   own static header directly.
 * - Loading external third-party widgets or chat services.
 *
 * Invariants:
 * - Runs only in client Document Object Model (DOM) browser environments.
 * - Requires a <header> element in the host HTML document to target.
 */

/**
 * Injects the canonical website header into the service page header element.
 *
 * Narrative walkthrough:
 * Step 1: Query the document for the top-level <header> container element.
 * Step 2: Verify that the current page is indeed located inside the /services/
 *         directory path, skipping execution otherwise.
 * Step 3: Populate the inner HTML of the header element with the brand logo,
 *         telephone contact link, email address, and consultation note.
 *
 * @returns {void}
 */
function updateHeader() {
    // Step 1: Query the document for the top-level <header> element.
    const headerElement = document.querySelector('header');

    if (headerElement) {
        // Step 2: Detect whether execution is occurring on a service subpage.
        const isServicePage = window.location.pathname.includes('/services/');

        if (!isServicePage) {
            // Skip non-service pages.
            return;
        }

        // Step 3: Insert the canonical company header markup into the element.
        headerElement.innerHTML = `
            <a href="../index.html" class="logo"><img src="/assets/glasses.png" alt="IToldYouSo" /> <span><i>IT</i>oldYouSo Computing</span></a>
            <div class="phone-info">
                <a href="tel:07809590652" class="phone-number">07809590652</a>
                <a href="mailto:contactus@itoldyouso.tech" class="email-address">contactus@itoldyouso.tech</a>
                <p class="consultation-text">Free consultation</p>
            </div>
        `;
    }
}

// Register the header initialisation to run once the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', updateHeader);
