(function () {
  function setupOrganisationFilters() {
    var page = document.querySelector('[data-organisation-page]');
    if (!page) {
      return;
    }

    var grid = page.querySelector('[data-org-grid]');
    var cards = Array.prototype.slice.call(page.querySelectorAll('[data-org-team-card]'));
    var departmentInput = page.querySelector('[data-org-filter="department"]');
    var teamTypeInput = page.querySelector('[data-org-filter="team_type"]');
    var dependenciesInput = page.querySelector('[data-org-filter="dependencies"]');
    var globalSearch = page.querySelector('[data-org-global-search]');
    var totalTeams = page.querySelector('[data-org-total-teams]');
    var totalMembers = page.querySelector('[data-org-total-members]');
    var emptyState = page.querySelector('[data-org-empty-state]');
    var viewButtons = Array.prototype.slice.call(page.querySelectorAll('[data-org-view]'));
    var exportLink = page.querySelector('.org-export-btn');

    function rawValue(input) {
      return input ? input.value.trim() : '';
    }

    function value(input) {
      return rawValue(input).toLowerCase();
    }

    function getActiveView() {
      var activeButton = viewButtons.find(function (button) {
        return button.classList.contains('is-active');
      });
      return activeButton ? activeButton.getAttribute('data-org-view') : 'grid';
    }

    function updateExportLink() {
      if (!exportLink) {
        return;
      }

      var baseHref = exportLink.getAttribute('href') || '';
      var url = new URL(baseHref, window.location.origin);
      var params = new URLSearchParams(url.search);

      var department = rawValue(departmentInput);
      var teamType = rawValue(teamTypeInput);
      var dependencies = rawValue(dependenciesInput);
      var search = rawValue(globalSearch);
      var view = getActiveView();

      if (department) {
        params.set('department', department);
      } else {
        params.delete('department');
      }

      if (teamType) {
        params.set('team_type', teamType);
      } else {
        params.delete('team_type');
      }

      if (dependencies) {
        params.set('dependencies', dependencies);
      } else {
        params.delete('dependencies');
      }

      if (search) {
        params.set('search', search);
      } else {
        params.delete('search');
      }

      params.set('view', view);

      url.search = params.toString();
      exportLink.setAttribute('href', url.pathname + (url.search ? '?' + url.search : ''));
    }

    function applyFilters() {
      var department = value(departmentInput);
      var teamType = value(teamTypeInput);
      var dependencies = value(dependenciesInput);
      var search = value(globalSearch);
      var visibleCount = 0;
      var visibleMembers = 0;

      cards.forEach(function (card) {
        var name = (card.getAttribute('data-team-name') || '').toLowerCase();
        var cardDepartment = (card.getAttribute('data-team-department') || '').toLowerCase();
        var cardType = (card.getAttribute('data-team-type') || '').toLowerCase();
        var cardDependencies = (card.getAttribute('data-team-dependencies') || '').toLowerCase();
        var memberCount = parseInt(card.getAttribute('data-team-members') || '0', 10);
        var matchesDepartment = !department || cardDepartment.indexOf(department) !== -1;
        var matchesTeamType = !teamType || cardType.indexOf(teamType) !== -1;
        var matchesDependencies = !dependencies || cardDependencies.indexOf(dependencies) !== -1;
        var searchHaystack = [name, cardDepartment, cardType, cardDependencies].join(' ');
        var matchesSearch = !search || searchHaystack.indexOf(search) !== -1;
        var isVisible = matchesDepartment && matchesTeamType && matchesDependencies && matchesSearch;

        card.classList.toggle('is-hidden', !isVisible);
        if (isVisible) {
          visibleCount += 1;
          visibleMembers += Number.isNaN(memberCount) ? 0 : memberCount;
        }
      });

      if (totalTeams) {
        totalTeams.textContent = String(visibleCount);
      }

      if (totalMembers) {
        totalMembers.textContent = String(visibleMembers);
      }

      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }

      if (grid) {
        grid.classList.toggle('is-empty', visibleCount === 0);
      }

      updateExportLink();
    }

    [departmentInput, teamTypeInput, dependenciesInput, globalSearch].forEach(function (input) {
      if (!input) {
        return;
      }
      input.addEventListener('input', applyFilters);
    });

    viewButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var mode = button.getAttribute('data-org-view');
        viewButtons.forEach(function (item) {
          item.classList.toggle('is-active', item === button);
        });
        if (grid) {
          grid.classList.toggle('is-network', mode === 'network');
          grid.classList.toggle('is-grid', mode !== 'network');
        }
        updateExportLink();
      });
    });

    applyFilters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupOrganisationFilters);
  } else {
    setupOrganisationFilters();
  }
})();
