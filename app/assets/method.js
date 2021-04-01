/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
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
  result.data = window.method.updateData();
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
  result.data = null;
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
  storeData.data = JSON.parse(
    window.sessionStorage.getItem("local-mrsim-data")
  );
  const listomers = document.querySelectorAll(
    "#method-read-only div.scrollable-list ul li"
  );

  let overView = document.querySelectorAll("[data-edit-mth]");
  overView.forEach((edit) => {
    edit.addEventListener("click", () => {
      document.getElementById("view-methods").click();
    });
  });

  overView = document.querySelectorAll("[data-table-mth] thead");
  overView.forEach((tr, i) => {
    tr.addEventListener("click", () => {
      overView.forEach((tr) => {
        tr.classList.remove("active");
      });
      tr.classList.add("active");
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

  // activte the add, copy, and remove btn on the home page.
  // activateMethodTools();

  // Toggle classname to slide the contents on smaller screens
  const element = document.getElementById("met-slide");
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
      window.method.onClick(tr, i);
      event.preventDefault();
    });
  });

  // Select the entry at current index by initiating a click. If the current
  // index is greater then the length of the li, select 0;
  let index = window.method.getIndex();
  index = index >= listomers.length ? 0 : index;
  window.method.select(listomers, index);
  return null;
};

window.dash_clientside.method = {
  updateMethodJson: _updateMethodJson,
  onMethodsLoad: _onMethodsLoad,
  export_simulation_from_selected_method: function (n, data) {
    if (n == null) {
      alert("No method found. Try adding a method first.");
      return "";
    }
    if (data == null) {
      alert("No simulation data available for the method.");
      return "";
    }
    let i = window.method.getIndex();

    // get the data corresponding to the selected method.
    let selectedData = data[i];

    // // if decompose is false, add the data from all dependent variables.
    // if (!decompose) {
    //   let sum, obj, component, ix, len;
    //   obj = selectedData.csdm.dependent_variables;
    //   objLength = obj.length;
    //   // get the data corresponding to the first dependent variable and add the
    //   // rest to it.
    //   sum = decodeFromBase64(obj[0].components[0]);
    //   console.log(sum);
    //   len = sum.length;
    //   for (j = objLength; j-- > 1; ) {
    //     component = decodeFromBase64(obj[j].components[0]);
    //     for (ix = len; ix-- > 0; ) sum[ix] += component[ix];
    //     obj.pop();
    //   }
    //   console.log(sum);
    //   let base64String = btoa(
    //     String.fromCharCode(...new Uint8Array(sum.buffer))
    //   );
    //   //   let base64String = Buffer.from(sum.buffer).toString('base64');
    //   obj[0].components[0] = base64String;
    // }

    // prepare the download.
    let dataStr = "data:text/json;charset=utf-8,";
    dataStr += encodeURIComponent(JSON.stringify(selectedData));

    let dlAnchorElem = document.getElementById(
      "export-simulation-from-method-link"
    );
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "simulation.csdf");
    dlAnchorElem.click();

    dataStr = ndlAnchorElem = null;
    return "";
  },
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

