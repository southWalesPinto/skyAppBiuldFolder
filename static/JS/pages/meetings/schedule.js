(function () {
  function setupScheduleModal() {
    var modal = document.querySelector('[data-schedule-modal-root]');
    if (!modal) {
      return;
    }

    var openButtons = Array.prototype.slice.call(document.querySelectorAll('[data-schedule-open-modal]'));
    var closeTargets = Array.prototype.slice.call(document.querySelectorAll('[data-schedule-close-modal]'));
    var dialog = modal.querySelector('.schedule-modal-dialog');

    function openModal() {
      modal.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      modal.classList.remove('is-open');
      document.body.style.overflow = '';
    }

    openButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        openModal();
      });
    });

    closeTargets.forEach(function (element) {
      element.addEventListener('click', function (event) {
        event.preventDefault();
        closeModal();
      });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) {
        closeModal();
      }
    });

    modal.addEventListener('click', function (event) {
      if (!dialog.contains(event.target)) {
        closeModal();
      }
    });

    if (modal.classList.contains('is-open')) {
      document.body.style.overflow = 'hidden';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupScheduleModal);
  } else {
    setupScheduleModal();
  }
})();
