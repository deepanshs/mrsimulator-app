/*
 * Author = "Deepansh J. Srivastava"
 * Email = "srivastava.89@osu.edu"
 */

/* jshint esversion: 6 */

var activateMethodTools = function () {
  const obj = document.querySelectorAll("[data-table-header-mth] li");
  obj.forEach((li, i) => {
    li.addEventListener("click", () => {
      if (i == 0) document.getElementById("add-method-button").click();
      if (i == 1) document.getElementById("duplicate-method-button").click();
      if (i == 2) document.getElementById("remove-method-button").click();
    });
  });
};

// Method operations
// update method
var updateMethod = function () {
  let result = {};
  result.data = window.method.updateFields();
  result.index = window.method.getIndex();
  result.operation = "modify";
  return result;
};

// add method
var addMethod = function (method_template, l) {
  let result = {};
  result.data = method_template.method;
  result.index = l;
  result.operation = "add";
  result.time = Date.now();
  method_template = l = null;
  return result;
};

// copy method
var copyMethod = function (data, l) {
  let result = {};
  checkForEmptyListBeforeOperation("copy", "method", l);
  result.data = data.methods[window.method.getIndex()];
  result.index = l;
  result.operation = "duplicate";
  data = l = null;
  return result;
};

// delete method
var delMethod = function (l) {
  let result = {};
  checkForEmptyListBeforeOperation("delete", "method", l);
  let new_val = window.method.getIndex();
  result.data = Date.now();
  result.index = new_val;
  result.operation = "delete";
  n4 = l = new_val = null;
  return result;
};

var _updateMethodJson = function () {
  const trig_id = ctxTriggerID()[0].split(".")[0].split("-")[0];
  const method_template = ctxTriggerStates()["add-method-from-template.data"];
  const data = storeData.data;
  const l = data.methods.length;
  if (trig_id === "apply") return updateMethod();
  if (trig_id === "add") return addMethod(method_template, l);
  if (trig_id === "duplicate") return copyMethod(data, l);
  if (trig_id === "remove") return delMethod(l);
  return null;
};

var _onMethodsLoad = function () {
  const listomers = document.querySelectorAll(
    "#method-read-only div.scrollable-list ul li"
  );

  let overView = document.querySelectorAll("[data-edit-mth]");
  activatePencilButton(overView, "view-methods");

  overView = document.querySelectorAll("[data-table-mth] thead");
  activateHomeTableElements(overView, listomers);

  // Toggle classnames to slide the contents on smaller screens
  const element = document.getElementById("met-slide");
  toggleClassNamesForSmallerScreens(element, listomers.length);
  updateListEventListener(listomers, window.method.onClick);

  // Select the entry at current index by initiating a click. If the current
  // index is greater then the length of the li, select 0;
  let index = window.method.getIndex();
  index = index >= listomers.length ? 0 : index;
  window.method.select(listomers, index);

  return null;
};

var _setFields = function (index) {
  let data = storeData.data;
  let method = data.methods[index];
  let sd, i, temp; //, array = [];
  document.getElementById("method-title").innerHTML = method.name;

  // noise standard deviation
  if (method.experiment != null) {
    let exp_data = method.experiment.csdm.dependent_variables[0];
    if (exp_data.application == null) {
      exp_data.application = {};
    }
    if (exp_data.application['com.github.DeepanshS.mrsimulator'] == null) {
      exp_data.application['com.github.DeepanshS.mrsimulator'] = {
        'sigma': 1
      };
    }
    let sigma = exp_data.application['com.github.DeepanshS.mrsimulator'].sigma;

    // array.push(sigma);
    setValue("measurement-sigma", sigma);
  }
  temp = parseQuantityValue(method.magnetic_flux_density); // in T
  // array.push(temp);
  setValue("magnetic_flux_density", temp);

  temp = parseQuantityValue(method.rotor_frequency) / 1e3; // to kHz
  // array.push(temp);
  setValue("rotor_frequency", temp);

  temp = rad_to_deg(parseQuantityValue(method.rotor_angle)); // to deg
  // array.push(temp);
  setValue("rotor_angle", temp);

  for (i = 0; i < method.spectral_dimensions.length; i++) {
    sd = method.spectral_dimensions[i];
    // array.push(sd.count);
    setValue(`count-${i}`, sd.count);

    temp = parseQuantityValue(sd.spectral_width) / 1e3; // to kHz
    // array.push(temp);
    setValue(`spectral_width-${i}`, temp);

    temp = parseQuantityValue(sd.reference_offset) / 1e3; // to kHz
    // array.push(temp);
    setValue(`reference_offset-${i}`, temp);
    setValue(`label-${i}`, sd.label);
  }

  // show/hide desired number of dimensions.
  let dimUI, n_dim = method.spectral_dimensions.length;
  let total = 2;
  for (i = 0; i < total; i++) {
    dimUI = document.getElementById(`dim-${i}-feature-collapse`);
    if (i < n_dim) dimUI.classList.add("show");
    else dimUI.classList.remove("show");
  }
  data = method = sd = null;
};

