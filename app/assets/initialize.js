/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

var init = function () {
  console.log($("#isotope"));
  /* Hide quadrupolar section if the isotope is spin 1/2. */
  $("#isotope").on("change", function (e) {
    hideQuad();
    e.preventDefault();
  });

  // // Update storeData values when field value change.
  //   var keys;
  // for (i = 0; i < ALL_KEYS.length; i++) {
  //     keys = ALL_KEYS[i].split('-');
  //     if (keys.length == 1) {
  //         $(`#${ALL_KEYS[i]}`).on('change', function () {
  //             index = get_spin_system_index();
  //             temp = storeData['data']['spin_systems'][index]['sites'][0];
  //             temp[this.id] = (isNaN(+(this.value))) ? this.value :
  //             +(this.value);

  //             var listomers = $('#spin-system-read-only div.display-form ul
  //             li'); listomers[index].innerHTML =
  //             update_info(storeData['data']['spin_systems'][index], index);
  //         });
  //     } else {
  //         $(`#${ALL_KEYS[i]}`).on('change', function () {
  //             var k_ = this.id.split('-')
  //             index = get_spin_system_index();
  //             temp = storeData['data']['spin_systems'][index]['sites'][0];
  //             if (!temp.hasOwnProperty(k_[0])) { temp[k_[0]] = {}; }

  //             val = parseFloat(this.value);
  //             if (k_[1] == 'Cq') { val *= 1e6 }
  //             else if (k_[1] == 'alpha') { val /= to_deg }
  //             else if (k_[1] == 'beta') { val /= to_deg }
  //             else if (k_[1] == 'gamma') { val /= to_deg }
  //             temp[k_[0]][k_[1]] = val;

  //             var listomers = $('#spin-system-read-only div.display-form ul
  //             li'); listomers[index].innerHTML =
  //             update_info(storeData['data']['spin_systems'][index], index);
  //         });
  //     }
  // }

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

  // Toggle spin-system window with view-spin-systems button
  $("#view-spin-systems").on("click", function (e) {
    let element1 = $("#spin-system-body")[0].classList;
    let element2 = $("#method-body")[0].classList;
    let element3 = $("#info-body")[0].classList;

    element1.remove("hide-window");
    element2.add("hide-window");
    element3.add("hide-window");

    let spin_system_tools = $("#spin-system-edit-tools")[0];
    let method_tools = $("#method-edit-tools")[0];
    spin_system_tools.style.display = "flex";
    method_tools.style.display = "none";

    e.preventDefault();
  });

  // Toggle methods window with view-methods button
  $("#view-methods").on("click", function (e) {
    let element1 = $("#spin-system-body")[0].classList;
    let element2 = $("#method-body")[0].classList;
    let element3 = $("#info-body")[0].classList;

    element1.add("hide-window");
    element2.remove("hide-window");
    element3.add("hide-window");

    let spin_system_tools = $("#spin-system-edit-tools")[0];
    let method_tools = $("#method-edit-tools")[0];
    spin_system_tools.style.display = "none";
    method_tools.style.display = "flex";

    e.preventDefault();
  });

  // Toggle info window with view-info button
  $("#view-info").on("click", function (e) {
    let element1 = $("#spin-system-body")[0].classList;
    let element2 = $("#method-body")[0].classList;
    let element3 = $("#info-body")[0].classList;

    element1.add("hide-window");
    element2.add("hide-window");
    element3.remove("hide-window");

    let spin_system_tools = $("#spin-system-edit-tools")[0];
    let method_tools = $("#method-edit-tools")[0];
    spin_system_tools.style.display = "none";
    method_tools.style.display = "none";
    e.preventDefault();
  });

  // MenuBar items default action
  // show menu when hover.
  $('[class$="-menu"] label').each(function () {
    $(this).hover(function (e) {
      this.nextElementSibling.style.display = "flex";
      e.preventDefault();
    });
  });
  // hide menu.
  $('[class$="-menu"] li').each(function () {
    $(this).click(function (e) {
      this.parentElement.style.display = "none";
      // e.preventDefault();
    });
  });

  // View menu callbacks.
  $(".view-menu li").each(function () {
    $(this).click(function (e) {
      let index = $(this).index();
      if (index === 0) {
        $("#view-info")[0].click();
      }
      if (index === 1) {
        $("#view-spin-systems")[0].click();
      }
      if (index === 2) {
        $("#view-methods")[0].click();
      }

      e.preventDefault();
    });
  });

  // Spin system menu callbacks.
  $(".spin-system-menu li").each(function () {
    $(this).click(function (e) {
      let index = $(this).index();
      if (index === 0) {
        $("#add-spin-system-button")[0].click();
      }
      if (index === 1) {
        $("#duplicate-spin-system-button")[0].click();
      }
      if (index === 2) {
        $("#remove-spin-system-button")[0].click();
      }
      e.preventDefault();
    });
  });

  // Method menu callbacks.
  $(".method-menu li").each(function () {
    $(this).click(function (e) {
      let index = $(this).index();
      if (index === 0) {
        $("#add-method-button")[0].click();
      }
      if (index === 1) {
        $("#duplicate-method-button")[0].click();
      }
      if (index === 2) {
        $("#remove-method-button")[0].click();
      }
      e.preventDefault();
    });
  });

  // $('#open-mrsimulator-file').on('click', function(e) {
  //   $('#upload-and-add-spin-system-button input')[0].click();
  //   e.preventDefault();
  // });

  // $('#upload_spin_system_button').on('click', function(e) {
  //   $('#upload-spin-system-local input')[0].click();
  //   e.preventDefault();
  // });

  // $('.view-menu button').on('click', function(e) {
  //   var viewUl = $('.view-menu ul')[0];
  //   if (viewUl.style.opacity === '1') {
  //     viewUl.style.opacity = 0;
  //     viewUl.style.pointerEvents = 'none';
  //     viewUl.style.transform = 'translateY(-10px)';
  //   } else {
  //     viewUl.style.opacity = 1;
  //     viewUl.style.pointerEvents = 'all';
  //     viewUl.style.transform = 'translateY(0px)';
  //   }
  // });

  // $('.main').on('click', function(e) {
  //   var viewUl = $('.view-menu ul')[0];
  //   if (viewUl.style.opacity === '1') {
  //     viewUl.style.opacity = 0;
  //     viewUl.style.pointerEvents = 'none';
  //     viewUl.style.transform = 'translateY(-10px)';
  //   }
  // });

  // $('#add-spin-system-button').on('click', addNewSpinSystem);

  // var app1 = document.getElementsByClassName("app-1");
  // app1[0].onscroll = function () {
  //     var graph = document.getElementById("floating-card");
  //     var sticky = graph.offsetTop;

  //     if (app1[0].scrollTop > sticky - 5) {
  //         graph.classList.add("sticky");
  //     } else {
  //         graph.classList.remove("sticky");
  //     }

  //     var h = document.getElementById("method-body").offsetTop;
  //     if (app1[0].scrollTop > h) {
  //         graph.classList.remove('hide-display')
  //     }
  // };
  $("#view-info")[0].click();
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
