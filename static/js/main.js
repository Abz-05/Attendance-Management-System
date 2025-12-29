// Common JavaScript functions for Attendance Management System

// Show message function
function showMessage(message, type = "info") {
  const messageDiv = document.getElementById("message");
  messageDiv.className = `message show ${type}`;
  messageDiv.textContent = message;

  // Auto-hide after 5 seconds
  setTimeout(() => {
    messageDiv.classList.remove("show");
  }, 5000);
}

// Format date to YYYY-MM-DD
function formatDate(date) {
  if (typeof date === "string") {
    return date;
  }
  const d = new Date(date);
  const month = "" + (d.getMonth() + 1);
  const day = "" + d.getDate();
  const year = d.getFullYear();

  return [year, month.padStart(2, "0"), day.padStart(2, "0")].join("-");
}

// Remove message when user starts typing
document.addEventListener("DOMContentLoaded", function () {
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach((input) => {
    input.addEventListener("input", () => {
      const messageDiv = document.getElementById("message");
      if (messageDiv && messageDiv.classList.contains("error")) {
        messageDiv.classList.remove("show");
      }
    });
  });
});
