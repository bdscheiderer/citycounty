// Countdown to the next Missouri General Assembly session start or end,
// adapted from countdown.s2legacy.com. When a date passes, the countdown
// moves on to the next entry; it hides itself once the list runs out.
const phases = [
  { date: "2026-05-15T18:00:00-05:00", label: "103rd General Assembly session ends",  when: "Friday, May 15, 2026, 6 PM CDT" },
  { date: "2027-01-06T12:00:00-06:00", label: "104th General Assembly convenes",      when: "Wednesday, January 6, 2027, 12 PM CST" },
  { date: "2027-05-14T18:00:00-05:00", label: "104th General Assembly session ends",  when: "Friday, May 14, 2027, 6 PM CDT" },
  { date: "2028-01-05T12:00:00-06:00", label: "105th General Assembly convenes",      when: "Wednesday, January 5, 2028, 12 PM CST" },
  { date: "2028-05-12T18:00:00-05:00", label: "105th General Assembly session ends",  when: "Friday, May 12, 2028, 6 PM CDT" },
  { date: "2029-01-03T12:00:00-06:00", label: "106th General Assembly convenes",      when: "Wednesday, January 3, 2029, 12 PM CST" },
  { date: "2029-05-18T18:00:00-05:00", label: "106th General Assembly session ends",  when: "Friday, May 18, 2029, 6 PM CDT" },
  { date: "2030-01-09T12:00:00-06:00", label: "107th General Assembly convenes",      when: "Wednesday, January 9, 2030, 12 PM CST" },
  { date: "2030-05-17T18:00:00-05:00", label: "107th General Assembly session ends",  when: "Friday, May 17, 2030, 6 PM CDT" },
  { date: "2031-01-08T12:00:00-06:00", label: "108th General Assembly convenes",      when: "Wednesday, January 8, 2031, 12 PM CST" },
  { date: "2031-05-16T18:00:00-05:00", label: "108th General Assembly session ends",  when: "Friday, May 16, 2031, 6 PM CDT" },
];

const countdownEl = document.getElementById("session-countdown");

function updateCountdown() {
  const now = new Date();
  const phase = phases.find(p => new Date(p.date) > now);

  // no upcoming dates left: hide the countdown
  if (!phase) {
    countdownEl.hidden = true;
    return;
  }

  const diff = new Date(phase.date) - now;
  const days    = Math.floor(diff / 86400000);
  const hours   = String(Math.floor(diff / 3600000) % 24).padStart(2, "0");
  const minutes = String(Math.floor(diff / 60000) % 60).padStart(2, "0");
  const seconds = String(Math.floor(diff / 1000) % 60).padStart(2, "0");

  countdownEl.textContent = `🏛️ ${phase.label} in ${days}d ${hours}h ${minutes}m ${seconds}s`;
  countdownEl.title = phase.when;
  countdownEl.hidden = false;
}

if (countdownEl) {
  updateCountdown();
  setInterval(updateCountdown, 1000);
}
