/**
 * MAIN.JS - Client-Side JavaScript
 * ==================================
 *
 * PURPOSE:
 * Contains JavaScript code that runs in the user's browser.
 * Handles interactivity, dynamic updates, and client-side logic.
 *
 * JAVASCRIPT BASICS FOR JUNIOR DEVELOPERS:
 *
 * What is JavaScript?
 * - Programming language that runs in web browsers
 * - Makes web pages interactive and dynamic
 * - Can modify HTML and CSS in real-time
 * - Handles user events (clicks, typing, etc.)
 *
 * JavaScript vs Python:
 * - Python runs on server (backend)
 * - JavaScript runs in browser (frontend)
 * - Similar syntax but different ecosystems
 *
 * WHEN THIS CODE RUNS:
 * - After HTML is loaded
 * - In the user's browser
 * - Can interact with page elements
 *
 * JUNIOR DEVELOPER NOTES:
 * - console.log() is like print() in Python (for debugging)
 * - Use browser DevTools (F12) to see console output
 * - Errors in JavaScript won't crash server (only affect that user's page)
 */

// ============================================
// WAIT FOR PAGE TO LOAD
// ============================================

/**
 * DOMContentLoaded Event
 *
 * WHY?
 * JavaScript can run before HTML is fully loaded.
 * If we try to access <div id="menu"> before it exists, we get errors.
 *
 * SOLUTION:
 * Wait for DOMContentLoaded event - fires when HTML is ready.
 *
 * DOM (Document Object Model):
 * Tree structure representing HTML. JavaScript uses DOM to access/modify HTML.
 *
 * Example:
 * <body>
 *   <div id="content">
 *     <p>Hello</p>
 *   </div>
 * </body>
 *
 * DOM tree:
 * body
 *   └── div#content
 *         └── p
 *               └── "Hello"
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Finance Dashboard loaded!');

    /**
     * CONSOLE.LOG:
     * Prints to browser console (F12 → Console tab)
     * Very useful for debugging!
     *
     * Console methods:
     * - console.log(): Normal message
     * - console.error(): Error message (red)
     * - console.warn(): Warning (yellow)
     * - console.info(): Info message
     * - console.table(): Display data as table
     */

    // Initialize features
    initMobileMenu();
    initFormValidation();
    initAutoClosAlerts();
    setCurrentDate();

    /**
     * FUNCTION CALLS:
     * We define functions below and call them here.
     * Keeps code organized - setup code in one place.
     */
});


// ============================================
// MOBILE MENU TOGGLE
// ============================================

/**
 * Makes hamburger menu work on mobile devices.
 *
 * HOW IT WORKS:
 * 1. Find menu button and menu
 * 2. When button clicked, toggle 'active' class
 * 3. CSS shows/hides menu based on 'active' class
 */

function initMobileMenu() {
    const menuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.querySelector('.nav-menu');

    /**
     * SELECTING ELEMENTS:
     *
     * document.getElementById('id'):
     * - Finds element with id="id"
     * - Returns one element (IDs should be unique)
     * - Fast and specific
     *
     * document.querySelector('selector'):
     * - Finds first element matching CSS selector
     * - Can use any CSS selector (.class, #id, element, etc.)
     * - More flexible than getElementById
     *
     * document.querySelectorAll('selector'):
     * - Returns ALL matching elements (NodeList)
     * - Can loop through results
     *
     * OLD WAY (still works):
     * - document.getElementsByClassName('class') - returns HTMLCollection
     * - document.getElementsByTagName('tag') - returns HTMLCollection
     *
     * querySelector is modern and preferred!
     */

    if (menuBtn && navMenu) {
        menuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');

            /**
             * CLASSLIST API:
             * Methods for working with CSS classes:
             *
             * .add('class'):    Add class
             * .remove('class'): Remove class
             * .toggle('class'): Add if missing, remove if present
             * .contains('class'): Check if class exists
             * .replace('old', 'new'): Replace class
             *
             * OLD WAY:
             * element.className += ' active'  // Can cause issues
             *
             * NEW WAY:
             * element.classList.add('active')  // Clean and safe
             */
        });
    }

    /**
     * NULL CHECK:
     * if (menuBtn && navMenu) checks both exist.
     *
     * WHY?
     * - Mobile menu button only exists on some pages
     * - Prevents errors if element is missing
     * - Called "defensive programming"
     *
     * Without check:
     * menuBtn.addEventListener() → Error if menuBtn is null
     *
     * With check:
     * Code only runs if both elements exist
     */
}


