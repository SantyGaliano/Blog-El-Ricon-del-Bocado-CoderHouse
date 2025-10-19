const TB_ITEMS = [
  { icon: 'sparkles', title: 'Nuevas Recetas',      desc: 'Descubre las últimas creaciones culinarias de nuestra comunidad', grad: 0 },
  { icon: 'trending', title: 'Comunidad Creciente', desc: '50,000+ chefs compartiendo sus pasiones culinarias',             grad: 1 },
  { icon: 'gift',     title: 'Nueva Función',       desc: 'Organiza tus recetas favoritas en colecciones personalizadas',   grad: 2 },
  { icon: 'flame',    title: 'Tendencias',          desc: 'Recetas asiáticas fusión liderando en popularidad',             grad: 3 },
  { icon: 'star',     title: 'Chef Destacado',      desc: 'María Sánchez alcanza 2 millones de vistas este mes',           grad: 4 },
  { icon: 'zap',      title: 'Recetas Express',     desc: 'Deliciosas comidas listas en menos de 15 minutos',              grad: 5 }
];

const ICONS = {
  sparkles: '<svg viewBox="0 0 24 24" fill="none"><path d="M5 3l1.5 3L10 7.5 6.5 9 5 12 3.5 9 0 7.5 3.5 6 5 3Z" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 10l1 2 2 1-2 1-1 2-1-2-2-1 2-1 1-2Z" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  trending: '<svg viewBox="0 0 24 24" fill="none"><path d="M3 17l6-6 4 4 7-7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 8h7v7" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  gift:     '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="8" width="18" height="13" rx="2" stroke="#fff" stroke-width="2"/><path d="M12 8v13M3 12h18" stroke="#fff" stroke-width="2"/><path d="M12 8c-1.5-3-6-3-6 0 3 0 6 0 6 0Zm0 0c1.5-3 6-3 6 0-3 0-6 0-6 0Z" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>',
  flame:    '<svg viewBox="0 0 24 24" fill="none"><path d="M12 2s4 4 4 8a4 4 0 0 1-8 0c0-4 4-8 4-8Z" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 14a3 3 0 0 0-3 3c0 2 3 4 3 4s3-2 3-4a3 3 0 0 0-3-3Z" stroke="#fff" stroke-width="2"/></svg>',
  star:     '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3l3.09 6.26L22 10.27l-5 4.88L18.18 22 12 18.77 5.82 22 7 15.15l-5-4.88 6.91-1.01L12 3Z" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></svg>',
  zap:      '<svg viewBox="0 0 24 24" fill="none"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8Z" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></svg>'
};

(function(){
  const root = document.getElementById('topbar-min');
  if (!root) return;

  const bg = document.getElementById('tbBg');
  const dotsWrap = document.getElementById('tbDots');
  const btnPrev = document.getElementById('tbPrev');
  const btnNext = document.getElementById('tbNext');
  const btnClose = document.getElementById('tbClose');

  const slide = document.getElementById('tbSlide');
  const icon = document.getElementById('tbIcon');
  const title = document.getElementById('tbTitle');
  const desc = document.getElementById('tbDesc');
  const titleMobile = document.getElementById('tbTitleMobile');
  const bar = document.getElementById('tbProgressBar');

  let index = 0;
  let progress = 0;
  let timer = null;
  let direction = 1;

  // dots
  TB_ITEMS.forEach((_, i) => {
    const d = document.createElement('button');
    d.type = 'button';
    d.className = 'tb-dot' + (i === 0 ? ' is-active' : '');
    d.setAttribute('aria-label', `Ir al anuncio ${i+1}`);
    d.addEventListener('click', () => {
      direction = i > index ? 1 : -1;
      goTo(i);
    });
    dotsWrap.appendChild(d);
  });

  // chevrons
  btnNext.addEventListener('click', () => { direction = 1; goTo((index + 1) % TB_ITEMS.length); });
  btnPrev.addEventListener('click', () => { direction = -1; goTo((index - 1 + TB_ITEMS.length) % TB_ITEMS.length); });

  // cerrar
  btnClose.addEventListener('click', () => {
    root.style.display = 'none';
    document.documentElement.style.setProperty('--topbar-h', '0px');
  });

  // inicio
  render(0, true);
  start();

  function start(){
    stop();
    const duration = 5000, interval = 50, inc = 100 / (duration / interval);
    timer = setInterval(() => {
      progress += inc;
      if (progress >= 100) {
        direction = 1;
        goTo((index + 1) % TB_ITEMS.length);
      } else {
        bar.style.width = `${progress}%`;
      }
    }, interval);
  }
  function stop(){ if (timer) clearInterval(timer); timer = null; }

  const OUT_MS = 380, IN_MS = 500;

  function goTo(next){ if (next !== index) swap(next); }

  function swap(next){
    animateOut(slide, direction);
    setTimeout(() => {
      render(next, false);
      animateIn(slide, direction);
    }, OUT_MS);
  }

  function render(i, first){
    const item = TB_ITEMS[i];

    // fondo
    const prevClass = [...bg.classList].find(c => c.startsWith('tb-grad-'));
    if (prevClass) bg.classList.remove(prevClass);
    bg.classList.add(`tb-grad-${item.grad}`);

    // ícono sin fondo ni caja
    icon.innerHTML = `<span class="tb-icon-badge">${ICONS[item.icon] || ICONS.sparkles}</span>`;

    // textos
    title.textContent = item.title;
    titleMobile.textContent = item.title;
    desc.textContent = item.desc;

    // progress
    progress = 0;
    bar.style.width = '0%';
    const gradMap = {
      0: 'linear-gradient(90deg,#f97316,#ec4899)',
      1: 'linear-gradient(90deg,#a855f7,#2563eb)',
      2: 'linear-gradient(90deg,#ec4899,#e11d48)',
      3: 'linear-gradient(90deg,#ef4444,#ea580c)',
      4: 'linear-gradient(90deg,#eab308,#ea580c)',
      5: 'linear-gradient(90deg,#06b6d4,#2563eb)'
    };
    bar.style.background = gradMap[item.grad] || gradMap[0];

    // dots
    const all = dotsWrap.querySelectorAll('.tb-dot');
    all.forEach((d, idx) => d.classList.toggle('is-active', idx === i));

    if (!first){ start(); }
    index = i;
  }

  function animateOut(el, dir){
    el.style.transition = `opacity ${OUT_MS}ms cubic-bezier(.25,.1,.25,1), transform ${OUT_MS}ms cubic-bezier(.25,.1,.25,1)`;
    el.style.opacity = '1'; el.style.transform = 'translateY(0)';
    void el.offsetWidth;
    el.style.opacity = '0';
    el.style.transform = `translateY(${dir > 0 ? -20 : 20}px)`;
  }
  function animateIn(el, dir){
    el.style.transition = 'none';
    el.style.opacity = '0';
    el.style.transform = `translateY(${dir > 0 ? 20 : -20}px)`;
    void el.offsetWidth;
    el.style.transition = `opacity ${IN_MS}ms cubic-bezier(.25,.1,.25,1), transform ${IN_MS}ms cubic-bezier(.25,.1,.25,1)`;
    el.style.opacity = '1';
    el.style.transform = 'translateY(0)';
  }
})();
