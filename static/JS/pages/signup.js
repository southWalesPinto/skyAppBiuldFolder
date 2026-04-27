(function () {
  function setupSignupTeamPicker() {
    var wrapper = document.querySelector('[data-team-wrapper]');
    var picker = document.querySelector('[data-team-picker]');
    var select = document.querySelector('[data-team-select]');
    var hint = document.querySelector('[data-team-selection-hint]');
    var searchInput = document.querySelector('[data-team-search]');

    if (!picker || !select || !wrapper) {
      return;
    }

    var buttons = Array.prototype.slice.call(picker.querySelectorAll('[data-team-option]'));

    function openPicker() {
      picker.classList.add('is-open');
      if (searchInput) searchInput.focus();
    }

    function closePicker() {
      picker.classList.remove('is-open');
      if (searchInput) searchInput.value = '';
      filterTeams('');
    }

    function syncSelection(value) {
      select.value = value;
      buttons.forEach(function (button) {
        button.classList.toggle('is-active', button.getAttribute('data-team-value') === value);
      });

      var activeButton = buttons.find(function (button) {
        return button.getAttribute('data-team-value') === value;
      });

      if (hint && activeButton) {
        hint.textContent = 'Selected team: ' + activeButton.getAttribute('data-team-name') + ' · ' + activeButton.getAttribute('data-team-lead');
      }
    }

    function filterTeams(query) {
      var lowerQuery = query.toLowerCase();
      var hasVisibleCards = false;

      buttons.forEach(function (button) {
        var teamName = button.getAttribute('data-team-name').toLowerCase();
        var teamLead = button.getAttribute('data-team-lead').toLowerCase();
        var matches = teamName.includes(lowerQuery) || teamLead.includes(lowerQuery);

        if (query === '' || matches) {
          button.classList.remove('hidden');
          hasVisibleCards = true;
        } else {
          button.classList.add('hidden');
        }
      });

      if (query && !hasVisibleCards) {
        picker.classList.add('has-no-matches');
      } else {
        picker.classList.remove('has-no-matches');
      }
    }

    // Open picker on select focus/click
    select.addEventListener('click', openPicker);
    select.addEventListener('focus', openPicker);

    // Close picker when clicking outside
    document.addEventListener('click', function (e) {
      if (!wrapper.contains(e.target)) {
        closePicker();
      }
    });

    buttons.forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault();
        syncSelection(button.getAttribute('data-team-value'));
        closePicker();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', function () {
        filterTeams(searchInput.value);
      });
    }

    if (!select.value && buttons.length) {
      syncSelection(buttons[0].getAttribute('data-team-value'));
    } else {
      syncSelection(select.value);
    }

    select.addEventListener('change', function () {
      syncSelection(select.value);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSignupTeamPicker);
  } else {
    setupSignupTeamPicker();
  }
})();
