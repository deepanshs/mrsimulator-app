/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

const ISOTOPE_DATA = [
  "1H",
  "3He",
  "13C",
  "15N",
  "19F",
  "29Si",
  "31P",
  "57Fe",
  "77Se",
  "89Y",
  "103Rh",
  "109Ag",
  "107Ag",
  "111Cd",
  "119Sn",
  "117Sn",
  "115Sn",
  "125Te",
  "129Xe",
  "169Tm",
  "171Yb",
  "183W",
  "187Os",
  "195Pt",
  "199Hg",
  "205Tl",
  "203Tl",
  "207Pb",
];
const to_deg = 180 / 3.14159265359;
const ATTR_PER_SITE = 12;
const euler_angle = ["alpha", "beta", "gamma"];
const ALL_KEYS = [
  "isotope",
  "isotropic_chemical_shift",
  "shielding_symmetric-zeta",
  "shielding_symmetric-eta",
  "shielding_symmetric-alpha",
  "shielding_symmetric-beta",
  "shielding_symmetric-gamma",
  "quadrupolar-Cq",
  "quadrupolar-eta",
  "quadrupolar-alpha",
  "quadrupolar-beta",
  "quadrupolar-gamma",
];

/* Spin system functions */
/* Return the selected li index from the spin-systems. */
var get_spin_system_index = function () {
  return storeData.spin_system_index;
};

var set_spin_system_index = function (index) {
  storeData.spin_system_index = index;
};

/* Initiate a click event for the li.
 * @param listomer: A list of li, each summarizing an spin-system.
 * @param index: The index of li to initiate the click.
 */
var select_spin_system = function (listomers, index) {
  if (listomers.length > 0) {
    listomers[index].click();
  }
};

/* Extract the site attributes and set it to the UI fields.
 * @param site: The site dictionary.
 */
var set_site_attributes = function (site) {
  // isotope and isotropic chemical shift
  setValue("isotope", site.isotope);
  setValue("isotropic_chemical_shift", site.isotropic_chemical_shift);

  // shielding symmetric
  let key = "shielding_symmetric";
  if (site.hasOwnProperty(key)) {
    let ss = site[key];
    setValue(`${key}-zeta`, ss.zeta);
    setValue(`${key}-eta`, ss.eta);
    // Convert Euler angles in radians.
    setValue(
      `${key}-alpha`,
      ss.hasOwnProperty("alpha") ? rad_to_deg(ss.alpha) : null
    );
    setValue(
      `${key}-beta`,
      ss.hasOwnProperty("beta") ? rad_to_deg(ss.beta) : null
    );
    setValue(
      `${key}-gamma`,
      ss.hasOwnProperty("gamma") ? rad_to_deg(ss.gamma) : null
    );
    ss = null;
  } else {
    setValue(`${key}-zeta`, null);
    setValue(`${key}-eta`, null);
    setValue(`${key}-alpha`, null);
    setValue(`${key}-beta`, null);
    setValue(`${key}-gamma`, null);
  }

  // quadrupolar
  key = "quadrupolar";
  if (site.hasOwnProperty(key)) {
    let ss = site[key];
    setValue(`${key}-Cq`, ss.Cq / 1e6); // Convert Cq in MHz.
    setValue(`${key}-eta`, ss.eta);
    // Convert Euler angles in radians.
    setValue(
      `${key}-alpha`,
      ss.hasOwnProperty("alpha") ? rad_to_deg(ss.alpha) : null
    );
    setValue(
      `${key}-beta`,
      ss.hasOwnProperty("beta") ? rad_to_deg(ss.beta) : null
    );
    setValue(
      `${key}-gamma`,
      ss.hasOwnProperty("gamma") ? rad_to_deg(ss.gamma) : null
    );
    ss = null;
  } else {
    setValue(`${key}-Cq`, null);
    setValue(`${key}-eta`, null);
    setValue(`${key}-alpha`, null);
    setValue(`${key}-beta`, null);
    setValue(`${key}-gamma`, null);
  }
  key = null;
};

/* Update the spin-system UI field using the data from the spin-systems dictionary
 * at index, `index`.
 * @param index: The index of the spin-system.
 */
