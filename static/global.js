(function () {
  function setupProfileDropdown() {
    var wrapper = document.querySelector('[data-profile-menu-wrapper]');
    if (!wrapper) {
      return;
    }

    var button = wrapper.querySelector('[data-profile-menu-button]');
    var menu = wrapper.querySelector('[data-profile-menu]');
    if (!button || !menu) {
      return;
    }

    function openMenu() {
      wrapper.classList.add('is-open');
      menu.classList.add('is-open');
      menu.hidden = false;
      button.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
      wrapper.classList.remove('is-open');
      menu.classList.remove('is-open');
      menu.hidden = true;
      button.setAttribute('aria-expanded', 'false');
    }

    function toggleMenu() {
      var isOpen = wrapper.classList.contains('is-open');
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    }

    button.addEventListener('click', function (event) {
      event.stopPropagation();
      toggleMenu();
    });

    document.addEventListener('click', function (event) {
      if (!wrapper.contains(event.target)) {
        closeMenu();
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closeMenu();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupProfileDropdown);
  } else {
    setupProfileDropdown();
  }
})();
