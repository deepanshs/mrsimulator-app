/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

/* jshint esversion: 6 */

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

if (!window.spinSystem) {
  window.spinSystem = {};
}

window.spinSystem = {
  getIndex: function () {
    return storeData.spin_system_index;
  },

  setIndex: function (index) {
    storeData.spin_system_index = index;
  },
  select: function (listomers, index) {
    if (listomers.length > 0) {
      listomers[index].click();
    }
  },
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
  document.getElementById("spin-system-title").innerHTML = name;

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
  let index = window.spinSystem.getIndex();
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

var spinSystemOnClick = function (obj, index) {
  default_li_item_action(obj);

  // store the current-spin-system-index in the session
  window.spinSystem.setIndex(index);

  // Update the spin-system fields
  update_field_from_spin_system_at_index(index);

  // Trigger hide quad for spin-1/2
  hideQuad();

  // Select the corresponding tr elements
  overView = document.querySelectorAll("[data-table-sys] tr");
  overView.forEach((tr) => {
    tr.classList.remove("active");
  });
  overView[index + 1].classList.add("active");
};

var activateSystemTools = function () {
  const obj = document.querySelectorAll("[data-table-header-sys] li");
  obj.forEach((li, i) => {
    li.addEventListener("click", () => {
      if (i == 0) document.getElementById("add-spin-system-button").click();
      if (i == 1)
        document.getElementById("duplicate-spin-system-button").click();
      if (i == 2) document.getElementById("remove-spin-system-button").click();
    });
  });
};

// update system
var updateSystem = function () {
  let result = {};
  result.data = extract_site_object_from_fields();
  result.index = window.spinSystem.getIndex();
  result.operation = "modify";
  return result;
};

// add system
var addSystem = function (l) {
  let result = {};
  result.data = {
    name: `System ${l}`,
    description: "",
    abundance: 1,
    sites: [{ isotope: "1H", isotropic_chemical_shift: 0 }],
  };
  result.index = l;
  result.operation = "add";
  result.time = Date.now();
  l = null;
  return result;
};

// copy system
var copySystem = function (data, l) {
  let result = {};
  checkForEmptyListBeforeOperation("copy", "spin system", l);
  result.data = data.spin_systems[window.spinSystem.getIndex()];
  result.index = l;
  result.operation = "duplicate";
  data = l = null;
  return result;
};

// delete system
var delSystem = function (l) {
  let result = {};
  checkForEmptyListBeforeOperation("delete", "spin system", l);
  let new_val = window.spinSystem.getIndex();
  console.log("index to remove", new_val);
  result.data = null;
  result.index = new_val;
  result.operation = "delete";
  l = new_val = null;
  return result;
};

var _updateSpinSystemJson = function () {
  const trig_id = ctxTriggerID()[0].split(".")[0].split("-")[0];
  const data = storeData.data;
  const l = data.spin_systems.length;
  if (trig_id === "apply") return updateSystem();
  if (trig_id === "add") return addSystem(l);
  if (trig_id === "duplicate") return copySystem(data, l);
  if (trig_id === "remove") return delSystem(l);
  return null;
};

// Search spin systems
var _searchSpinSystems = function (input) {
  let filter, li, i, j, elements1, elements2, elements, txtValue;
  filter = input.toUpperCase();
  li = document.querySelectorAll(
    "#spin-system-read-only div.scrollable-list ul li"
  );

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
  filter = li = i = j = elements1 = elements2 = elements = txtValue = null;
  throw window.dash_clientside.PreventUpdate;
};

var _onSpinSystemsLoad = function () {
  storeData.data = JSON.parse(
    window.sessionStorage.getItem("local-mrsim-data")
  );
  const listomers = document.querySelectorAll(
    "#spin-system-read-only div.scrollable-list ul li"
  );

  // event listener to pensil in the home screen
  let overView = document.querySelectorAll("[data-edit-sys]");
  overView.forEach((edit) => {
    edit.addEventListener("click", () => {
      document.getElementById("view-spin_systems").click();
    });
  });

  // event listener to side panel click and update the site fields.
  overView = document.querySelectorAll("[data-table-sys] thead");
  overView.forEach((tr, i) => {
    tr.addEventListener("click", () => {
      listomers[i - 1].click();
      // Scroll to the selection.
      let ul = listomers[i - 1].parentElement;
      scrollTo(
        ul.parentElement.parentElement,
        listomers[i - 1].offsetTop - 200,
        300,
        "vertical"
      );
    });
  });

  // Toggle classname to slide the contents on smaller screens
  const element = document.getElementById("iso-slide");
  if (element.classList.contains("slide-offset")) {
    element.classList.toggle("slide-offset");
    element.classList.toggle("slide");
  }

  // Toggle classname to slide the contents on smaller screens
  if (listomers.length === 0) {
    element.classList.toggle("slide-offset");
    element.classList.toggle("slide");
  }

  default_li_action(listomers);

  // Add a fresh bind event to the list.
  listomers.forEach((tr, i) => {
    tr.addEventListener("click", (event) => {
      spinSystemOnClick(tr, i);
      event.preventDefault();
    });
  });

  // Select the entry at current index by initiating a click. If the current
  // index is greater then the length of the li, select 0;
  let index = window.spinSystem.getIndex();
  index = index >= listomers.length ? 0 : index;
  window.spinSystem.select(listomers, index);
  return null;
};

window.dash_clientside.spin_system = {
  searchSpinSystems: _searchSpinSystems,
  updateSpinSystemJson: _updateSpinSystemJson,
  onSpinSystemsLoad: _onSpinSystemsLoad,
};