window.dash_clientside.method = {
  updateMethodJson: _updateMethodJson,
  onMethodsLoad: _onMethodsLoad,
  // export_simulation_from_selected_method: function (n, data) {
  //   if (n === null) {
  //     alert("No method found. Try adding a method first.");
  //     return "";
  //   }
  //   if (data === null) {
  //     alert("No simulation data available for the method.");
  //     return "";
  //   }

  //   // prepare the download.
  //   let dataStr = "data:text/json;charset=utf-8,";
  //   dataStr += encodeURIComponent(JSON.stringify(data));

  //   let dlAnchorElem = document.getElementById(
  //     "export-simulation-from-method-link"
  //   );
  //   dlAnchorElem.setAttribute("href", dataStr);
  //   dlAnchorElem.setAttribute("download", "simulation.csdf");
  //   dlAnchorElem.click();

  //   dataStr = ndlAnchorElem = null;
  //   return "";
  // },
};

var decodeFromBase64 = function (encodedString) {
  let binary_string = atob(encodedString);
  let buffer = new ArrayBuffer(binary_string.length);
  let bytes_buffer = new Uint8Array(buffer);

  for (let i = 0; i < binary_string.length; i++) {
    bytes_buffer[i] = binary_string.charCodeAt(i);
  }
  return new Float64Array(buffer);
};

/* Initiate a click event for the li.
 * @param listomers: A list of li, each summarizing a method.
 * @param index: The index of li to initiate the click.
 */

if (!window.method) {
  window.method = {};
}
window.method = {
  getIndex: function () {
    return storeData.method_index;
  },

  setIndex: function (index) {
    storeData.method_index = index;
    document.getElementById("force-refresh-method").click();
  },

  select: function (listomers, index) {
    if (listomers == null) {
      listomers = document.querySelectorAll(
        "#method-read-only div.scrollable-list ul li"
      );
    }
    if (listomers.length > 0) {
      listomers[index].click();
    }
  },

  onClick: function (index) {
    // store the current-spin-system-index in the session
    window.method.setIndex(index);

    // Update the method fields
    window.method.setFields(index);

    // Select the corresponding tr elements
    let overView = document.querySelectorAll("[data-table-mth] thead");
    overView.forEach((tr) => {
      tr.classList.remove("active");
    });
    overView[index + 1].classList.add("active");

    // Select updates method in features tab
    window.features.selectMethod(index);
  },

  setFields: _setFields,

  updateFields: function () {
    let sd, i, temp;
    let method = storeData.data.methods[window.method.getIndex()];

    // noise standard deviation
    if (method.experiment != null) {
      temp = getValue('measurement-sigma');
      let exp_data = method.experiment.csdm.dependent_variables[0];
      if (exp_data.application == null) {
        exp_data.application = {};
      }
      if (exp_data.application['com.github.DeepanshS.mrsimulator'] == null) {
        exp_data.application['com.github.DeepanshS.mrsimulator'] = {};
      }
      exp_data.application['com.github.DeepanshS.mrsimulator'].sigma = temp;
    }

    temp = getValue('magnetic_flux_density');
    method.magnetic_flux_density = toQuantityValue(temp, "T");

    temp = deg_to_rad(getValue('rotor_angle'));
    method.rotor_angle = toQuantityValue(temp, "rad");

    temp = getValue('rotor_frequency') * 1e3; // to Hz
    method.rotor_frequency = toQuantityValue(temp, "Hz");

    for (i = 0; i < method.spectral_dimensions.length; i++) {
      sd = method.spectral_dimensions[i];
      sd.count = getValue(`count-${i}`);

      temp = getValue(`spectral_width-${i}`) * 1e3; // to Hz
      sd.spectral_width = toQuantityValue(temp, "Hz");

      temp = getValue(`reference_offset-${i}`) * 1e3; // to Hz
      sd.reference_offset = toQuantityValue(temp, "Hz");
    }
    sd = i = null;
    return method;
  },
};

function searchMethods() {
  let input, filter, li, i, j, elements1, elements2, elements, txtValue;
  input = document.getElementById("search-method");
  filter = input.value.toUpperCase();
  li = document.querySelectorAll("#method-read-only div.scrollable-list ul li");

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
