document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const userEmailInput = document.getElementById("user-email");
  const checkRoleBtn = document.getElementById("check-role-btn");
  const userRoleSpan = document.getElementById("user-role");
  const adminContainer = document.getElementById("admin-container");
  const notificationsList = document.getElementById("notifications-list");

  let currentUserEmail = "";
  let isAdmin = false;

  // User role management
  checkRoleBtn.addEventListener("click", () => {
    currentUserEmail = userEmailInput.value;
    updateUserRole();
  });

  function updateUserRole() {
    const adminEmails = ["admin@mergington.edu", "teacher@mergington.edu"];
    isAdmin = adminEmails.includes(currentUserEmail);
    
    if (isAdmin) {
      userRoleSpan.textContent = "👤 Admin/Teacher";
      adminContainer.classList.remove("hidden");
    } else {
      userRoleSpan.textContent = "👤 Student";
      adminContainer.classList.add("hidden");
    }
    
    // Refresh data
    fetchActivities();
    fetchNotifications();
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      
      // Clear and repopulate select dropdowns
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';
      const attendanceActivitySelect = document.getElementById("attendance-activity");
      if (attendanceActivitySelect) {
        attendanceActivitySelect.innerHTML = '<option value="">-- Select activity --</option>';
      }

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft =
          details.max_participants - details.participants.length;

        // Create participants HTML with delete icons instead of bullet points
        const participantsHTML =
          details.participants.length > 0
            ? `<div class="participants-section">
              <h5>Participants:</h5>
              <ul class="participants-list">
                ${details.participants
                  .map(
                    (email) =>
                      `<li><span class="participant-email">${email}</span><button class="delete-btn" data-activity="${name}" data-email="${email}">❌</button></li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No participants yet</em></p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-container">
            ${participantsHTML}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
        
        // Add to attendance dropdown if admin
        if (attendanceActivitySelect) {
          const attOption = document.createElement("option");
          attOption.value = name;
          attOption.textContent = name;
          attendanceActivitySelect.appendChild(attOption);
        }
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      activitiesList.innerHTML =
        "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const activity = button.getAttribute("data-activity");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";

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
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/signup?email=${encodeURIComponent(email)}`,
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

  // Fetch and display notifications
  async function fetchNotifications() {
    try {
      const url = currentUserEmail 
        ? `/notifications?user_email=${encodeURIComponent(currentUserEmail)}`
        : '/notifications';
      const response = await fetch(url);
      const notifications = await response.json();

      notificationsList.innerHTML = "";

      if (notifications.length === 0) {
        notificationsList.innerHTML = "<p><em>No notifications</em></p>";
      } else {
        notifications.slice(-5).reverse().forEach((notif) => {
          const notifDiv = document.createElement("div");
          notifDiv.className = "notification-item";
          const timestamp = new Date(notif.timestamp).toLocaleString();
          notifDiv.innerHTML = `
            <div>${notif.message}</div>
            <div class="timestamp">${timestamp}</div>
          `;
          notificationsList.appendChild(notifDiv);
        });
      }
    } catch (error) {
      console.error("Error fetching notifications:", error);
      notificationsList.innerHTML = "<p>Failed to load notifications</p>";
    }
  }

  // Admin: Create Activity Form
  const createActivityForm = document.getElementById("create-activity-form");
  if (createActivityForm) {
    createActivityForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      
      const name = document.getElementById("new-activity-name").value;
      const description = document.getElementById("new-activity-desc").value;
      const schedule = document.getElementById("new-activity-schedule").value;
      const maxParticipants = parseInt(document.getElementById("new-activity-max").value);
      
      try {
        const response = await fetch(
          `/admin/activities?activity_name=${encodeURIComponent(name)}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-User-Email": currentUserEmail
            },
            body: JSON.stringify({
              description,
              schedule,
              max_participants: maxParticipants
            })
          }
        );
        
        const result = await response.json();
        const adminMessage = document.getElementById("admin-message");
        
        if (response.ok) {
          adminMessage.textContent = result.message;
          adminMessage.className = "message success";
          createActivityForm.reset();
          fetchActivities();
          fetchNotifications();
        } else {
          adminMessage.textContent = result.detail || "Failed to create activity";
          adminMessage.className = "message error";
        }
        
        adminMessage.classList.remove("hidden");
        setTimeout(() => adminMessage.classList.add("hidden"), 5000);
      } catch (error) {
        console.error("Error creating activity:", error);
      }
    });
  }

  // Admin: Mark Attendance Form
  const attendanceForm = document.getElementById("attendance-form");
  if (attendanceForm) {
    attendanceForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      
      const activity = document.getElementById("attendance-activity").value;
      const email = document.getElementById("attendance-email").value;
      const date = document.getElementById("attendance-date").value;
      const attended = document.getElementById("attendance-present").checked;
      
      try {
        const response = await fetch(
          `/admin/activities/${encodeURIComponent(activity)}/attendance`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-User-Email": currentUserEmail
            },
            body: JSON.stringify({ email, attended, date })
          }
        );
        
        const result = await response.json();
        const adminMessage = document.getElementById("admin-message");
        
        if (response.ok) {
          adminMessage.textContent = result.message;
          adminMessage.className = "message success";
          attendanceForm.reset();
          // Set today's date as default
          document.getElementById("attendance-date").valueAsDate = new Date();
        } else {
          adminMessage.textContent = result.detail || "Failed to mark attendance";
          adminMessage.className = "message error";
        }
        
        adminMessage.classList.remove("hidden");
        setTimeout(() => adminMessage.classList.add("hidden"), 5000);
      } catch (error) {
        console.error("Error marking attendance:", error);
      }
    });
  }

  // Admin: View Activities Report
  const viewActivitiesReportBtn = document.getElementById("view-activities-report-btn");
  if (viewActivitiesReportBtn) {
    viewActivitiesReportBtn.addEventListener("click", async () => {
      try {
        const response = await fetch("/admin/reports/activities", {
          headers: { "X-User-Email": currentUserEmail }
        });
        const report = await response.json();
        
        displayActivitiesReport(report);
      } catch (error) {
        console.error("Error fetching report:", error);
      }
    });
  }

  function displayActivitiesReport(report) {
    const reportsContainer = document.getElementById("reports-container");
    const reportsContent = document.getElementById("reports-content");
    
    reportsContainer.classList.remove("hidden");
    
    let html = `
      <div class="report-summary">
        <h4>Activities Summary</h4>
        <p><strong>Total Activities:</strong> ${report.total_activities}</p>
        <p><strong>Generated:</strong> ${new Date(report.generated_at).toLocaleString()}</p>
      </div>
      <table class="report-table">
        <thead>
          <tr>
            <th>Activity</th>
            <th>Current</th>
            <th>Max</th>
            <th>Available</th>
            <th>Attendance Records</th>
          </tr>
        </thead>
        <tbody>
    `;
    
    report.activities.forEach(activity => {
      html += `
        <tr>
          <td>${activity.activity_name}</td>
          <td>${activity.current_participants}</td>
          <td>${activity.max_participants}</td>
          <td>${activity.available_spots}</td>
          <td>${activity.attendance_records}</td>
        </tr>
      `;
    });
    
    html += `
        </tbody>
      </table>
    `;
    
    reportsContent.innerHTML = html;
  }

  // Admin: View Attendance Report
  const viewAttendanceReportBtn = document.getElementById("view-attendance-report-btn");
  if (viewAttendanceReportBtn) {
    viewAttendanceReportBtn.addEventListener("click", async () => {
      // For simplicity, show attendance for first activity
      const activities = await (await fetch("/activities")).json();
      const firstActivity = Object.keys(activities)[0];
      
      if (!firstActivity) {
        alert("No activities available");
        return;
      }
      
      try {
        const response = await fetch(
          `/admin/reports/attendance/${encodeURIComponent(firstActivity)}`,
          { headers: { "X-User-Email": currentUserEmail } }
        );
        const report = await response.json();
        
        displayAttendanceReport(report);
      } catch (error) {
        console.error("Error fetching attendance report:", error);
      }
    });
  }

  function displayAttendanceReport(report) {
    const reportsContainer = document.getElementById("reports-container");
    const reportsContent = document.getElementById("reports-content");
    
    reportsContainer.classList.remove("hidden");
    
    let html = `
      <div class="report-summary">
        <h4>Attendance Report: ${report.activity_name}</h4>
        <p><strong>Total Records:</strong> ${report.total_records}</p>
        <p><strong>Attended:</strong> ${report.attended_count}</p>
        <p><strong>Absent:</strong> ${report.absence_count}</p>
        <p><strong>Attendance Rate:</strong> ${report.attendance_rate.toFixed(1)}%</p>
        <p><strong>Generated:</strong> ${new Date(report.generated_at).toLocaleString()}</p>
      </div>
    `;
    
    if (report.records.length > 0) {
      html += `
        <table class="report-table">
          <thead>
            <tr>
              <th>Email</th>
              <th>Date</th>
              <th>Status</th>
              <th>Marked By</th>
            </tr>
          </thead>
          <tbody>
      `;
      
      report.records.forEach(record => {
        html += `
          <tr>
            <td>${record.email}</td>
            <td>${record.date}</td>
            <td>${record.attended ? '✓ Present' : '✗ Absent'}</td>
            <td>${record.marked_by}</td>
          </tr>
        `;
      });
      
      html += `
          </tbody>
        </table>
      `;
    } else {
      html += `<p><em>No attendance records yet</em></p>`;
    }
    
    reportsContent.innerHTML = html;
  }

  // Initialize app
  updateUserRole();
  fetchActivities();
  fetchNotifications();
  
  // Set today's date as default for attendance
  const attendanceDateInput = document.getElementById("attendance-date");
  if (attendanceDateInput) {
    attendanceDateInput.valueAsDate = new Date();
  }
  
  // Refresh notifications every 30 seconds
  setInterval(fetchNotifications, 30000);
});
