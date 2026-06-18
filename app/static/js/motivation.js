/* motivation.js — Daily Motivation Generator | rotates every 2 minutes */

const MOTIVATION_QUOTES = [
  { text: "No Pain, No Gain", author: "Stay consistent, stay strong" },
  { text: "Your body can stand almost anything. It's your mind you have to convince.", author: "Mindset matters" },
  { text: "The only bad workout is the one that didn't happen.", author: "Just show up" },
  { text: "Health is not about the weight you lose, but the life you gain.", author: "Focus on the journey" },
  { text: "Small steps every day lead to big results.", author: "Consistency wins" },
  { text: "Take care of your body. It's the only place you have to live.", author: "Jim Rohn" },
  { text: "Discipline is choosing between what you want now and what you want most.", author: "Long-term thinking" },
  { text: "A healthy outside starts from the inside.", author: "Nourish yourself" },
  { text: "Don't count the days, make the days count.", author: "Muhammad Ali" },
  { text: "Strive for progress, not perfection.", author: "Every step counts" },
  { text: "The groundwork for all happiness is good health.", author: "Leigh Hunt" },
  { text: "Eat well, move daily, sleep enough, repeat.", author: "Simple habits, big impact" },
  { text: "You don't have to be extreme, just consistent.", author: "Build the habit" },
  { text: "Every workout counts, no matter how small.", author: "Keep moving" },
  { text: "Your future self will thank you for the choices you make today.", author: "Invest in you" },
  { text: "Rest is not idleness — recovery is part of the plan.", author: "Sleep well" },
  { text: "Hydrate, move, breathe, repeat.", author: "Daily basics" },
  { text: "Wellness is a journey, not a destination.", author: "Enjoy the process" },
  { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
  { text: "The food you eat can either be the safest and most powerful form of medicine, or the slowest form of poison.", author: "Ann Wigmore" },
];

function initMotivationGenerator(elIds) {
  // elIds: array of { text: selector, author: selector } for each display location
  function pickAndRender() {
    const idx = Math.floor(Math.random() * MOTIVATION_QUOTES.length);
    const q = MOTIVATION_QUOTES[idx];
    elIds.forEach(set => {
      const textEl = document.querySelector(set.text);
      const authEl = document.querySelector(set.author);
      if (textEl) textEl.textContent = `"${q.text}"`;
      if (authEl) authEl.textContent = q.author;
    });
  }
  pickAndRender();
  // Rotate every 2 minutes (120000 ms)
  setInterval(pickAndRender, 2 * 60 * 1000);
}