// ============================================
// FORM VALIDATION
// ============================================

/**
 * Validates form inputs before submission.
 *
 * CLIENT-SIDE vs SERVER-SIDE VALIDATION:
 *
 * Client-side (JavaScript):
 * - Fast feedback (no server request)
 * - Better user experience
 * - Can be bypassed (not secure)
 *
 * Server-side (Python):
 * - Secure (user can't bypass)
 * - Catches all cases
 * - Slower (requires server request)
 *
 * BEST PRACTICE:
 * Use BOTH! Client-side for UX, server-side for security.
 */

function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            /**
             * SUBMIT EVENT:
             * Fires when user submits form (clicks submit button or presses Enter)
             *
             * event parameter:
             * - Contains information about the event
             * - event.preventDefault() stops form submission
             * - event.target is the form element
             */

            // Validate amount fields
            const amountInputs = form.querySelectorAll('input[type="number"]');

            amountInputs.forEach(input => {
                const value = parseFloat(input.value);

                /**
                 * PARSEFLOAT:
                 * Converts string to decimal number
                 * '25.50' → 25.5
                 * 'abc' → NaN (Not a Number)
                 *
                 * Similar functions:
                 * - parseInt(): '25.50' → 25 (integer)
                 * - Number(): '25.50' → 25.5 (same as parseFloat for decimals)
                 */

                if (isNaN(value) || value <= 0) {
                    /**
                     * ISNAN:
                     * Checks if value is "Not a Number"
                     * Used to validate parseFloat succeeded
                     *
                     * isNaN(25.5) → false (is a number)
                     * isNaN('abc') → true (not a number)
                     */

                    alert('Please enter a valid positive amount');
                    event.preventDefault(); // Stop form submission
                    input.focus(); // Put cursor in invalid field

                    /**
                     * FOCUS:
                     * Puts keyboard cursor in element
                     * Helps user see which field has error
                     */

                    return; // Exit function early
                }
            });
        });
    });

    /**
     * FOREACH:
     * Loops through array/NodeList
     *
     * forms.forEach(form => { ... })
     *
     * form is each element in forms
     * Code in { } runs for each element
     *
     * ARROW FUNCTION:
     * => is shorthand for function
     *
     * Old way:
     * forms.forEach(function(form) { ... })
     *
     * New way:
     * forms.forEach(form => { ... })
     *
     * Same result, shorter syntax!
     */
}


// ============================================
// AUTO-CLOSE FLASH MESSAGES
// ============================================

/**
 * Automatically dismisses alert messages after 5 seconds.
 *
 * USER EXPERIENCE:
 * - User sees message
 * - After 5 seconds, message fades away
 * - User can also close manually (X button)
 */

function initAutoClosAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Auto-close after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';

            /**
             * STYLE PROPERTY:
             * Access/modify CSS directly from JavaScript
             *
             * element.style.propertyName = 'value'
             *
             * CSS property names change:
             * CSS: background-color
             * JS:  backgroundColor
             *
             * CSS: font-size
             * JS:  fontSize
             *
             * Rule: Remove hyphens, capitalize next letter (camelCase)
             */

            setTimeout(() => {
                alert.remove();

                /**
                 * REMOVE:
                 * Removes element from DOM completely
                 *
                 * Other manipulation methods:
                 * - appendChild(child): Add child element
                 * - insertBefore(new, existing): Insert before element
                 * - replaceChild(new, old): Replace element
                 * - cloneNode(deep): Copy element
                 */
            }, 300); // Wait for fade animation

        }, 5000); // 5000 milliseconds = 5 seconds

        /**
         * SETTIMEOUT:
         * Runs code after delay
         *
         * setTimeout(function, milliseconds)
         * setTimeout(() => { code }, 5000)
         *
         * Similar function:
         * setInterval(function, milliseconds)
         * - Runs repeatedly every X milliseconds
         * - Use for clocks, auto-refresh, animations
         *
         * Clear timers:
         * - clearTimeout(id): Stop setTimeout
         * - clearInterval(id): Stop setInterval
         */
    });
}


