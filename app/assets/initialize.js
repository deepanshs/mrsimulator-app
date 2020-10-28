/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

var init = function () {
  /* Hide quadrupolar section if the isotope is spin 1/2. */
  $("#isotope").on("change", function (e) {
    hideQuad();
    e.preventDefault();
  });

  // Update spin-system card title when the value of the spin-system name
  // attribute change.
  $("#spin-system-name").on("keyup", function (e) {
    $("#spin-system-title")[0].innerHTML = this.value;
    e.preventDefault();
  });

  // Search and filter spin-systems
  $("#search-spin-system").on("input", searchSpinSystems);

  // Search and filter methods
  $("#search-method").on("input", searchMethods);

  // Selection of sidebar tabs
  let sidebarTabs = document.querySelectorAll("[data-tab-target]");
  sidebarTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      let target = $(`#${tab.dataset.tabTarget}`)[0];

      sidebarTabs.forEach((tab) => {
        let target = $(`#${tab.dataset.tabTarget}`)[0];
        target.classList.remove("active");
      });
      target.classList.add("active");

      sidebarTabs.forEach((tab) => {
        tab.classList.remove("active");
      });
      tab.classList.add("active");
    });
  });

  return null;
};

/* Hide the quadrupolar attribute from the user, if the isotope is not
 * quadrupolar. */
var hideQuad = function () {
  var isotope_id, quad_collapse, check_quad;
  isotope_id = getValue("isotope");
  if (isotope_id === null) {
    throw window.dash_clientside.PreventUpdate;
  }
  quad_collapse = document.getElementById("quadrupolar-feature-collapse");
  if (quad_collapse === null) {
    throw window.dash_clientside.PreventUpdate;
  }
  check_quad = ISOTOPE_DATA.includes(isotope_id) ? false : true;
  if (check_quad) {
    quad_collapse.classList.add("show");
    quad_collapse.attributes[2].value = "true";
  } else {
    quad_collapse.classList.remove("show");
    quad_collapse.attributes[2].value = "false";
  }
};

// var hideMenu = function(element) {
//   element.style.opacity = 0;
//   element.style.pointerEvents = 'none';
//   element.style.transform = 'translateY(-10px)';
// }
