/* charts.js — Chart.js initializers | Feature: Dashboard charts */

Chart.defaults.color           = '#94a3b8';
Chart.defaults.font.family     = "'Inter', sans-serif";
Chart.defaults.font.size       = 12;
Chart.defaults.plugins.legend.display = false;

const TEAL   = '#00C897';
const ORANGE = '#f97316';
const BLUE   = '#4A9EFF';
const GRID   = 'rgba(255,255,255,0.05)';

// Registry to avoid duplicate chart instances
const _chartRegistry = {};
function _destroyChart(id) {
  if (_chartRegistry[id]) {
    _chartRegistry[id].destroy();
    delete _chartRegistry[id];
  }
}

/**
 * Sleep bar chart
 */
function initSleepChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx || !labels.length) return;
  _destroyChart(id);
  _chartRegistry[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: data.map(h =>
          h >= 7 ? 'rgba(0,200,151,.75)' :
          h >= 5 ? 'rgba(245,158,11,.75)' : 'rgba(239,68,68,.75)'
        ),
        borderColor: data.map(h =>
          h >= 7 ? TEAL : h >= 5 ? '#F59E0B' : '#EF4444'
        ),
        borderWidth:  1.5,
        borderRadius: 6,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid:{ color:GRID }, border:{ display:false } },
        y: { grid:{ color:GRID }, border:{ display:false },
             min:0, max:12,
             ticks: { stepSize:2 },
             title:{ display:true, text:'Hours', color:'#475569' },
        },
      },
      plugins: {
        tooltip: { callbacks: { label: c => ` ${c.parsed.y}h sleep` } },
      },
    },
  });
}

/**
 * Calorie line chart — teal gradient fill, fixed height container
 */
function initCalChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  _destroyChart(id);

  // Ensure canvas has proper dimensions
  ctx.style.maxHeight = '220px';

  _chartRegistry[id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data,
        borderColor:          TEAL,
        backgroundColor:      'rgba(0,200,151,.08)',
        borderWidth:          2.5,
        pointBackgroundColor: TEAL,
        pointBorderColor:     '#0a0e1a',
        pointBorderWidth:     2,
        pointRadius:          5,
        fill:    true,
        tension: 0.4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid:{ color:GRID }, border:{ display:false } },
        y: { grid:{ color:GRID }, border:{ display:false },
             beginAtZero: true,
             title:{ display:true, text:'kcal', color:'#475569' },
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: c => ` ${c.parsed.y} kcal` } },
      },
    },
  });
}

/**
 * Macro doughnut chart — fixed to avoid glitch when no data
 */
function initMacroChart(id, protein, carbs, fat) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  _destroyChart(id);

  const total = protein + carbs + fat;
  if (total <= 0) {
    // Show placeholder text instead of blank chart
    const parent = ctx.parentElement;
    ctx.style.display = 'none';
    if (!parent.querySelector('.macro-empty-msg')) {
      const msg = document.createElement('p');
      msg.className = 'macro-empty-msg';
      msg.style.cssText = 'color:#555;text-align:center;padding:40px 0;font-size:.85rem';
      msg.textContent = 'Log meals to see macro breakdown';
      parent.appendChild(msg);
    }
    return;
  }

  _chartRegistry[id] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Protein', 'Carbs', 'Fat'],
      datasets: [{
        data: [protein, carbs, fat],
        backgroundColor: ['#3b82f6', '#00C897', '#f97316'],
        borderColor:     ['#1e40af', '#00a67e', '#c2410c'],
        borderWidth: 2,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '62%',
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            color: '#aaa',
            font: { size: 12 },
            padding: 12,
            usePointStyle: true,
          }
        },
        tooltip: {
          callbacks: {
            label: c => ` ${c.label}: ${c.parsed}g (${Math.round(c.parsed/total*100)}%)`
          }
        }
      }
    },
  });
}

/**
 * Expense doughnut
 */
function initExpenseChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx || !data.length) return;
  _destroyChart(id);

  const COLORS = [TEAL, ORANGE, BLUE, '#8B5CF6', '#10b981', '#F59E0B', '#EC4899'];

  _chartRegistry[id] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: COLORS.slice(0, data.length).map(c => c + 'CC'),
        borderColor:     COLORS.slice(0, data.length),
        borderWidth: 1.5,
        hoverOffset: 8,
      }],
    },
    options: {
      responsive: true,
      cutout: '68%',
      plugins: {
        legend: {
          display:  true,
          position: 'bottom',
          labels:   { padding:16, usePointStyle:true, pointStyleWidth:10, color:'#94a3b8' },
        },
        tooltip: { callbacks: { label: c => ` NPR ${c.parsed.toLocaleString()}` } },
      },
    },
  });
}