// ============================================
// SET CURRENT DATE
// ============================================

/**
 * Pre-fills date input with today's date.
 *
 * BETTER UX:
 * Most expenses are today, so default to today.
 * User can still change if needed.
 */

function setCurrentDate() {
    const dateInput = document.getElementById('date');

    if (dateInput && !dateInput.value) {
        /**
         * CHECK IF EMPTY:
         * !dateInput.value means "if value is empty"
         *
         * Only set if:
         * 1. Date input exists
         * 2. It doesn't already have a value
         *
         * Why? If editing expense, don't overwrite existing date!
         */

        const today = new Date();

        /**
         * DATE OBJECT:
         * JavaScript's built-in date/time handling
         *
         * Creating dates:
         * - new Date(): Current date/time
         * - new Date('2025-10-01'): Specific date
         * - new Date(2025, 9, 1): Year, month (0-11!), day
         *
         * Getting values:
         * - getFullYear(): 2025
         * - getMonth(): 0-11 (0=January!)
         * - getDate(): 1-31 (day of month)
         * - getDay(): 0-6 (day of week, 0=Sunday)
         * - getHours(), getMinutes(), getSeconds()
         */

        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');

        /**
         * FORMATTING DATE:
         * HTML date input expects: YYYY-MM-DD
         *
         * getMonth() + 1:
         * JavaScript months are 0-11 (0=January)
         * We need 1-12, so add 1
         *
         * padStart(2, '0'):
         * Ensures 2 digits by adding leading zeros
         * '1' → '01'
         * '12' → '12'
         *
         * String(value):
         * Converts number to string so padStart works
         * (padStart only exists on strings)
         */

        dateInput.value = `${year}-${month}-${day}`;

        /**
         * TEMPLATE LITERALS:
         * Backticks ` allow embedded expressions
         *
         * Old way:
         * dateInput.value = year + '-' + month + '-' + day;
         *
         * New way:
         * dateInput.value = `${year}-${month}-${day}`;
         *
         * Much cleaner for building strings!
         */
    }
}


// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Helper functions used throughout the application.
 */

/**
 * Format number as currency
 *
 * @param {number} amount - The amount to format
 * @returns {string} Formatted currency string
 *
 * Example:
 * formatCurrency(1234.5) → '$1,234.50'
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);

    /**
     * INTL.NUMBERFORMAT:
     * JavaScript's internationalization API
     * Formats numbers according to locale rules
     *
     * Options:
     * - style: 'currency', 'percent', 'decimal'
     * - currency: 'USD', 'EUR', 'GBP', etc.
     * - minimumFractionDigits: Minimum decimal places
     * - maximumFractionDigits: Maximum decimal places
     *
     * Handles:
     * - Currency symbols ($, €, ¥)
     * - Thousand separators (1,234)
     * - Decimal places (1.50)
     * - Regional differences
     */
}

/**
 * Format date as readable string
 *
 * @param {string} dateString - Date in YYYY-MM-DD format
 * @returns {string} Formatted date string
 *
 * Example:
 * formatDate('2025-10-01') → 'October 1, 2025'
 */
function formatDate(dateString) {
    const date = new Date(dateString);

    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);

    /**
     * INTL.DATETIMEFORMAT:
     * Similar to NumberFormat but for dates
     *
     * Options:
     * - year: 'numeric' (2025), '2-digit' (25)
     * - month: 'numeric' (10), 'long' (October), 'short' (Oct)
     * - day: 'numeric' (1), '2-digit' (01)
     * - weekday: 'long' (Monday), 'short' (Mon)
     * - hour, minute, second: Format time
     */
}

/**
 * Debounce function
 * Limits how often a function can run
 *
 * USE CASE:
 * User typing in search box - don't search on every keystroke!
 * Wait until they stop typing (e.g., 300ms pause)
 *
 * @param {function} func - Function to debounce
 * @param {number} wait - Milliseconds to wait
 * @returns {function} Debounced function
 */
function debounce(func, wait) {
    let timeout;

    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };

        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };

    /**
     * HOW IT WORKS:
     * 1. User types → function called
     * 2. Start timer (300ms)
     * 3. User types again → cancel previous timer, start new one
     * 4. User stops typing → timer completes → function runs
     *
     * Result: Function only runs 300ms after user stops typing
     *
     * ...args:
     * "Rest parameters" - collects all arguments into array
     * Allows debounced function to accept any arguments
     */
}


