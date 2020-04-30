/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]
 */

const ISOTOPE_DATA = [
  '1H',    '3He',   '13C',   '15N',   '19F',   '29Si',  '31P',
  '57Fe',  '77Se',  '89Y',   '103Rh', '109Ag', '107Ag', '111Cd',
  '119Sn', '117Sn', '115Sn', '125Te', '129Xe', '169Tm', '171Yb',
  '183W',  '187Os', '195Pt', '199Hg', '205Tl', '203Tl', '207Pb',
];


const to_deg = 180 / 3.14159265359;
const ATTR_PER_SITE = 12;
var i, j, k;
const euler_angle = ['alpha', 'beta', 'gamma'];
const ALL_KEYS = [
  'isotope', 'isotropic_chemical_shift', 'shielding_symmetric-zeta',
  'shielding_symmetric-eta', 'shielding_symmetric-alpha',
  'shielding_symmetric-beta', 'shielding_symmetric-gamma', 'quadrupolar-Cq',
  'quadrupolar-eta', 'quadrupolar-alpha', 'quadrupolar-beta',
  'quadrupolar-gamma'
];

/* Isotopomer functions */
/* Return the selected li index from the isotopomers. */
var get_isotopomer_index = function() {
  return storeData['isotopomer_index'];
};

var set_isotopomer_index = function(index) {
  storeData['isotopomer_index'] = index;
};

/* Intiate a click event for the li.
 * @param listomer: A list of li, each summarizing an isotopomer.
 * @param index: The index of li to initiate the click.
 */
var select_isotopomer = function(listomers, index) {
  if (listomers.length > 0) {
    listomers[index].click();
  }
};

/* Extract the site attributes and set it to the UI fields.
 * @param site: The site dictionary.
 */
var set_site_attributes = function(site) {
  // isotope and isotropic chemical shift
  setValue('isotope', site['isotope']);
  setValue('isotropic_chemical_shift', site['isotropic_chemical_shift']);

  // shielding symmetric
  var key = 'shielding_symmetric';
  if (site.hasOwnProperty(key)) {
    var ss = site[key];
    setValue(`${key}-zeta`, ss['zeta']);
    setValue(`${key}-eta`, ss['eta']);
    // Convert Euler angles in radians.
    setValue(
        `${key}-alpha`,
        (ss.hasOwnProperty('alpha')) ? rad_to_deg(ss['alpha']) : null);
    setValue(
        `${key}-beta`,
        (ss.hasOwnProperty('beta')) ? rad_to_deg(ss['beta']) : null);
    setValue(
        `${key}-gamma`,
        (ss.hasOwnProperty('gamma')) ? rad_to_deg(ss['gamma']) : null);
  } else {
    setValue(`${key}-zeta`, null);
    setValue(`${key}-eta`, null);
    setValue(`${key}-alpha`, null);
    setValue(`${key}-beta`, null);
    setValue(`${key}-gamma`, null);
  };

  // quadrupolar
  key = 'quadrupolar';
  if (site.hasOwnProperty(key)) {
    var ss = site[key];
    setValue(`${key}-Cq`, ss['Cq'] / 1e6);  // Convert Cq in MHz.
    setValue(`${key}-eta`, ss['eta']);
    // Convert Euler angles in radians.
    setValue(
        `${key}-alpha`,
        (ss.hasOwnProperty('alpha')) ? rad_to_deg(ss['alpha']) : null);
    setValue(
        `${key}-beta`,
        (ss.hasOwnProperty('beta')) ? rad_to_deg(ss['beta']) : null);
    setValue(
        `${key}-gamma`,
        (ss.hasOwnProperty('gamma')) ? rad_to_deg(ss['gamma']) : null);
  } else {
    setValue(`${key}-Cq`, null);
    setValue(`${key}-eta`, null);
    setValue(`${key}-alpha`, null);
    setValue(`${key}-beta`, null);
    setValue(`${key}-gamma`, null);
  }
};

