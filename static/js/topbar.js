// Datos del carrusel: texto + gradiente + icono (SVG blanco)
const TB_ITEMS = [
  {
    text: 'Nuevas recetas de temporada disponibles',
    grad: 0,
    icon: 'sparkles'
  },
  {
    text: '50K+ chefs ya forman parte de nuestra comunidad',
    grad: 1,
    icon: 'trending'
  },
  {
    text: 'Nuevo: sistema de favoritos y colecciones personalizadas',
    grad: 2,
    icon: 'gift'
  },
  {
    text: 'Tendencia: recetas asiáticas fusión más populares',
    grad: 3,
    icon: 'flame'
  },
  {
    text: 'Chef del mes: María Sánchez con más de 2M de vistas',
    grad: 4,
    icon: 'star'
  },
  {
    text: 'Express: recetas listas en menos de 15 minutos',
    grad: 5,
    icon: 'zap'
  }
];

// SVGs en stroke blanco, 16x16
const ICONS = {
  sparkles: '<svg viewBox="0 0 24 24" fill="none"><path d="M5 3l1.5 3L10 7.5 6.5 9 5 12 3.5 9 0 7.5 3.5 6 5 3Z" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 10l1 2 2 1-2 1-1 2-1-2-2-1 2-1 1-2Z" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  trending: '<svg viewBox="0 0 24 24" fill="none"><path d="M3 17l6-6 4 4 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 8h7v7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  gift:     '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="8" width="18" height="13" rx="2" stroke-width="2"/><path d="M12 8v13M3 12h18" stroke-width="2"/><path d="M12 8c-1.5-3-6-3-6 0 3 0 6 0 6 0Zm0 0c1.5-3 6-3 6 0-3 0-6 0-6 0Z" stroke-width="2" stroke-linecap="round"/></svg>',
  flame:    '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2s4 4 4 8a4 4 0 0 1-8 0c0-4 4-8 4-8Z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 14a3 3 0 0 0-3 3c0 2 3 4 3 4s3-2 3-4a3 3 0 0 0-3-3Z" stroke-width="2"/></svg>',
  star:     '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3l3.09 6.26L22 10.27l-5 4.88L18.18 22 12 18.77 5.82 22 7 15.15l-5-4.88 6.91-1.01L12 3Z" stroke-width="2" stroke-linejoin="round"/></svg>',
  zap:      '<svg viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8Z" stroke-width="2" stroke-linejoin="round"/></svg>'
};

(function initTopbar() {
  const root = document.getElementById('topbar-aurora');
  if (!root) return;

  const bg = document.getElementById('tbBg');
  const textWrap = document.getElementById('tbTextWrap');
  const textNode = document.getElementById('tbText');
  const iconNode = document.getElementById('tbIcon');
  const dotsRight = document.getElementById('tbDotsRight');

  let idx = 0;
  let timer = null;

  // crea dots
  TB_ITEMS.forEach((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'tb-dot' + (i === 0 ? ' is-active' : '');
    b.setAttribute('aria-label', `Ir al anuncio ${i + 1}`);
    b.addEventListener('click', () => goTo(i, i > idx ? 1 : -1));
    dotsRight.appendChild(b);
  });

  // render inicial
  applyItem(0, 0);

  // autoplay
  start();

  // oculta topbar al hacer scroll; ajusta --topbar-h para mover el navbar a top
  let hidden = false;
  window.addEventListener('scroll', () => {
    const shouldHide = window.scrollY > 80;
    if (shouldHide !== hidden) {
      hidden = shouldHide;
      if (hidden) {
        root.classList.add('tb-hidden');
        document.documentElement.style.setProperty('--topbar-h', '0px');
      } else {
        root.classList.remove('tb-hidden');
        document.documentElement.style.setProperty('--topbar-h', '40px');
      }
    }
  }, { passive: true });

  function start() {
    stop();
    timer = setInterval(() => {
      goTo((idx + 1) % TB_ITEMS.length, 1);
    }, 4000);
  }

  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  // transiciones más lentas y limpias
  const OUT_MS = 520;   // salida
  const IN_MS  = 720;   // entrada

  function goTo(next, dir) {
    if (next === idx) return;
    swapContent(next, dir);
    setBg(next);
    setDots(next);
    idx = next;
  }

  function setBg(next) {
    const prevClass = [...bg.classList].find(c => c.startsWith('tb-grad-'));
    if (prevClass) bg.classList.remove(prevClass);
    bg.classList.add(`tb-grad-${TB_ITEMS[next].grad}`);
  }

  function setDots(next) {
    const all = dotsRight.querySelectorAll('.tb-dot');
    all.forEach((d, i) => d.classList.toggle('is-active', i === next));
  }

  function sentenceCase(str) {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function iconSVG(key) {
    return ICONS[key] || ICONS.sparkles;
  }

  function swapContent(next, dir) {
    // animación de salida
    animateOut(iconNode, dir);
    animateOut(textNode, dir);

    // sustituye contenido cuando termina la salida
    setTimeout(() => {
      iconNode.innerHTML = iconSVG(TB_ITEMS[next].icon);
      iconNode.classList.remove('tb-icon-anim'); // reinicio de animación
      void iconNode.offsetWidth;                 // reflow
      iconNode.classList.add('tb-icon-anim');

      textNode.textContent = sentenceCase(TB_ITEMS[next].text);

      // animación de entrada
      animateIn(iconNode, dir);
      animateIn(textNode, dir);
    }, OUT_MS);
  }

  function animateOut(el, dir) {
    el.style.transition = `opacity ${OUT_MS}ms cubic-bezier(.22,.61,.36,1), transform ${OUT_MS}ms cubic-bezier(.22,.61,.36,1)`;
    el.style.opacity = '1';
    el.style.transform = 'translateX(0)';
    // fuerza reflow
    void el.offsetWidth;
    el.style.opacity = '0';
    el.style.transform = `translateX(${dir > 0 ? -24 : 24}px)`;
  }

  function animateIn(el, dir) {
    el.style.transition = 'none';
    el.style.opacity = '0';
    el.style.transform = `translateX(${dir > 0 ? 24 : -24}px)`;
    void el.offsetWidth;
    el.style.transition = `opacity ${IN_MS}ms cubic-bezier(.22,.61,.36,1), transform ${IN_MS}ms cubic-bezier(.22,.61,.36,1)`;
    el.style.opacity = '1';
    el.style.transform = 'translateX(0)';
  }

  function applyItem(i, dir) {
    setBg(i);
    setDots(i);
    iconNode.innerHTML = iconSVG(TB_ITEMS[i].icon);
    iconNode.classList.add('tb-icon-anim');
    textNode.textContent = sentenceCase(TB_ITEMS[i].text);
    // entrada inicial sin salida previa
    animateIn(iconNode, dir);
    animateIn(textNode, dir);
  }
})();
