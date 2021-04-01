/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

/* jshint esversion: 6 */

var init = function () {
  // Update spin-system card title when the value of the spin-system name
  // attribute change.
  let element = document.getElementById("spin-system-name");
  element.addEventListener("keyup", (event) => {
    document.getElementById("spin-system-title").innerHTML = getValue(
      "spin-system-name"
    );
    event.preventDefault();
  });

  // Search and filter spin-systems
  // $("#search-spin-system").on("input", searchSpinSystems);

  // Search and filter methods
  element = document.getElementById("search-method");
  element.addEventListener("input", searchMethods);

  return null;
};

/* Hide the quadrupolar attribute from the user, if the isotope is not
 * quadrupolar. */
var hideQuad = function () {
  let isotope_id, quad_collapse, check_quad;
  isotope_id = getValue("isotope");
  quad_collapse = document.getElementById("quadrupolar-feature-collapse");
  console.log(quad_collapse);
  check_quad = ISOTOPE_DATA.includes(isotope_id) ? false : true;
  if (check_quad) quad_collapse.classList.add("show");
  else quad_collapse.classList.remove("show");
};
