/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

window.dash_clientside.method = {
  export_simulation_from_selected_method: function (n, data) {
    if (n == null) {
      alert("No method found. Try adding a method first.");
      return "";
    }
    if (data == null) {
      alert("No simulation data available for the method.");
      return "";
    }
    let i = get_method_index();

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

    let dlAnchorElem = $("#export-simulation-from-method-link")[0];
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

/* Method function */
/* Return the selected li index from the methods. */
var get_method_index = function () {
  return storeData.method_index;
};

var set_method_index = function (index) {
  storeData.method_index = index;
};

/* Intiate a click event for the li.
 * @param listomer: A list of li, each summarizing a method.
 * @param index: The index of li to initiate the click.
 */
var select_method = function (listomers, index) {
  if (listomers.length > 0) {
    listomers[index].click();
  }
};

if (!window.methods) {
  window.methods = {};
}
window.methods = {
  setFields: function (index) {
    let data = storeData.data;
    let method = data.methods[index];
    let sd, i, j;
    let ul = $("#dim-tab div div ul.vertical-tabs");
    let li = $("#dim-tab div div ul.vertical-tabs li");
    $("#method-title")[0].innerHTML = method.name;

    // setValue(`method-description`, method.description);
    // setValue(`channel`, method.channels[0]);
    for (i = 0; i < method.spectral_dimensions.length; i++) {
      // show dimension tabs that are applicable for the given method.
      li[i].classList.remove("hide-display");

      sd = method.spectral_dimensions[i];
      setValue(`count-${i}`, sd.count);
      setValue(`spectral_width-${i}`, sd.spectral_width / 1e3); // to kHz
      setValue(`reference_offset-${i}`, sd.reference_offset / 1e3); // to kHz
      // setValue(`origin_offset-${i}`, sd.origin_offset / 1e6); // to MHz
      setValue(`label-${i}`, sd.label);

      for (j = 0; j < sd.events.length; j++) {
        // show events that are applicable for the given method.
        showElement(`event-${i}-${j}`);
        setValue(
          `magnetic_flux_density-${i}-${j}`,
          sd.events[j].magnetic_flux_density
        );
        setValue(
          `rotor_frequency-${i}-${j}`,
          sd.events[j].rotor_frequency / 1e3
        ); // to kHz
        setValue(`rotor_angle-${i}-${j}`, rad_to_deg(sd.events[j].rotor_angle));
        setValue(
          `transition-${i}-${j}`,
          sd.events[j].transition_query["P"]["channel-1"][0][0]
        );
      }
      for (j = sd.events.length; j < 2; j++) {
        // hide events that are not applicable for the given method.
        hideElement(`event-${i}-${j}`);
      }
    }

    // hide the transition symmetry option for the last entry
    // i = method.spectral_dimensions.length - 1;
    // j = method.spectral_dimensions[i].events.length - 1;
    // hideElement(`transition-${i}-${j}-left-label`);
    // hideElement(`transition-${i}-${j}`);
    // hideElement(`transition-${i}-${j}-right-label`);

    // hide dimension tabs that are not applicable for the given method
    for (i = method.spectral_dimensions.length; i < 2; i++) {
      li[i].classList.add("hide-display");
    }
    if (method.spectral_dimensions.length === 1) {
      li[0].children[0].click();
      ul[0].classList.add("hide-display");
    } else {
      ul[0].classList.remove("hide-display");
    }
    data = method = sd = li = ul = null;
  },
  updateData: function () {
    let sd, ev, i, j;
    // let channel = getValue(`channel`);
    // let description = getValue(`method-description`);

    let method = storeData.data.methods[get_method_index()];

    // method.description = description;
    // method.channels = [channel];

    for (i = 0; i < method.spectral_dimensions.length; i++) {
      sd = method.spectral_dimensions[i];
      sd.count = getValue(`count-${i}`);
      sd.spectral_width = getValue(`spectral_width-${i}`) * 1e3; // to Hz
      sd.reference_offset = getValue(`reference_offset-${i}`) * 1e3; // to Hz
      // sd.origin_offset = getValue(`origin_offset-${i}`) * 1e6; // to Hz

      for (j = 0; j < sd.events.length; j++) {
        ev = sd.events[j];
        if (ev.user_variables.includes("magnetic_flux_density")) {
          ev.magnetic_flux_density = getValue(
            `magnetic_flux_density-${i}-${j}`
          ); // in T
        }
        if (ev.user_variables.includes("rotor_angle")) {
          ev.rotor_angle = deg_to_rad(getValue(`rotor_angle-${i}-${j}`)); // in rad
        }
        if (ev.user_variables.includes("rotor_frequency")) {
          ev.rotor_frequency = getValue(`rotor_frequency-${i}-${j}`) * 1e3; // in Hz
        }
        ev.transition_query["P"]["channel-1"][0][0] = getValue(
          `transition-${i}-${j}`
        );
      }
    }
    sd = ev = i = j = null;
    return method;
  },
};

var methodOnClick = function (obj) {
  default_li_item_action(obj);

  // store the current-spin-system-index in the session
  let index = $(obj).index();
  set_method_index(index);

  // Update the method fields
  window.methods.setFields(index);

  // Select the corresponding tr elements
  overView = document.querySelectorAll("[data-table-mth] tr");
  overView.forEach((tr) => {
    tr.classList.remove("active");
  });
  overView[index + 1].classList.add("active");
};

function searchMethods() {
  let input, filter, li, i, j, elements1, elements2, elements, txtValue;
  input = document.getElementById("search-method");
  filter = input.value.toUpperCase();
  li = $("#method-read-only div.display-form ul li");

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

function hideElement(id) {
  var element = document.getElementById(id);
  element.classList.add("hide-display");
}

function showElement(id) {
  var element = document.getElementById(id);
  element.classList.remove("hide-display");
}