/* Update the isotopomer UI field using the data from the isotopomers dictionary
 * at index, `index`.
 * @param index: The index of the isotopomer.
 */
var update_field_from_isotopomer_at_index = function(index) {
  var data = storeData['data'];
  var isotopomer = data['isotopomers'][index];

  // name, description, and abundance of the isotopomer

  var name = isotopomer['name'];
  setValue('isotopomer-name', name);
  $('#isotopomer-title')[0].innerHTML = (name == '') ? `Isotopomer ${index}` : name;
  setValue('isotopomer-description', isotopomer['description']);
  setValue('isotopomer-abundance', isotopomer['abundance']);

  // extract site information
  var site = isotopomer['sites'][0];
  set_site_attributes(site);
};

/* Convert Euler angles from degrees to radians.
 * @params obj: An object dictionary holding the three Euler angles
 */
var euler_angle_deg_to_rad = function(obj) {
  for (i = 0; i < euler_angle.length; i++) {
    if (obj.hasOwnProperty(euler_angle[i])) {
      obj[euler_angle[i]] /= to_deg;
    }
  }
};

/* Extract the site dictionary from the UI field using the UI ids. */
var extract_site_object_from_fields = function() {
  // Get the isotopomers data from the session storage.
  var data = storeData['data'];
  if (data === null) {
    throw window.dash_clientside.PreventUpdate;
  }
  // Extract the current isotopomer index, and get the respective isotopomer.
  var index = get_isotopomer_index();
  var isotopomer = data['isotopomers'][index];

  // Extract name and description information from the states and update the
  // isotopomer object
  isotopomer['name'] = getValue('isotopomer-name');
  isotopomer['description'] = getValue('isotopomer-description');
  isotopomer['abundance'] = getValue('isotopomer-abundance');

  // Set up a default site dictionary and then populate the key-value pairs.
  var site = {
    'isotope': null,
    'isotropic_chemical_shift': null,
    'shielding_symmetric': {},
    'quadrupolar': {}
  };
  var val, id, key;
  for (i = 0; i < ATTR_PER_SITE; i++) {
    id = ALL_KEYS[i];
    val = getValue(id);
    if (val != null) {
      key = id.split('-');
      if (key.length === 1) {
        site[key[0]] = val;
      }
      if (key.length === 2) {
        site[key[0]][key[1]] = val;
      }
    }
  }
  // Convert Euler angles from degrees to radians.
  euler_angle_deg_to_rad(site['shielding_symmetric']);
  euler_angle_deg_to_rad(site['quadrupolar']);

  // Convert Cq from MHz to Hz.
  if (site['quadrupolar'].hasOwnProperty('Cq')) {
    site['quadrupolar']['Cq'] *= 1.0e6;
  }

  // Check if the value of a key is an empty dictionary. If true, remove the
  // respective key-value pair.
  if (Object.keys(site['shielding_symmetric']).length === 0) {
    delete site['shielding_symmetric'];
  }
  if (Object.keys(site['quadrupolar']).length === 0) {
    delete site['quadrupolar'];
  }

  // Assign the new site object to the isotopomers at site index 0.
  isotopomer['sites'][0] = site;
  return isotopomer;
};


print_label =
    ['Isotope', 'Shift (δ)', 'ζ', 'η', 'α', 'β', 'γ', 'Cq', 'η', 'α', 'β', 'γ'];
unit = [null, 'ppm', 'ppm', '', '°', '°', '°', 'MHz', '', '°', '°', '°'];

