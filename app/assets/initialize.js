/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]
 */

var init = function() {
  console.log($('#isotope'));
  /* Hide quadrupolar section if the isotope is spin 1/2. */
  $('#isotope').on('change', function(e) {
    hide_quad();
    e.preventDefault();
  });

  // // Update storeData values when field value change.
  //   var keys;
  // for (i = 0; i < ALL_KEYS.length; i++) {
  //     keys = ALL_KEYS[i].split('-');
  //     if (keys.length == 1) {
  //         $(`#${ALL_KEYS[i]}`).on('change', function () {
  //             index = get_isotopomer_index();
  //             temp = storeData['data']['isotopomers'][index]['sites'][0];
  //             temp[this.id] = (isNaN(+(this.value))) ? this.value :
  //             +(this.value);

  //             var listomers = $('#isotopomer-read-only div.display-form ul
  //             li'); listomers[index].innerHTML =
  //             update_info(storeData['data']['isotopomers'][index], index);
  //         });
  //     } else {
  //         $(`#${ALL_KEYS[i]}`).on('change', function () {
  //             var k_ = this.id.split('-')
  //             index = get_isotopomer_index();
  //             temp = storeData['data']['isotopomers'][index]['sites'][0];
  //             if (!temp.hasOwnProperty(k_[0])) { temp[k_[0]] = {}; }

  //             val = parseFloat(this.value);
  //             if (k_[1] == 'Cq') { val *= 1e6 }
  //             else if (k_[1] == 'alpha') { val /= to_deg }
  //             else if (k_[1] == 'beta') { val /= to_deg }
  //             else if (k_[1] == 'gamma') { val /= to_deg }
  //             temp[k_[0]][k_[1]] = val;

  //             var listomers = $('#isotopomer-read-only div.display-form ul
  //             li'); listomers[index].innerHTML =
  //             update_info(storeData['data']['isotopomers'][index], index);
  //         });
  //     }
  // }

  // Update isotopomer card title when the value of the isotopomer name
  // attribute change.
  $('#isotopomer-name').on('keyup', function(e) {
    $('#isotopomer-title')[0].innerHTML = this.value;
    e.preventDefault();
  });

  // Search and filter isotopomers
  // $('#search-isotopomer').on = search;
  $('#search-isotopomer').on('input', search);

  // Toggle isotopomer window with view-isotopomers button
  $('#view-isotopomers').on('click', function(e) {
    var element1 = $('#isotopomer-body')[0].classList;
    var element2 = $('#dimension-body')[0].classList;
    element1.remove('hide-window');
    element2.add('hide-window');
    e.preventDefault();
  });

  // Toggle methods window with view-methods button
  $('#view-methods').on('click', function(e) {
    var element1 = $('#isotopomer-body')[0].classList;
    var element2 = $('#dimension-body')[0].classList;
    element1.add('hide-window');
    element2.remove('hide-window');
    e.preventDefault();
  });

  // $('#add-isotopomer-button').on('click', addNewIsotopomer);


  // var app1 = document.getElementsByClassName("app-1");
  // console.log(app1);
  // app1[0].onscroll = function () {
  //     var graph = document.getElementById("floating-card");
  //     var sticky = graph.offsetTop;

  //     // console.log(app1[0]);
  //     if (app1[0].scrollTop > sticky - 5) {
  //         graph.classList.add("sticky");
  //     } else {
  //         graph.classList.remove("sticky");
  //     }

  //     var h = document.getElementById("dimension-body").offsetTop;
  //     if (app1[0].scrollTop > h) {
  //         graph.classList.remove('hide-display')
  //     }
  // };
  return null;
};

/* Hide the quadrupolar attribute from the user, if the isotope is not
 * quadrupolar. */
var hide_quad = function() {
  var isotope_id = getValue('isotope');
  if (isotope_id === null) {
    window.dash_clientside.PreventUpdate;
  }
  quad_collapse = document.getElementById('quadrupolar-feature-collapse');
  if (quad_collapse === null) {
    window.dash_clientside.PreventUpdate;
  }
  check_quad = ISOTOPE_DATA.includes(isotope_id) ? false : true;
  if (check_quad) {
    quad_collapse.classList.add('show');
    quad_collapse.attributes[2].value = 'true';
  } else {
    quad_collapse.classList.remove('show');
    quad_collapse.attributes[2].value = 'false';
  }
};
