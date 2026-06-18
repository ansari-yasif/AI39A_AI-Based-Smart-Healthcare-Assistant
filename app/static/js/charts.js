/* charts.js — Chart.js initializers | Feature: Dashboard charts */

// Figma exact chart colours
if (!Chart.defaults.color) {
  Chart.defaults.color           = '#94a3b8';
  Chart.defaults.font.family     = "'Inter', sans-serif";
  Chart.defaults.font.size       = 12;
  Chart.defaults.plugins.legend.display = false;
}

// Define chart constants (use let to avoid const redeclaration errors on hot reload)
if (typeof TEAL === 'undefined') {
  window.TEAL   = '#00C897';
  window.ORANGE = '#f97316';
  window.BLUE   = '#4A9EFF';
  window.GRID   = 'rgba(255,255,255,0.05)';
}


/**
 * Sleep bar chart — teal/blue/red bars by quality threshold
 */
function initSleepChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx || !labels.length) return;

  new Chart(ctx, {
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
          h >= 7 ? window.TEAL : h >= 5 ? '#F59E0B' : '#EF4444'
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
        x: { grid:{ color:window.GRID }, border:{ display:false } },
        y: { grid:{ color:window.GRID }, border:{ display:false },
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
 * Calorie line chart — teal gradient fill
 */
function initCalChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx || !labels.length) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data,
        borderColor:          window.TEAL,
        backgroundColor:      'rgba(0,200,151,.08)',
        borderWidth:          2.5,
        pointBackgroundColor: window.TEAL,
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
        x: { grid:{ color:window.GRID }, border:{ display:false } },
        y: { grid:{ color:window.GRID }, border:{ display:false },
             title:{ display:true, text:'kcal', color:'#475569' },
        },
      },
      plugins: {
        tooltip: { callbacks: { label: c => ` ${c.parsed.y} kcal` } },
      },
    },
  });
}


/**
 * Expense doughnut — for expense page if added
 */
function initExpenseChart(id, labels, data) {
  const ctx = document.getElementById(id);
  if (!ctx || !data.length) return;

  const COLORS = [window.TEAL, window.ORANGE, window.BLUE, '#8B5CF6', '#10b981', '#F59E0B', '#EC4899'];

  new Chart(ctx, {
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