var update_field_from_spin_system_at_index = function (index) {
  let data = storeData.data;
  let spin_system = data.spin_systems[index];

  // name, description, and abundance of the spin_system
  let name = spin_system.name;
  setValue("spin-system-name", name);
  name = name == "" ? `Spin system ${index}` : name;
  $("#spin-system-title")[0].innerHTML = name;

  let description = spin_system.description;
  description = description == null ? "" : description;
  setValue("spin-system-description", description);
  setValue("spin-system-abundance", spin_system.abundance);

  // extract site information
  let site = spin_system.sites[0];
  set_site_attributes(site);
  data = spin_system = name = description = site = null;
};

/* Convert Euler angles from degrees to radians.
 * @params obj: An object dictionary holding the three Euler angles
 */
var euler_angle_deg_to_rad = function (obj) {
  for (let i = 0; i < euler_angle.length; i++) {
    if (obj.hasOwnProperty(euler_angle[i])) {
      obj[euler_angle[i]] /= to_deg;
    }
  }
};

/* Extract the site dictionary from the UI field using the UI ids. */
var extract_site_object_from_fields = function () {
  // Get the spin-systems data from the session storage.
  let data = storeData.data;
  let update = false;
  let temp;
  if (data === null) {
    throw window.dash_clientside.PreventUpdate;
  }
  // Extract the current spin-system index, and get the respective spin-system.
  let index = get_spin_system_index();
  let spin_system = data.spin_systems[index];

  let site_index = 0;
  let old_site = spin_system.sites[site_index];
  let old_site_string = JSON.stringify(old_site);

  // Extract name and description information from the states and update the
  // spin-system object
  temp = getValue("spin-system-name");
  if (spin_system.name != temp) {
    spin_system.name = temp;
    update = true;
  }
  temp = getValue("spin-system-description");
  if (spin_system.description != temp) {
    spin_system.description = temp;
    update = true;
  }
  temp = getValue("spin-system-abundance");
  if (spin_system.abundance != temp) {
    spin_system.abundance = temp;
    update = true;
  }

  let val, id, key, i;
  // Set up a default site dictionary and then populate the key-value pairs.
  let site = {
    isotope: null,
    isotropic_chemical_shift: null,
    shielding_symmetric: {},
    quadrupolar: {},
  };

  for (i = 0; i < ATTR_PER_SITE; i++) {
    id = ALL_KEYS[i];
    val = getValue(id);
    if (val != null) {
      key = id.split("-");
      if (key.length === 1) {
        site[key[0]] = val;
      }
      if (key.length === 2) {
        site[key[0]][key[1]] = val;
      }
    }
  }
  // Convert Euler angles from degrees to radians.
  euler_angle_deg_to_rad(site.shielding_symmetric);
  euler_angle_deg_to_rad(site.quadrupolar);

  // Convert Cq from MHz to Hz.
  if (site.quadrupolar.hasOwnProperty("Cq")) {
    site.quadrupolar.Cq *= 1.0e6;
  }

  // Check if the value of a key is an empty dictionary. If true, remove the
  // respective key-value pair.
  if (Object.keys(site.shielding_symmetric).length === 0) {
    delete site.shielding_symmetric;
  }
  if (Object.keys(site.quadrupolar).length === 0) {
    delete site.quadrupolar;
  }

  let new_site_string = JSON.stringify(site);
  if (old_site_string !== new_site_string) {
    update = true;
  }

  if (!update) {
    throw window.dash_clientside.PreventUpdate;
  }
  // Assign the new site object to the spin-systems at site index 0.
  spin_system.sites[site_index] = site;

  data = update = temp = index = site_index = old_site = old_site_string = null;
  val = id = key = i = site = new_site_string = null;
  return spin_system;
};

print_label = [
  "Isotope",
  "Shift (δ)",
  "ζ",
  "η",
  "α",
  "β",
  "γ",
  "Cq",
  "η",
  "α",
  "β",
  "γ",
];
unit = [null, "ppm", "ppm", "", "°", "°", "°", "MHz", "", "°", "°", "°"];

// var update_info = function (ito, i) {
//   let output = `<div><a>`;
//   let s_len, sto, sti, temp, sites, key, val, j, k;

//   // name
//   temp = `Spin system ${i}`;
//   if (ito.hasOwnProperty("name")) {
//     if (ito.name != "" || ito.name != null) {
//       temp = ito.name;
//     }
//   }
//   output += `<b>${temp}</b>`; // add name

