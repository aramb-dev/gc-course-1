 document.addEventListener("DOMContentLoaded", () => {
 console.log("DOM loaded, starting app initialization...");

  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    await fetchActivitiesAndPopulate();
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});

// Global function to remove participant (accessible from onclick)
async function removeParticipant(activityName, email) {
  try {
    const response = await fetch(
      `/activities/${encodeURIComponent(activityName)}/participant/${encodeURIComponent(email)}`,
      {
        method: "DELETE",
      }
    );

    const result = await response.json();

    if (response.ok) {
      // Show success message
      const messageDiv = document.getElementById("message");
      messageDiv.textContent = result.message;
      messageDiv.className = "success";
      messageDiv.classList.remove("hidden");

      // Refresh activities list to show updated participants
      const activitiesList = document.getElementById("activities-list");
      const activitySelect = document.getElementById("activity");

      // Re-fetch and display activities
      fetchActivitiesAndPopulate();

      // Hide message after 3 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 3000);
    } else {
      // Show error message
      const messageDiv = document.getElementById("message");
      messageDiv.textContent = result.detail || "Failed to remove participant";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
    }
  } catch (error) {
    console.error("Error removing participant:", error);
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = "Failed to remove participant. Please try again.";
    messageDiv.className = "error";
    messageDiv.classList.remove("hidden");
  }
}

// Helper function to fetch and populate activities (used by removeParticipant)
async function fetchActivitiesAndPopulate() {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");

  try {
    const response = await fetch("/activities");
    const activities = await response.json();

    // Clear existing content
    activitiesList.innerHTML = "";
    // Clear select options except the first one
    activitySelect.innerHTML = '<option value="">Select an activity</option>';

    // Populate activities list
    Object.entries(activities).forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;

      // Create participants list
      let participantsList = '';
      if (details.participants && details.participants.length > 0) {
        participantsList = `<div class="participants-list">${details.participants.map(email =>
          `<div class="participant-item">
            <span class="participant-email">${email}</span>
            <button class="delete-btn" onclick="removeParticipant('${name}', '${email}')" title="Remove participant">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>`
        ).join('')}</div>`;
      } else {
        participantsList = `<p class="no-participants">No participants yet</p>`;
      }

      activityCard.innerHTML = `
        <h4>${name}</h4>
        <p>${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        <div class="participants-section">
          <p><strong>Participants:</strong></p>
          ${participantsList}
        </div>
      `;

      activitiesList.appendChild(activityCard);

      // Add option to select dropdown
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      activitySelect.appendChild(option);
    });
  } catch (error) {
    activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
    console.error("Error fetching activities:", error);
  }
}
