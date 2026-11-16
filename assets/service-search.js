/*
 * FILE: assets/service-search.js
 *
 * Purpose: the "query tower" of the service search on index.html. It
 * encodes what the visitor types into the same hashed vector space as
 * the pre-built service vectors in assets/search-index.js, scores every
 * service card by cosine similarity, then re-orders and filters the
 * grid. It understands meaning (via the concept lexicon), tolerates
 * typos (character trigrams) and works as you type.
 *
 * Not for: custom search backend API calls or third-party ad tracking.
 * Everything runs locally in the browser from static files, while optionally
 * reporting debounced search terms to the existing first-party Google Tag
 * (window.gtag, measurement ID G-XP0QRKTWKZ) when present.
 *
 * Invariant: normalise, stem, tokenise, fnv1a and featurise MUST match
 * scripts/build_search_index.py step for step.
 */
(function initServiceSearch() {
    'use strict';

    var idx = window.SERVICE_SEARCH_INDEX;
    var input = document.getElementById('service-search-input');
    var status = document.getElementById('service-search-status');
    var empty = document.getElementById('service-search-empty');
    var cards = document.querySelectorAll('.service-card[data-tags]');
    if (!idx || !input || !cards.length) {
        return;
    }

    var DIM = idx.dim;
    var W_WORD = idx.weights[0];
    var W_CONCEPT = idx.weights[1];
    var W_TRIGRAM = idx.weights[2];

    // Step 1: lookup tables built once from the shipped index.
    var stop = {};
    idx.stopwords.forEach(function (w) { stop[w] = true; });
    var concepts = Object.keys(idx.concepts).map(function (name) {
        var set = {};
        idx.concepts[name].forEach(function (w) { set[w] = true; });
        return { name: name, set: set };
    });
    var docByHref = {};
    idx.docs.forEach(function (d) { docByHref[d.h] = d; });
    var cardByHref = {};
    cards.forEach(function (card) {
        cardByHref[card.getAttribute('href')] = card;
    });

    /* Lower-case and reduce text to a-z and 0-9 words (mirrors Python;
       "wi-fi" is folded into "wifi", other hyphens become gaps). */
    function normalise(text) {
        return text.toLowerCase().replace(/wi-fi/g, 'wifi')
            .replace(/[^a-z0-9]+/g, ' ').trim();
    }

    /* Strip plural "s", and "ing"/"ed" on long words (mirrors Python). */
    function stem(w) {
        if (w.length >= 6 && /ing$/.test(w)) { return w.slice(0, -3); }
        if (w.length >= 6 && /ed$/.test(w)) { return w.slice(0, -2); }
        if (w.length > 3 && /s$/.test(w) && !/ss$/.test(w)) {
            return w.slice(0, -1);
        }
        return w;
    }

    /* Stemmed, stop-word-free tokens. */
    function tokenise(text) {
        return normalise(text).split(' ').filter(function (w) {
            return w && !stop[w];
        }).map(stem);
    }

    /* 32-bit FNV-1a hash of an ASCII string. */
    function fnv1a(s) {
        var h = 2166136261;
        for (var i = 0; i < s.length; i++) {
            h ^= s.charCodeAt(i);
            h = Math.imul(h, 16777619) >>> 0;
        }
        return h >>> 0;
    }

    /* Query tower: text -> L2-normalised sparse vector {bucket: w}. */
    function encode(text) {
        var tokens = tokenise(text);
        var seen = {};
        var raw = {};
        function add(name, weight) {
            var b = fnv1a(name) % DIM;
            raw[b] = (raw[b] || 0) + weight;
        }
        tokens.forEach(function (tok) {
            seen[tok] = true;
            add('w:' + tok, W_WORD);
            var padded = '^' + tok + '$';
            for (var i = 0; i < padded.length - 2; i++) {
                add('g:' + padded.substr(i, 3), W_TRIGRAM);
            }
        });
        concepts.forEach(function (c) {
            for (var tok in seen) {
                if (c.set[tok]) {
                    add('c:' + c.name, W_CONCEPT);
                    break;
                }
            }
        });
        var vec = {};
        var norm = 0;
        for (var b in raw) {
            var v = (1 + Math.log(raw[b])) * idx.idf[b];
            vec[b] = v;
            norm += v * v;
        }
        norm = Math.sqrt(norm) || 1;
        for (var k in vec) { vec[k] /= norm; }
        return vec;
    }

    /* Cosine similarity of query vector with a stored document. */
    function score(qvec, doc, qnorm) {
        var s = 0;
        for (var i = 0; i < doc.v.length; i++) {
            var q = qvec[doc.v[i][0]];
            if (q) { s += q * doc.v[i][1]; }
        }
        // Small bonus when the literal phrase appears in the text.
        if (qnorm.length > 2 && doc.x.indexOf(qnorm) !== -1) { s += 0.15; }
        if (qnorm.length > 2 && doc.t.indexOf(qnorm) !== -1) { s += 0.1; }
        return s;
    }

    /* Show every card in its original order. */
    function reset() {
        cards.forEach(function (card) {
            card.classList.remove('is-hidden');
            card.style.order = '';
        });
        empty.hidden = true;
        status.textContent = 'Showing all ' + cards.length + ' services.';
    }

    /* Rank and filter the grid for the current query. */
    var gaSearchTimer = null;
    function scheduleSearchReport(qnorm, shown) {
        if (gaSearchTimer) { clearTimeout(gaSearchTimer); }
        if (!qnorm || qnorm.length < 3) { return; }
        gaSearchTimer = setTimeout(function () {
            if (typeof window.gtag === 'function') {
                window.gtag('event', 'service_search', {
                    search_term: qnorm.slice(0, 80),
                    matches_count: shown
                });
            }
        }, 1000);
    }

    function run() {
        var query = input.value;
        var qnorm = normalise(query);
        if (!qnorm) { reset(); return; }
        var qvec = encode(query);
        var ranked = [];
        var top = 0;
        idx.docs.forEach(function (doc) {
            var s = score(qvec, doc, qnorm);
            ranked.push({ href: doc.h, s: s });
            if (s > top) { top = s; }
        });
        var cutoff = Math.max(0.08, top * 0.35);
        ranked.sort(function (a, b) { return b.s - a.s; });
        var shown = 0;
        ranked.forEach(function (r, i) {
            var card = cardByHref[r.href];
            if (!card) { return; }
            var keep = r.s >= cutoff;
            card.classList.toggle('is-hidden', !keep);
            card.style.order = String(i);
            if (keep) { shown++; }
        });
        empty.hidden = shown !== 0;
        status.textContent = shown === 0
            ? 'No matching services.'
            : shown + (shown === 1 ? ' service matches.'
                : ' services match, best first.');
        scheduleSearchReport(qnorm, shown);
    }

    // Typing demo: types example needs into the placeholder (never the
    // real value, so no search runs) as part of the glow. It replays every
    // time the box scrolls into view. It is cancelled when the box leaves
    // view or the visitor focuses or types, and skipped for reduced motion.
    var examples = [
        'my till will not print',
        'wifi dead zone in the garden',
        'lost photos from an old laptop'
    ];
    var staticHint = input.getAttribute('placeholder');
    // Each run gets a number; a stale run notices it was superseded.
    var currentRun = 0;
    var reduceMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* Cancel any running demo and restore the normal hint text. */
    function stopDemo() {
        currentRun++;
        input.setAttribute('placeholder', staticHint);
    }

    /* Start a fresh glow plus typing demo from the beginning. */
    function startDemo() {
        stopDemo();
        // Skip if the visitor is already using the box.
        if (input.value || document.activeElement === input) { return; }
        // Restart the CSS glow: remove, force a reflow, add again.
        input.classList.remove('is-attention');
        void input.offsetWidth;
        input.classList.add('is-attention');
        if (reduceMotion) { return; }
        var run = currentRun;
        var which = 0;
        var pos = 0;
        var deleting = false;
        function tick() {
            if (run !== currentRun || input.value) { return; }
            var text = examples[which];
            pos += deleting ? -1 : 1;
            input.setAttribute('placeholder',
                text.slice(0, pos) + (pos < text.length || deleting
                    ? '|' : ''));
            var delay = deleting ? 25 : 55;
            if (!deleting && pos === text.length) {
                deleting = true;
                delay = 1400;
            } else if (deleting && pos === 0) {
                deleting = false;
                which++;
                if (which === examples.length) {
                    input.setAttribute('placeholder', staticHint);
                    return;
                }
                delay = 400;
            }
            setTimeout(tick, delay);
        }
        tick();
    }
    input.addEventListener('focus', function () {
        stopDemo();
        input.classList.remove('is-attention');
    });
    input.addEventListener('input', stopDemo);

    // Watch the box: play on every entry into view, reset on every exit.
    if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
            if (entries[0].isIntersecting) {
                startDemo();
            } else {
                stopDemo();
                input.classList.remove('is-attention');
            }
        }, { threshold: 0.6 }).observe(input);
    }

    /*
     * Progressive-enhancement voice dictation via the browser's built-in
     * Web Speech Application Programming Interface (API).
     *
     * Reveals the microphone button only when SpeechRecognition (or
     * webkitSpeechRecognition) is available, configures British English
     * (en-GB) with live interim results, and feeds spoken text straight
     * into the search box so the catalogue filters as the visitor speaks.
     *
     * Arguments: none (closes over input, status, stopDemo, run, reset).
     * Returns: undefined.
     * Side effects: un-hides #service-search-mic, attaches click handler,
     *   updates input.value and status.textContent, and optionally sends
     *   a first-party Google Analytics 4 event via window.gtag.
     */
    function initDictation() {
        var SpeechRec = window.SpeechRecognition ||
            window.webkitSpeechRecognition;
        var micBtn = document.getElementById('service-search-mic');
        if (!SpeechRec || !micBtn) { return; }

        // Step 1: reveal the button now that browser support is confirmed.
        micBtn.hidden = false;
        var listening = false;
        var recognition = null;

        // Step 2: helper to keep button attributes and state synchronised.
        function setListening(active) {
            listening = active;
            micBtn.classList.toggle('is-listening', active);
            micBtn.setAttribute('aria-pressed', active ? 'true' : 'false');
            micBtn.setAttribute('aria-label',
                active ? 'Stop dictation' : 'Dictate your search');
        }

        // Step 3: map speech recognition error codes to clear messages.
        function describeError(code) {
            if (code === 'not-allowed' || code === 'service-not-allowed') {
                return 'Microphone access was blocked. Allow permission ' +
                    'or type your search.';
            }
            if (code === 'no-speech') {
                return 'No speech detected. Try again or type your search.';
            }
            if (code === 'network') {
                return 'Speech recognition could not connect. Please type ' +
                    'your search instead.';
            }
            return 'Voice input unavailable here. Please type your search.';
        }

        // Step 4: start or stop dictation when the microphone is clicked.
        micBtn.addEventListener('click', function () {
            if (listening && recognition) {
                recognition.stop();
                return;
            }
            stopDemo();
            input.classList.remove('is-attention');

            recognition = new SpeechRec();
            recognition.lang = 'en-GB';
            recognition.interimResults = true;
            recognition.continuous = false;
            recognition.maxAlternatives = 1;

            recognition.onstart = function () {
                setListening(true);
                status.textContent = 'Listening... speak what you need.';
                if (typeof window.gtag === 'function') {
                    window.gtag('event', 'service_search_dictate');
                }
            };

            recognition.onresult = function (event) {
                var transcript = '';
                for (var i = 0; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript + ' ';
                }
                input.value = transcript.trim();
                run();
            };

            recognition.onerror = function (event) {
                setListening(false);
                if (event.error !== 'aborted') {
                    status.textContent = describeError(event.error);
                }
            };

            recognition.onend = function () {
                setListening(false);
                if (!input.value.trim() &&
                        status.textContent.indexOf('Listening') === 0) {
                    reset();
                }
            };

            try {
                recognition.start();
            } catch (err) {
                setListening(false);
                status.textContent = describeError('unavailable');
            }
        });
    }

    initDictation();

    input.addEventListener('input', run);
    input.closest('form').addEventListener('submit', function (e) {
        e.preventDefault();
    });
    var q = new URLSearchParams(window.location.search).get('q');
    if (q) { input.value = q; run(); }
})();