/* Intiate a click event for the li.
 * @param listomer: A list of li, each summarizing a method.
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
  },

  select: function (listomers, index) {
    if (listomers.length > 0) {
      listomers[index].click();
    }
  },

  onClick: function (obj, index) {
    default_li_item_action(obj);

    // store the current-spin-system-index in the session
    window.method.setIndex(index);

    // Update the method fields
    window.method.setFields(index);

    // Select the corresponding tr elements
    let overView = document.querySelectorAll("[data-table-mth] tr");
    overView.forEach((tr) => {
      tr.classList.remove("active");
    });
    overView[index + 1].classList.add("active");
  },

  setFields: function (index) {
    let data = storeData.data;
    let method = data.methods[index];
    let sd, i;
    document.getElementById("method-title").innerHTML = method.name;

    let evt = method.spectral_dimensions[0].events[0];
    setValue("magnetic_flux_density", evt.magnetic_flux_density);
    setValue("rotor_frequency", evt.rotor_frequency / 1e3); // to kHz
    setValue("rotor_angle", rad_to_deg(evt.rotor_angle));

    // setValue(`method-description`, method.description);
    // setValue(`channel`, method.channels[0]);
    for (i = 0; i < method.spectral_dimensions.length; i++) {
      // show dimension tabs that are applicable for the given method.
      // li[i].classList.remove("hide-display");

      sd = method.spectral_dimensions[i];
      setValue(`count-${i}`, sd.count);
      setValue(`spectral_width-${i}`, sd.spectral_width / 1e3); // to kHz
      setValue(`reference_offset-${i}`, sd.reference_offset / 1e3); // to kHz
      setValue(`label-${i}`, sd.label);

      // for (j = 0; j < sd.events.length; j++) {
      //   // show events that are applicable for the given method.
      //   showElement(`event-${i}-${j}`);
      //   setValue(
      //     `magnetic_flux_density-${i}-${j}`,
      //     sd.events[j].magnetic_flux_density
      //   );
      //   setValue(
      //     `rotor_frequency-${i}-${j}`,
      //     sd.events[j].rotor_frequency / 1e3
      //   ); // to kHz
      //   setValue(`rotor_angle-${i}-${j}`, rad_to_deg(sd.events[j].rotor_angle));
      //   // setValue(
      //   //   `transition-${i}-${j}`,
      //   //   sd.events[j].transition_query["P"]["channel-1"][0][0]
      //   // );
      // }
      // for (j = sd.events.length; j < 2; j++) {
      //   // hide events that are not applicable for the given method.
      //   hideElement(`event-${i}-${j}`);
      // }
    }

    // hide the transition symmetry option for the last entry
    // i = method.spectral_dimensions.length - 1;
    // j = method.spectral_dimensions[i].events.length - 1;
    // hideElement(`transition-${i}-${j}-left-label`);
    // hideElement(`transition-${i}-${j}`);
    // hideElement(`transition-${i}-${j}-right-label`);

    // hide dimension tabs that are not applicable for the given method
    // for (i = method.spectral_dimensions.length; i < 2; i++) {
    //   li[i].classList.add("hide-display");
    // }
    // if (method.spectral_dimensions.length === 1) {
    //   li[0].children[0].click();
    //   ul[0].classList.add("hide-display");
    // } else {
    //   ul[0].classList.remove("hide-display");
    // }
    data = method = sd = null;
  },

  updateData: function () {
    let sd, i;
    // let channel = getValue(`channel`);
    // let description = getValue(`method-description`);

    let method = storeData.data.methods[window.method.getIndex()];

    let evt = method.spectral_dimensions[0].events[0];
    evt.magnetic_flux_density = getValue(`magnetic_flux_density`); // in T
    evt.rotor_angle = deg_to_rad(getValue(`rotor_angle`)); // in rad
    evt.rotor_frequency = getValue(`rotor_frequency`) * 1e3; // in Hz
    // method.description = description;
    // method.channels = [channel];
    // global params
    for (i = 0; i < method.spectral_dimensions.length; i++) {
      sd = method.spectral_dimensions[i];
      sd.count = getValue(`count-${i}`);
      sd.spectral_width = getValue(`spectral_width-${i}`) * 1e3; // to Hz
      sd.reference_offset = getValue(`reference_offset-${i}`) * 1e3; // to Hz
      // sd.origin_offset = getValue(`origin_offset-${i}`) * 1e6; // to Hz

      // for (j = 0; j < sd.events.length; j++) {
      //   ev = sd.events[j];
      //   ev.magnetic_flux_density = getValue(`magnetic_flux_density-${i}-${j}`); // in T
      //   ev.rotor_angle = deg_to_rad(getValue(`rotor_angle-${i}-${j}`)); // in rad
      //   ev.rotor_frequency = getValue(`rotor_frequency-${i}-${j}`) * 1e3; // in Hz
      //   // ev.transition_query["P"]["channel-1"][0][0] = getValue(
      //   //   `transition-${i}-${j}`
      //   // );
      // }
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
