// TaskFlow — JS minimal (menu mobile + sous-menus)
document.addEventListener("DOMContentLoaded", () => {
  // Menu mobile
  const toggle = document.querySelector("[data-menu-toggle]");
  const sidebar = document.querySelector(".sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  }

  // Sous-menus dépliables (<li data-collapsible>)
  document.querySelectorAll("[data-collapsible] > .nav-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      const sub = link.nextElementSibling;
      if (sub && sub.classList.contains("subnav")) {
        e.preventDefault();
        sub.hidden = !sub.hidden;
      }
    });
  });
});
