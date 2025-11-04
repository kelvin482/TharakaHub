// copied from users/static/users/js/main.js
document.addEventListener('DOMContentLoaded', function () {
  try {
    console.log('TharakaHub main.js loaded');
    document.querySelectorAll('.social-link').forEach(function(el){
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener noreferrer');
    });
    window.TharakaHub = window.TharakaHub || {};
    window.TharakaHub.helpers = window.TharakaHub.helpers || {};
  } catch (err) {
    console.warn('TharakaHub main.js init error', err);
  }
});