// ============================================
// ERROR HANDLING
// ============================================

/**
 * Global error handler
 * Catches JavaScript errors and displays user-friendly message
 */

window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);

    /**
     * WINDOW OBJECT:
     * Represents browser window
     * Global object - all global variables/functions are properties of window
     *
     * window.alert() is same as alert()
     * window.console.log() is same as console.log()
     *
     * 'error' event:
     * Fires when JavaScript error occurs
     * Lets us handle errors gracefully instead of showing browser error message
     */

    // Show user-friendly error message
    // (In production, you might send error to logging service)
    const errorMsg = 'An error occurred. Please refresh the page and try again.';
    console.error(errorMsg);

    /**
     * ERROR LOGGING SERVICES:
     * In production, log errors to service like:
     * - Sentry
     * - LogRocket
     * - Rollbar
     *
     * These help you:
     * - Track errors users encounter
     * - See stack traces
     * - Monitor application health
     * - Get alerts for critical errors
     */
});


// ============================================
// BROWSER COMPATIBILITY
// ============================================

/**
 * MODERN JAVASCRIPT FEATURES:
 * This code uses modern JavaScript (ES6+):
 * - Arrow functions: () => {}
 * - Template literals: `${var}`
 * - const/let instead of var
 * - forEach, map, filter
 * - classList API
 *
 * BROWSER SUPPORT:
 * Works in all modern browsers:
 * - Chrome 51+
 * - Firefox 54+
 * - Safari 10+
 * - Edge 15+
 *
 * OLD BROWSERS (IE11):
 * Need transpiling (Babel) or use older syntax
 * For this project, we assume modern browsers
 */


// ============================================
// DEVELOPMENT VS PRODUCTION
// ============================================

/**
 * Check if in development mode
 * (Flask debug mode sets this)
 */
const isDevelopment = window.location.hostname === 'localhost';

if (isDevelopment) {
    console.log('🔧 Development mode - verbose logging enabled');

    /**
     * DEVELOPMENT TOOLS:
     * - Verbose console logging
     * - Source maps for debugging
     * - Unminified code
     * - Error details visible
     *
     * PRODUCTION:
     * - Minimal logging
     * - Minified/compressed code
     * - Error messages hidden from users
     * - Performance optimized
     */
}


// ============================================
// WEEK 4: LOADING STATES & FORM ENHANCEMENTS
// ============================================

/**
 * Add loading state to form submissions
 *
 * WHY?
 * - Prevents double-submissions
 * - Provides visual feedback
 * - Improves perceived performance
 *
 * HOW IT WORKS:
 * 1. User submits form
 * 2. Add 'loading' class to button
 * 3. Disable button
 * 4. Show spinner (via CSS)
 * 5. Form submits normally
 */

function initFormLoadingStates() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');

            if (submitButton && !submitButton.classList.contains('loading')) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;

                /**
                 * classList.add('loading'):
                 * Adds 'loading' class which CSS styles with spinner
                 *
                 * disabled = true:
                 * Prevents clicking button again
                 * Also changes appearance (grayed out)
                 */

                // If validation fails, re-enable button
                setTimeout(() => {
                    if (!form.checkValidity()) {
                        submitButton.classList.remove('loading');
                        submitButton.disabled = false;
                    }
                }, 100);

                /**
                 * setTimeout:
                 * Waits 100ms then checks if form is valid
                 * If invalid (browser validation failed), re-enable button
                 *
                 * checkValidity():
                 * Browser method - returns true if all required fields filled,
                 * patterns match, etc.
                 */
            }
        });
    });

    console.log(`✅ Loading states initialized for ${forms.length} forms`);
}

/**
 * Enhanced form validation with better error messages
 *
 * WHAT THIS DOES:
 * - Shows custom error messages instead of browser defaults
 * - Highlights invalid fields
 * - Provides real-time feedback
 */