//   // description
//   if (ito.hasOwnProperty("description")) {
//     if (ito.description != "" || ito.description != null) {
//       output += `<div>${ito.description}</div>`; // add description
//     }
//   }

//   // abundance
//   temp = ito.hasOwnProperty("abundance") ? ito.abundance : "100";
//   output += `<div>Abundance: ${parseFloat(temp).toFixed(3)} %</div>`;
//   sites = ito.sites;
//   s_len = sites.length;
//   for (j = 0; j < s_len; j++) {
//     sto = sites[j];

//     output += `<div class="pl-2">Isotope: ${sto.isotope}</div>`;
//     output += `<div class="pl-2">${print_label[1]}: ${sto.isotropic_chemical_shift} ${unit[1]}</div>`;

//     if (sto.hasOwnProperty("shielding_symmetric")) {
//       output += `<div class="pl-2">Symmetric Shielding</div>`;
//       sti = sto.shielding_symmetric;
//       for (k = 2; k < 7; k++) {
//         key = ALL_KEYS[k].split("-")[1];

//         val = sti[key];
//         if (key == "alpha") {
//           val *= to_deg;
//         } else if (key == "beta") {
//           val *= to_deg;
//         } else if (key == "gamma") {
//           val *= to_deg;
//         }

//         if (sti.hasOwnProperty(key)) {
//           output += `<div class="pl-4">${print_label[k]}: ${val} ${unit[k]}</div>`;
//         }
//       }
//     }
//     if (sto.hasOwnProperty("quadrupolar")) {
//       output += `<div class="pl-2">Quadrupolar</div>`;
//       sti = sto.quadrupolar;
//       for (k = 7; k < 12; k++) {
//         key = ALL_KEYS[k].split("-")[1];

//         val = sti[key];
//         if (key == "Cq") {
//           val /= 1e6;
//         } else if (key == "alpha") {
//           val *= to_deg;
//         } else if (key == "beta") {
//           val *= to_deg;
//         } else if (key == "gamma") {
//           val *= to_deg;
//         }

//         if (sti.hasOwnProperty(key)) {
//           output += `<div class="pl-4">${print_label[k]}: ${val} ${unit[k]}</div>`;
//         }
//       }
//     }
//   }
//   output += `</a></div>`;
//   s_len = sto = sti = temp = sites = key = val = j = k = null;
//   return output;
// };

function searchSpinSystems() {
  let input, filter, li, i, j, elements1, elements2, elements, txtValue;
  input = document.getElementById("search-spin-system");
  filter = input.value.toUpperCase();
  li = $("#spin-system-read-only div.display-form ul li");

  // Loop through all list items, and hide those who don't match the search
  // query
  for (i = 0; i < li.length; i++) {
    elements1 = li[i].getElementsByTagName("div");
    elements2 = li[i].getElementsByTagName("b");
    elements = [...elements1, ...elements2];
    for (j = 0; j < elements.length; j++) {
      txtValue = elements[j].textContent || elements[j].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
        break;
      } else {
        li[i].style.display = "none";
      }
    }
  }
  input = filter = li = i = j = elements1 = elements2 = elements = txtValue = null;
}

var spinSystemOnClick = function (obj) {
  default_li_item_action(obj);

  // store the current-spin-system-index in the session
  let index = $(obj).index();
  set_spin_system_index(index);

  // Update the spin-system fields
  update_field_from_spin_system_at_index(index);

  // Trigger hide quad for spin-1/2
  hideQuad();
};

// var addNewSpinSystem = function () {
//   let data = storeData.data;
//   let result, l;
//   l = data == null ? 0 : data.spin_systems.length;
//   result = {
//     name: `Spin system-${l}`,
//     description: "",
//     abundance: 1,
//     sites: [{ isotope: "1H", isotropic_chemical_shift: 0 }],
//   };
//   data.spin_systems.push(result);
//   // set_spin_system_index(l);

//   let ul = $("#spin-system-read-only div.display-form ul");
//   let li = document.createElement("li");
//   li.innerHTML = update_info(result, l);
//   li.className = "list-group-item";
//   ul[0].appendChild(li);
//   $(li).click(function () {
//     spinSystemOnClick(li);
//   });
//   li.click();
//   data = result = l = ul = li = null;
// };
