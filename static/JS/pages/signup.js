(function () {
  function setupSignupTeamPicker() {
    var picker = document.querySelector('[data-team-picker]');
    var select = document.querySelector('[data-team-select]');
    var hint = document.querySelector('[data-team-selection-hint]');

    if (!picker || !select) {
      return;
    }

    var buttons = Array.prototype.slice.call(picker.querySelectorAll('[data-team-option]'));

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

    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        syncSelection(button.getAttribute('data-team-value'));
      });
    });

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