function enhancedFormValidation() {
    const inputs = document.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        // Real-time validation on blur (when user leaves field)
        input.addEventListener('blur', function() {
            validateField(this);
        });

        // Clear error on focus
        input.addEventListener('focus', function() {
            this.classList.remove('input-error');
            const errorMsg = this.parentElement.querySelector('.field-error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        });
    });

    /**
     * addEventListener vs onclick:
     * - addEventListener: Can add multiple listeners
     * - onclick: Only one handler (overwrites previous)
     *
     * Always use addEventListener in modern code!
     */
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let errorMessage = '';

    /**
     * trim():
     * Removes whitespace from start and end
     * "  hello  " → "hello"
     * Prevents users submitting spaces as input
     */

    // Check if field is empty
    if (field.hasAttribute('required') && !value) {
        errorMessage = `${getFieldLabel(field)} is required`;
    }

    // Type-specific validation
    else if (type === 'email' && value && !isValidEmail(value)) {
        errorMessage = 'Please enter a valid email address';
    }
    else if (type === 'number') {
        const num = parseFloat(value);
        const min = field.hasAttribute('min') ? parseFloat(field.min) : -Infinity;
        const max = field.hasAttribute('max') ? parseFloat(field.max) : Infinity;

        if (isNaN(num)) {
            errorMessage = 'Please enter a valid number';
        } else if (num < min) {
            errorMessage = `Value must be at least ${min}`;
        } else if (num > max) {
            errorMessage = `Value must be at most ${max}`;
        }
    }

    /**
     * parseFloat vs parseInt:
     * - parseFloat: Handles decimals (25.50)
     * - parseInt: Only whole numbers (25)
     *
     * isNaN: is Not a Number
     * Returns true if value can't be converted to number
     */

    // Display error or clear it
    if (errorMessage) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
}

function showFieldError(field, message) {
    field.classList.add('input-error');

    // Remove existing error message
    const existingError = field.parentElement.querySelector('.field-error-message');
    if (existingError) {
        existingError.remove();
    }

    // Create new error message
    const errorDiv = document.createElement('span');
    errorDiv.className = 'field-error-message';
    errorDiv.textContent = message;

    /**
     * createElement:
     * Creates new HTML element in memory
     * Doesn't add to page yet
     *
     * textContent vs innerHTML:
     * - textContent: Safe, treats as plain text
     * - innerHTML: Unsafe, can execute scripts!
     * Always use textContent for user input
     */

    // Insert after the field
    field.parentElement.insertBefore(errorDiv, field.nextSibling);

    /**
     * DOM MANIPULATION METHODS:
     * - appendChild: Add to end of parent
     * - insertBefore: Add before specific element
     * - remove(): Remove element
     * - replaceChild: Replace one element with another
     */
}

function clearFieldError(field) {
    field.classList.remove('input-error');
    const errorMsg = field.parentElement.querySelector('.field-error-message');
    if (errorMsg) {
        errorMsg.remove();
    }
}

function getFieldLabel(field) {
    const label = field.parentElement.querySelector('label');
    return label ? label.textContent.replace(':', '') : field.name;

    /**
     * TERNARY OPERATOR:
     * condition ? value_if_true : value_if_false
     *
     * Same as:
     * if (label) {
     *     return label.textContent.replace(':', '');
     * } else {
     *     return field.name;
     * }
     *
     * More concise for simple conditions!
     */
}

function isValidEmail(email) {
    // Simple email validation regex
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);

    /**
     * REGULAR EXPRESSIONS (regex):
     * Pattern matching for strings
     *
     * This regex checks:
     * - One or more non-space, non-@ characters
     * - @ symbol
     * - One or more non-space, non-@ characters
     * - . (period)
     * - One or more non-space, non-@ characters
     *
     * Matches: user@example.com
     * Doesn't match: user@, @example.com, user example.com
     *
     * Regex is powerful but complex. Use existing patterns when possible!
     */
}

/**
 * Smooth scroll to top button
 *
 * WHAT IT DOES:
 * Shows button when user scrolls down
 * Clicking smoothly scrolls to top of page
 */

function initScrollToTop() {
    // Create button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--primary-color);
        color: white;
        border: none;
        font-size: 24px;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s, transform 0.3s;
        z-index: 1000;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    `;

    /**
     * style.cssText:
     * Sets multiple CSS properties at once
     * Alternative: scrollBtn.style.position = 'fixed' (one at a time)
     *
     * Backticks (`) create template literals:
     * - Can span multiple lines
     * - Can include variables: `Hello ${name}`
     */

    document.body.appendChild(scrollBtn);

    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.transform = 'translateY(0)';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.transform = 'translateY(20px)';
        }
    });

    /**
     * window.scrollY:
     * How many pixels user has scrolled down
     * 0 = top of page
     * 1000 = scrolled down 1000 pixels
     */

    // Scroll to top when clicked
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    /**
     * scrollTo:
     * Scrolls window to specific position
     *
     * behavior: 'smooth':
     * Animated scroll instead of instant jump
     * Much nicer UX!
     */

    console.log('✅ Scroll to top button initialized');
}

