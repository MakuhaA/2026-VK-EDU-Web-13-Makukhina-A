const root = document.documentElement;

window.addEventListener("pointermove", (e) => {
  // координаты курсора в пикселях от левого верхнего угла окна
  root.style.setProperty("--x", e.clientX);
  root.style.setProperty("--y", e.clientY);

  // нормализованные координаты от -0.5 до 0.5
  const xp = e.clientX / window.innerWidth - 0.5;
  const yp = e.clientY / window.innerHeight - 0.5;
  root.style.setProperty("--xp", xp);
  root.style.setProperty("--yp", yp);
});