var update_info = function(ito, i) {
  var output = `<div><a>`;
  var s_len, sto, sti, temp, sites, key, val;
  console.log(ito);

  // name
  temp = `Isotopomer ${i}`;
  if (ito.hasOwnProperty('name')) {
    if (ito['name'] != '' || ito['name'] != null) {
      temp = ito['name'];
    }
  }
  output += `<b>${temp}</b>`;  // add name

  // description
  if (ito.hasOwnProperty('description')) {
    if (ito['description'] != '' || ito['description'] != null) {
      output += `<div>${ito['description']}</div>`;  // add description
    }
  }

  // abundance
  temp = (ito.hasOwnProperty('abundance')) ? ito['abundance'] : '100';
  output += `<div>Abundance: ${temp} %</div>`;

  sites = ito['sites'];
  s_len = sites.length;
  for (j = 0; j < s_len; j++) {
    sto = sites[j];

    output += `<div class="pl-2">Isotope: ${sto['isotope']}</div>`;

    output += `<div class="pl-2">${print_label[1]}: ${
        sto['isotropic_chemical_shift']} ${unit[1]}</div>`;

    if (sto.hasOwnProperty('shielding_symmetric')) {
      output += `<div class="pl-2">Symmetric Shielding</div>`;
      sti = sto['shielding_symmetric'];
      for (k = 2; k < 7; k++) {
        key = ALL_KEYS[k].split('-')[1];

        val = sti[key];
        if (key == 'alpha') {
          val *= to_deg;
        } else if (key == 'beta') {
          val *= to_deg;
        } else if (key == 'gamma') {
          val *= to_deg;
        }

        if (sti.hasOwnProperty(key)) {
          output +=
              `<div class="pl-4">${print_label[k]}: ${val} ${unit[k]}</div>`;
        }
      }
    }
    if (sto.hasOwnProperty('quadrupolar')) {
      output += `<div class="pl-2">Quadrupolar</div>`;
      sti = sto['quadrupolar'];
      for (k = 7; k < 12; k++) {
        key = ALL_KEYS[k].split('-')[1];

        val = sti[key];
        if (key == 'Cq') {
          val /= 1e6;
        } else if (key == 'alpha') {
          val *= to_deg;
        } else if (key == 'beta') {
          val *= to_deg;
        } else if (key == 'gamma') {
          val *= to_deg;
        }

        if (sti.hasOwnProperty(key)) {
          output +=
              `<div class="pl-4">${print_label[k]}: ${val} ${unit[k]}</div>`;
        }
      }
    }
  }
  output += `</a></div>`;
  return output;
};


function search() {
  var input, filter, li, i, j, elements1, elements2, elements, txtValue;
  input = document.getElementById('search-isotopomer');
  console.log(input);
  filter = input.value.toUpperCase();
  li = $('#isotopomer-read-only div.display-form ul li');

  // Loop through all list items, and hide those who don't match the search
  // query
  for (i = 0; i < li.length; i++) {
    elements1 = li[i].getElementsByTagName('div');
    elements2 = li[i].getElementsByTagName('b');
    elements = [...elements1, ...elements2];
    for (j = 0; j < elements.length; j++) {
      txtValue = elements[j].textContent || elements[j].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = '';
        break;
      } else {
        li[i].style.display = 'none';
      }
    }
  }
};

var isotopomerOnClick = function(obj) {
  default_li_item_action(obj);

  // store the current-isotopomer-index in the session
  var index = $(obj).index();
  set_isotopomer_index(index);

  // Update the isotopomer fields
  update_field_from_isotopomer_at_index(index);

  // Trigger hide quad for spin-1/2
  hide_quad();
};

var addNewIsotopomer = function() {
  var data = storeData['data'], result, l;
  l = (data == null) ? 0 : data['isotopomers'].length;
  result = {
    'name': `Isotopomer-${l}`,
    'description': '',
    'abundance': 1,
    'sites': [{'isotope': '1H', 'isotropic_chemical_shift': 0}],
  };
  data['isotopomers'].push(result);
  // set_isotopomer_index(l);

  var ul = $('#isotopomer-read-only div.display-form ul');
  var li = document.createElement('li');
  li.innerHTML = update_info(result, l);
  li.className = 'list-group-item';
  console.log(ul);
  ul[0].appendChild(li);
  $(li).click(function() {
    isotopomerOnClick(li)
  });
  li.click();
};
