// CSRF utilities
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Light toast
function toast(msg, ok=true){
  const t = document.createElement('div');
  t.textContent = msg;
  t.style.cssText = `position:fixed;right:16px;bottom:16px;padding:10px 14px;border-radius:10px;color:#fff;z-index:9999;box-shadow:0 8px 20px rgba(0,0,0,.25);background:${ok?'#059669':'#dc2626'}`;
  document.body.appendChild(t);
  setTimeout(()=>{ t.remove(); }, 2500);
}

// AJAX proposal submit
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('proposalForm');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCookie('csrftoken') },
        body: data,
      });
      const json = await res.json();
      if (json.ok) {
        toast('Proposal sent');
        setTimeout(()=>{ location.reload(); }, 700);
      } else {
        toast('Error: ' + (json.errors || 'Failed'), false);
      }
    } catch(err) {
      toast('Network error', false);
    }
  });
});