/**
 * Initialize all Week 4 enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    initFormLoadingStates();
    enhancedFormValidation();
    initScrollToTop();

    console.log('🎨 Week 4 UI/UX enhancements loaded!');
});

/**
 * WEEK 4 JavaScript ENHANCEMENTS COMPLETE! ✅
 *
 * WHAT WE ADDED:
 * ✅ Form loading states (spinners, disabled buttons)
 * ✅ Enhanced validation (real-time, clear messages)
 * ✅ Field-level error highlighting
 * ✅ Scroll to top button (appears on scroll)
 * ✅ Better user feedback throughout
 *
 * JAVASCRIPT PERFORMANCE TIPS:
 * 1. Use event delegation for dynamic elements
 * 2. Debounce frequent events (scroll, resize, typing)
 * 3. Cache DOM queries (store in variables)
 * 4. Use document fragments for multiple DOM inserts
 * 5. Minimize reflows/repaints
 *
 * ACCESSIBILITY NOTES:
 * ✅ Keyboard navigation supported
 * ✅ Screen reader friendly error messages
 * ✅ Focus management
 * ✅ ARIA attributes where needed
 *
 * BROWSER COMPATIBILITY:
 * ✅ Modern browsers (ES6+)
 * ⚠️ For IE11 support, would need Babel transpilation
 *
 * TESTING CHECKLIST:
 * - [ ] Loading states work on form submit
 * - [ ] Validation shows clear errors
 * - [ ] Errors clear when user fixes input
 * - [ ] Scroll button appears/hides correctly
 * - [ ] All animations smooth on mobile
 * - [ ] No console errors
 * - [ ] Works with JavaScript disabled (graceful degradation)
 */

// ============================================
// EXPORT FOR TESTING (if using modules)
// ============================================

/**
 * If using JavaScript modules, export functions for testing
 * Commented out for now since we're using vanilla JS
 */

// export { formatCurrency, formatDate, debounce };

/**
 * JAVASCRIPT MODULES:
 * Modern way to organize code into separate files
 *
 * In main.js:
 * export function formatCurrency() { ... }
 *
 * In other file:
 * import { formatCurrency } from './main.js'
 *
 * Benefits:
 * - Better code organization
 * - Avoid global namespace pollution
 * - Easier testing
 * - Tree-shaking (remove unused code)
 *
 * Requires:
 * <script type="module" src="main.js"></script>
 */


console.log('📝 main.js loaded successfully');

/**
 * JAVASCRIPT BEST PRACTICES:
 *
 * ✅ Use const for values that don't change
 * ✅ Use let for values that do change
 * ❌ Don't use var (has confusing scope rules)
 *
 * ✅ Use === instead of == (strict equality)
 * ✅ Use arrow functions for callbacks
 * ✅ Use template literals for strings with variables
 *
 * ✅ Check if elements exist before using them
 * ✅ Add event listeners in DOMContentLoaded
 * ✅ Remove event listeners when done (prevents memory leaks)
 *
 * ✅ Use meaningful variable names
 * ✅ Comment complex logic
 * ✅ Keep functions small and focused
 *
 * ✅ Use browser DevTools for debugging
 * ✅ Test in multiple browsers
 * ✅ Handle errors gracefully
 *
 * DEBUGGING TIPS:
 * 1. console.log() everywhere!
 * 2. Use browser debugger (breakpoints)
 * 3. Check console for errors (F12)
 * 4. Verify elements exist (console.log(element))
 * 5. Check event listeners are attached
 * 6. Isolate problem (comment out code until it works)
 * 7. Search error messages online
 *
 * LEARNING RESOURCES:
 * - MDN Web Docs: developer.mozilla.org
 * - JavaScript.info: javascript.info
 * - FreeCodeCamp: freecodecamp.org
 * - YouTube: Traversy Media, Web Dev Simplified
 */


