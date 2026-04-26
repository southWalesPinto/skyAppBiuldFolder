
(function () {
  function setupDirectorySearch() {
    var directory = document.querySelector('[data-team-directory]');
    if (!directory) {
      return;
    }

    var searchInput = directory.querySelector('[data-team-directory-search]');
    var cards = Array.prototype.slice.call(directory.querySelectorAll('[data-team-card]'));
    var grid = directory.querySelector('[data-team-directory-grid]');
    var viewButtons = Array.prototype.slice.call(directory.querySelectorAll('[data-directory-view]'));

    if (searchInput && cards.length) {
      searchInput.addEventListener('input', function () {
        var query = searchInput.value.trim().toLowerCase();

        cards.forEach(function (card) {
          var haystack = (card.getAttribute('data-team-card-search') || '').toLowerCase();
          card.style.display = !query || haystack.indexOf(query) !== -1 ? '' : 'none';
        });
      });
    }

    if (grid && viewButtons.length) {
      viewButtons.forEach(function (button) {
        button.addEventListener('click', function () {
          var layout = button.getAttribute('data-directory-view');
          grid.classList.toggle('is-list', layout === 'list');
          viewButtons.forEach(function (item) {
            item.classList.toggle('is-active', item === button);
          });
        });
      });
    }
  }

  function setupTeamTabs() {
    var profile = document.querySelector('[data-team-profile]');
    if (!profile) {
      return;
    }

    var tabButtons = Array.prototype.slice.call(profile.querySelectorAll('[data-team-tab-button]'));
    var tabPanels = Array.prototype.slice.call(profile.querySelectorAll('[data-team-tab-panel]'));

    function showTab(name) {
      tabButtons.forEach(function (button) {
        var isActive = button.getAttribute('data-team-tab-button') === name;
        button.classList.toggle('is-active', isActive);
      });

      tabPanels.forEach(function (panel) {
        var isActive = panel.getAttribute('data-team-tab-panel') === name;
        panel.classList.toggle('is-active', isActive);
      });
    }

    tabButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        showTab(button.getAttribute('data-team-tab-button'));
      });
    });

    var defaultTab = tabButtons.find(function (button) {
      return button.classList.contains('is-active');
    });
    showTab((defaultTab && defaultTab.getAttribute('data-team-tab-button')) || 'overview');
  }

  function setupMemberFilters() {
    var profile = document.querySelector('[data-team-profile]');
    if (!profile) {
      return;
    }

    var roleButtons = Array.prototype.slice.call(profile.querySelectorAll('[data-member-filter]'));
    var memberSearch = profile.querySelector('[data-member-search]');
    var memberCards = Array.prototype.slice.call(profile.querySelectorAll('[data-member-card]'));

    function applyMemberFilters() {
      var activeRoleButton = roleButtons.find(function (button) {
        return button.classList.contains('is-active');
      });
      var activeRole = activeRoleButton ? activeRoleButton.getAttribute('data-member-filter') : 'all';
      var query = memberSearch ? memberSearch.value.trim().toLowerCase() : '';

      memberCards.forEach(function (card) {
        var role = (card.getAttribute('data-member-role') || '').toLowerCase();
        var haystack = (card.getAttribute('data-member-search') || '').toLowerCase();
        var roleMatch = activeRole === 'all' || role.indexOf(activeRole) !== -1;
        var queryMatch = !query || haystack.indexOf(query) !== -1;
        card.style.display = roleMatch && queryMatch ? '' : 'none';
      });
    }

    roleButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        roleButtons.forEach(function (item) {
          item.classList.toggle('is-active', item === button);
        });
        applyMemberFilters();
      });
    });

    if (memberSearch) {
      memberSearch.addEventListener('input', applyMemberFilters);
    }
  }

  function setupRepositoryView() {
    var profile = document.querySelector('[data-team-profile]');
    if (!profile) {
      return;
    }

    var grid = profile.querySelector('[data-repository-grid]');
    var buttons = Array.prototype.slice.call(profile.querySelectorAll('[data-repository-view]'));

    if (!grid || !buttons.length) {
      return;
    }

    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        var layout = button.getAttribute('data-repository-view');
        grid.classList.toggle('is-list', layout === 'list');
        grid.classList.toggle('is-grid', layout !== 'list');
        buttons.forEach(function (item) {
          item.classList.toggle('is-active', item === button);
        });
      });
    });
  }

  function setupRepositorySearch() {
    var profile = document.querySelector('[data-team-profile]');
    if (!profile) {
      return;
    }

    var searchInput = profile.querySelector('[data-repository-search]');
    var cards = Array.prototype.slice.call(profile.querySelectorAll('[data-repository-card]'));

    if (!searchInput || !cards.length) {
      return;
    }

    searchInput.addEventListener('input', function () {
      var query = searchInput.value.trim().toLowerCase();

      cards.forEach(function (card) {
        var haystack = (card.getAttribute('data-repository-search') || '').toLowerCase();
        card.style.display = !query || haystack.indexOf(query) !== -1 ? '' : 'none';
      });
    });
  }

  function setupDependencySearch() {
    var profile = document.querySelector('[data-team-profile]');
    if (!profile) {
      return;
    }

    var searchInput = profile.querySelector('[data-dependency-search]');
    var rows = Array.prototype.slice.call(profile.querySelectorAll('[data-dependency-row]'));

    if (!searchInput || !rows.length) {
      return;
    }

    searchInput.addEventListener('input', function () {
      var query = searchInput.value.trim().toLowerCase();

      rows.forEach(function (row) {
        var haystack = (row.getAttribute('data-dependency-search') || '').toLowerCase();
        row.style.display = !query || haystack.indexOf(query) !== -1 ? '' : 'none';
      });
    });
  }

  setupDirectorySearch();
  setupTeamTabs();
  setupMemberFilters();
  setupRepositoryView();
  setupRepositorySearch();
  setupDependencySearch();
})();
