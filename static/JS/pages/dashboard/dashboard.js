// Dashboard Page Interactions

document.addEventListener('DOMContentLoaded', function() {
  const dashboardPage = document.querySelector('[data-dashboard]');
  
  if (!dashboardPage) return;

  // Initialize dashboard features
  initSearch();
  initTeamCards();
  initActivityItems();
});

/**
 * Initialize search functionality
 */
function initSearch() {
  const searchInput = document.querySelector('[data-dashboard-search]');
  
  if (!searchInput) return;

  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase();
    
    // TODO: Implement search filtering
    console.log('Search query:', query);
  });

  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      // Redirect to teams search with query
      const query = e.target.value;
      if (query.trim()) {
        window.location.href = `/teams/?search=${encodeURIComponent(query)}`;
      }
    }
  });
}

/**
 * Initialize team card interactions
 */
function initTeamCards() {
  const teamCards = document.querySelectorAll('.dashboard-team-card');
  
  teamCards.forEach(card => {
    card.addEventListener('click', function() {
      const teamId = this.getAttribute('data-team-id');
      if (teamId) {
        // Navigate to team profile (assumes URL pattern exists)
        window.location.href = `/teams/${teamId}/`;
      }
    });

    // Add keyboard navigation
    card.setAttribute('tabindex', '0');
    card.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });
}

/**
 * Initialize activity items
 */
function initActivityItems() {
  const activityItems = document.querySelectorAll('.dashboard-activity-item');
  
  activityItems.forEach(item => {
    // Add subtle animation on load
    item.style.animation = 'fadeInUp 0.4s ease forwards';
  });
}

// Add animation styles dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);