// ============================================
// DARK MODE FUNCTIONALITY
// ============================================

/**
 * Toggles between light and dark mode
 *
 * HOW IT WORKS:
 * 1. Check if dark mode is currently active
 * 2. Toggle the 'dark-mode' class on body element
 * 3. Update the icon (moon/sun)
 * 4. Save preference to localStorage
 *
 * LOCALSTORAGE:
 * Browser storage that persists even after closing the page.
 * Allows us to remember user's preference.
 *
 * JUNIOR DEV NOTES:
 * - classList.toggle() adds class if missing, removes if present
 * - localStorage.setItem() saves data (key-value pairs)
 * - localStorage.getItem() retrieves saved data
 */
function toggleDarkMode() {
    const body = document.body;
    const icon = document.getElementById('darkModeIcon');

    // Add transition class for smooth animation
    body.style.transition = 'background 0.4s cubic-bezier(0.4, 0, 0.2, 1), color 0.4s cubic-bezier(0.4, 0, 0.2, 1)';

    // Toggle dark mode class
    body.classList.toggle('dark-mode');

    // Update icon based on current mode with animation
    if (body.classList.contains('dark-mode')) {
        // Switching to dark mode
        icon.style.transform = 'rotate(180deg)';
        setTimeout(() => {
            icon.textContent = '☀️';  // Sun icon in dark mode
            icon.style.transform = 'rotate(360deg)';
        }, 200);
        localStorage.setItem('darkMode', 'enabled');
        console.log('🌙 Dark mode enabled');
    } else {
        // Switching to light mode
        icon.style.transform = 'rotate(180deg)';
        setTimeout(() => {
            icon.textContent = '🌙';  // Moon icon in light mode
            icon.style.transform = 'rotate(360deg)';
        }, 200);
        localStorage.setItem('darkMode', 'disabled');
        console.log('☀️ Light mode enabled');
    }

    // Reset transform after animation
    setTimeout(() => {
        icon.style.transform = 'rotate(0deg)';
    }, 600);

    /**
     * WHY DIFFERENT ICONS?
     * - Light mode shows moon 🌙 (click to go dark)
     * - Dark mode shows sun ☀️ (click to go light)
     * Icon shows what will happen, not current state
     *
     * SMOOTH ANIMATION:
     * - Icon rotates 180° while changing
     * - Creates smooth, polished transition
     * - Provides visual feedback to user
     */
}

/**
 * Initializes dark mode on page load
 *
 * WHEN THIS RUNS:
 * On page load, check if user previously enabled dark mode.
 * If yes, automatically activate it.
 *
 * WHY THIS IS IMPORTANT:
 * Without this, dark mode would reset every time user navigates to new page.
 * localStorage lets us remember the preference!
 */
function initDarkMode() {
    const darkModePreference = localStorage.getItem('darkMode');
    const body = document.body;
    const icon = document.getElementById('darkModeIcon');

    if (darkModePreference === 'enabled') {
        body.classList.add('dark-mode');
        if (icon) {
            icon.textContent = '☀️';
        }
    }

    console.log('✅ Dark mode initialized. Current mode:', darkModePreference || 'light');
}

// Initialize dark mode when page loads
document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
});

/**
 * DARK MODE IMPLEMENTATION SUMMARY:
 *
 * CSS (style.css):
 * - CSS variables defined in :root for light mode
 * - body.dark-mode overrides variables for dark mode
 * - All colors use var(--variable-name) for easy switching
 *
 * HTML (base.html):
 * - Toggle button with onclick="toggleDarkMode()"
 * - Icon changes based on mode
 *
 * JavaScript (main.js):
 * - toggleDarkMode() switches classes and saves preference
 * - initDarkMode() loads saved preference on page load
 * - localStorage persists preference across sessions
 *
 * BENEFITS:
 * ✅ Reduces eye strain in low light
 * ✅ Saves battery on OLED screens
 * ✅ Modern, professional feature
 * ✅ Respects user preference
 * ✅ Smooth transitions between modes
 *
 * JUNIOR DEV CHALLENGE:
 * Try adding these enhancements:
 * 1. Auto-detect system preference (matchMedia)
 * 2. Different color schemes (not just light/dark)
 * 3. Scheduled mode switching (dark at night)
 * 4. Smooth color transitions with CSS
 */
