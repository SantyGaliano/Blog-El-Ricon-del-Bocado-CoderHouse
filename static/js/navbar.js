// hover-intent para dropdowns sin parpadeo
(function () {
  const HOVER_DELAY = 100;
  const LEAVE_DELAY = 180;

  document.querySelectorAll('.nav-item.dropdown.position-static[data-hover="true"]').forEach((li) => {
    const link = li.querySelector('[data-bs-toggle="dropdown"]');
    const menu = li.querySelector('.dropdown-menu');
    if (!link || !menu) return;

    let enterT = null;
    let leaveT = null;

    const show = () => {
      clearTimeout(leaveT);
      enterT = setTimeout(() => {
        li.classList.add('show');
        link.classList.add('show');
        menu.classList.add('show');
        link.setAttribute('aria-expanded', 'true');
      }, HOVER_DELAY);
    };

    const hide = () => {
      clearTimeout(enterT);
      leaveT = setTimeout(() => {
        li.classList.remove('show');
        link.classList.remove('show');
        menu.classList.remove('show');
        link.setAttribute('aria-expanded', 'false');
      }, LEAVE_DELAY);
    };

    li.addEventListener('mouseenter', show);
    li.addEventListener('mouseleave', hide);

    // en móvil conserva el comportamiento por click
    link.addEventListener('click', (e) => {
      if (window.matchMedia('(hover: hover)').matches) {
        e.preventDefault();
      }
    });
  });
})();
