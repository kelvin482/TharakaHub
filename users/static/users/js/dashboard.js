document.addEventListener('DOMContentLoaded', function () {
  console.log('Dashboard JS loaded ✅');

  // Initialize chart (Chart.js)
  const ctx = document.getElementById('earningsChart');
  if (ctx) {
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Monthly Earnings (Ksh)',
          data: [12000, 18000, 16000, 22000, 25000, 30000],
          borderColor: '#0077ff',
          backgroundColor: 'rgba(0,119,255,0.1)',
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  // Animate project progress bars
  document.querySelectorAll('.proj-progress-fill').forEach((bar) => {
    const progress = bar.getAttribute('data-progress');
    bar.style.width = progress + '%';
  });
});
