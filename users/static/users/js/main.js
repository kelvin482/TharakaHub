// users/static/users/js/main.js
// Site-wide JavaScript for TharakaHub

/* Small safe initializer - keep minimal to avoid conflicts with page scripts */
document.addEventListener('DOMContentLoaded', function () {
  try {
    // simple indicator to confirm the file loaded
    // (useful during local testing; remove console.log in production)
    console.log('TharakaHub main.js loaded');

    // Example: make footer social links open in a new tab (already added server-side)
    // Provide safe event delegation for future enhancements
    document.querySelectorAll('.social-link').forEach(function(el){
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener noreferrer');
    });

    // Expose a small namespace for page scripts to use without polluting global scope
    window.TharakaHub = window.TharakaHub || {};
    window.TharakaHub.helpers = window.TharakaHub.helpers || {};

  } catch (err) {
    // swallow errors to avoid breaking page-specific scripts
    console.warn('TharakaHub main.js init error', err);
  }
});
