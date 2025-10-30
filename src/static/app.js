document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const faqList = document.getElementById("faq-list");
  const faqSearch = document.getElementById("faq-search");

  // FAQ data structure
  const faqData = [
    {
      category: "General Event Information",
      icon: "ℹ️",
      questions: [
        {
          question: "What are extracurricular activities?",
          answer: "Extracurricular activities are programs and experiences that take place outside of regular classroom instruction. They include clubs, sports teams, arts programs, and other organized activities that help students develop new skills, pursue interests, and build friendships."
        },
        {
          question: "When do activities take place?",
          answer: "Activities typically take place after school hours, usually between 3:00 PM and 6:00 PM on weekdays. Some activities may also meet during lunch periods or on weekends. Specific schedules are listed for each activity."
        },
        {
          question: "How long do activities run?",
          answer: "Most activities run for the entire school year, from September through May. However, some seasonal activities like sports teams may only run during specific seasons. Session lengths vary from 1 to 2 hours per meeting."
        },
        {
          question: "Are there any costs involved?",
          answer: "Most activities are free for all students. However, some activities may have minimal fees to cover materials, equipment, or competition entry fees. Any costs will be clearly communicated when you sign up."
        }
      ]
    },
    {
      category: "Types of Activities",
      icon: "🎯",
      questions: [
        {
          question: "What types of activities are available?",
          answer: "We offer a wide variety of activities including academic clubs (Math Club, Debate Team), sports teams (Soccer, Basketball), arts programs (Art Club, Drama Club), technology clubs (Programming Class), and traditional games (Chess Club). Check the activities list above for all current offerings."
        },
        {
          question: "Are there academic clubs?",
          answer: "Yes! We have several academic clubs including Math Club, Programming Class, Debate Team, and Chess Club. These clubs help students develop critical thinking, problem-solving, and communication skills."
        },
        {
          question: "What sports are offered?",
          answer: "We currently offer Soccer Team, Basketball Team, and Gym Class. Our sports programs focus on teamwork, physical fitness, and competitive skills. Teams compete in local school leagues throughout the year."
        },
        {
          question: "Are there arts and creative activities?",
          answer: "Absolutely! We have Art Club for visual arts (painting, drawing) and Drama Club for theater and performing arts. These programs encourage creative expression and help students develop artistic skills."
        },
        {
          question: "Can students suggest new activities?",
          answer: "Yes! We encourage student input. If you're interested in starting a new activity, please speak with the activities coordinator or email activities@mergington.edu with your proposal. We need at least 8 interested students and a faculty advisor to launch a new activity."
        }
      ]
    },
    {
      category: "Participation Requirements",
      icon: "✓",
      questions: [
        {
          question: "Who can participate in activities?",
          answer: "All currently enrolled Mergington High School students are eligible to participate in extracurricular activities. Students must maintain good academic standing and follow the school's code of conduct."
        },
        {
          question: "Are there grade level restrictions?",
          answer: "Most activities are open to all grade levels (9-12). However, some competitive teams may have tryouts or prerequisites. Check the specific activity description for any grade-level requirements."
        },
        {
          question: "What is the minimum/maximum number of participants?",
          answer: "Each activity has different capacity limits. Minimums are typically 8-10 students to maintain the activity, while maximums vary from 10 to 30 depending on the activity type, available space, and supervision requirements. Current availability is shown for each activity."
        },
        {
          question: "Can students join multiple activities?",
          answer: "Yes! Students are encouraged to explore multiple interests. However, please be mindful of time commitments and ensure you can attend all meetings. Some activities with conflicting schedules may be difficult to manage simultaneously."
        },
        {
          question: "What happens if an activity is full?",
          answer: "If an activity has reached maximum capacity, you can contact activities@mergington.edu to be placed on a waiting list. We'll notify you if a spot becomes available. We may also consider opening additional sections if there's sufficient demand."
        },
        {
          question: "How to withdraw from an activity?",
          answer: "If you need to withdraw from an activity, click the ❌ button next to your name in the participants list, or email activities@mergington.edu. Please provide at least one week's notice when possible so we can offer your spot to another student."
        }
      ]
    },
    {
      category: "Technical Support",
      icon: "🔧",
      questions: [
        {
          question: "How to sign up for activities?",
          answer: "To sign up, use the 'Sign Up for an Activity' form on this page. Enter your Mergington student email address (ending in @mergington.edu) and select the activity you want to join. You'll receive a confirmation message once you're successfully registered."
        },
        {
          question: "What if I can't access my email?",
          answer: "If you're having trouble accessing your school email, contact the IT help desk at helpdesk@mergington.edu or visit the computer lab for assistance. Your email is required for all activity communications and confirmations."
        },
        {
          question: "Browser compatibility issues",
          answer: "This website works best with modern browsers including Chrome, Firefox, Safari, and Edge. Make sure your browser is updated to the latest version. If you're experiencing issues, try clearing your browser cache or using a different browser."
        },
        {
          question: "Who to contact for technical problems?",
          answer: "For technical issues with the website or signup process, contact the IT help desk at helpdesk@mergington.edu. For questions about specific activities or availability, email activities@mergington.edu."
        }
      ]
    }
  ];

  // Function to render FAQ items
  function renderFAQ() {
    faqList.innerHTML = "";
    faqData.forEach((category) => {
      const categoryDiv = document.createElement("div");
      categoryDiv.className = "faq-category";
      
      const categoryTitle = document.createElement("div");
      categoryTitle.className = "faq-category-title";
      categoryTitle.innerHTML = `<span>${category.icon}</span><span>${category.category}</span>`;
      categoryDiv.appendChild(categoryTitle);

      category.questions.forEach((item, index) => {
        const faqItem = document.createElement("div");
        faqItem.className = "faq-item";
        faqItem.setAttribute("data-category", category.category);
        faqItem.setAttribute("data-question", item.question.toLowerCase());
        faqItem.setAttribute("data-answer", item.answer.toLowerCase());

        // Sanitize category name for use in IDs (replace spaces and special chars with hyphens)
        const categoryId = category.category.toLowerCase().replace(/[^a-z0-9]+/g, '-');

        const question = document.createElement("div");
        question.className = "faq-question";
        question.setAttribute("tabindex", "0");
        question.setAttribute("role", "button");
        question.setAttribute("aria-expanded", "false");
        question.setAttribute("aria-controls", `faq-answer-${categoryId}-${index}`);
        question.innerHTML = `
          <span>${item.question}</span>
          <span class="faq-icon">▼</span>
        `;

        const answer = document.createElement("div");
        answer.className = "faq-answer";
        answer.id = `faq-answer-${categoryId}-${index}`;
        answer.setAttribute("role", "region");
        answer.innerHTML = `<p>${item.answer}</p>`;

        faqItem.appendChild(question);
        faqItem.appendChild(answer);
        categoryDiv.appendChild(faqItem);

        // Add click event to toggle answer
        question.addEventListener("click", () => toggleFAQ(faqItem, question));
        
        // Add keyboard support (Enter and Space keys)
        question.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggleFAQ(faqItem, question);
          }
        });
      });

      faqList.appendChild(categoryDiv);
    });
  }

  // Function to toggle FAQ item
  function toggleFAQ(item, question) {
    const isActive = item.classList.contains("active");
    item.classList.toggle("active");
    question.setAttribute("aria-expanded", !isActive);
  }

  // Function to filter FAQ items based on search
  function filterFAQ() {
    const searchTerm = faqSearch.value.toLowerCase().trim();
    const allItems = document.querySelectorAll(".faq-item");
    const categories = document.querySelectorAll(".faq-category");
    let visibleCount = 0;

    if (searchTerm === "") {
      allItems.forEach((item) => {
        item.classList.remove("hidden");
      });
      categories.forEach((cat) => {
        cat.style.display = "block";
      });
      // Remove any existing no-results message
      const noResults = document.querySelector(".no-results");
      if (noResults) noResults.remove();
      return;
    }

    allItems.forEach((item) => {
      const question = item.getAttribute("data-question");
      const answer = item.getAttribute("data-answer");
      
      if (question.includes(searchTerm) || answer.includes(searchTerm)) {
        item.classList.remove("hidden");
        visibleCount++;
      } else {
        item.classList.add("hidden");
      }
    });

    // Hide categories with no visible items
    categories.forEach((category) => {
      const visibleItems = category.querySelectorAll(".faq-item:not(.hidden)");
      if (visibleItems.length === 0) {
        category.style.display = "none";
      } else {
        category.style.display = "block";
      }
    });

    // Show "no results" message if no items match
    const noResults = document.querySelector(".no-results");
    if (visibleCount === 0) {
      if (!noResults) {
        const noResultsDiv = document.createElement("div");
        noResultsDiv.className = "no-results";
        noResultsDiv.textContent = `No FAQ items found matching "${searchTerm}"`;
        faqList.appendChild(noResultsDiv);
      }
    } else {
      if (noResults) noResults.remove();
    }
  }

  // Add event listener for FAQ search
  faqSearch.addEventListener("input", filterFAQ);

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

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

  // Initialize app
  fetchActivities();
  renderFAQ();
});
