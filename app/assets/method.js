/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu"]
 */

window.dash_clientside.method = {
  export_simulation_from_selected_method: function (n, data, decompose) {
    if (n == null || data == null) {
      throw window.dash_clientside.PreventUpdate;
    }
    let i = get_method_index();
    let j, objLength;

    // get the data corresponding to the selected method.
    let selectedData = data[i];
    console.log(selectedData);

    // if decompose is false, add the data from all dependent variables.
    if (!decompose) {
      let sum, obj, component, ix, len;
      obj = selectedData.csdm.dependent_variables;
      objLength = obj.length;
      // get the data corresponding to the first dependent variable and add the
      // rest to it.
      sum = decodeFromBase64(obj[0].components[0]);
      console.log(sum);
      len = sum.length;
      for (j = objLength; j-- > 1; ) {
        component = decodeFromBase64(obj[j].components[0]);
        for (ix = len; ix-- > 0; ) sum[ix] += component[ix];
        obj.pop();
      }
      console.log(sum);
      let base64String = btoa(
        String.fromCharCode(...new Uint8Array(sum.buffer))
      );
      //   let base64String = Buffer.from(sum.buffer).toString('base64');
      obj[0].components[0] = base64String;
    }

    // prepare the download.
    let dataStr = "data:text/json;charset=utf-8,";
    dataStr += encodeURIComponent(JSON.stringify(selectedData));

    let dlAnchorElem = $("#export-simulation-from-method-link")[0];
    console.log($("#export-simulation-from-method-link")[0]);
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "simulation.csdf");
    dlAnchorElem.click();
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
    let sd, i;
    $("#method-title")[0].innerHTML = method.name;

    setValue(`method-description`, method.description);
    setValue(`channel`, method.channels[0]);
    for (i = 0; i < method.spectral_dimensions.length; i++) {
      sd = method.spectral_dimensions[i];
      setValue(`count-${i}`, sd.count);
      setValue(`spectral_width-${i}`, sd.spectral_width / 1e3); // to kHz
      setValue(`reference_offset-${i}`, sd.reference_offset / 1e3); // to kHz
      setValue(`origin_offset-${i}`, sd.origin_offset / 1e6); // to MHz

      setValue(
        `magnetic_flux_density-${i}`,
        sd.events[0].magnetic_flux_density
      );
      setValue(`rotor_frequency-${i}`, sd.events[0].rotor_frequency / 1e3); // to kHz
      setValue(`rotor_angle-${i}`, rad_to_deg(sd.events[0].rotor_angle));
    }
  },
  updateData: function () {
    let channel = getValue(`channel`);
    let description = getValue(`method-description`);

    let count = getValue(`count-0`);
    let spectral_width = getValue(`spectral_width-0`);
    let reference_offset = getValue(`reference_offset-0`);
    let origin_offset = getValue(`origin_offset-0`);

    let magnetic_flux_density = getValue(`magnetic_flux_density-0`);
    let rotor_angle = getValue(`rotor_angle-0`);
    let rotor_frequency = getValue(`rotor_frequency-0`);
    let dimensions = [
      {
        count: count,
        spectral_width: spectral_width,
        reference_offset: reference_offset,
        origin_offset: origin_offset,
      },
    ];
    return updateMethod(
      dimensions,
      magnetic_flux_density,
      rotor_angle,
      rotor_frequency,
      channel,
      description
    );
  },
};

function updateMethod(
  dimensions,
  magnetic_flux_density,
  rotor_angle,
  rotor_frequency,
  channel,
  description
) {
  let method = storeData.data.methods[get_method_index()];
  let sd, ev, i, j;

  method.description = description;
  method.channels = [channel];

  for (i = 0; i < method.spectral_dimensions.length; i++) {
    sd = method.spectral_dimensions[i];
    sd.count = dimensions[i].count;
    sd.spectral_width = dimensions[i].spectral_width * 1e3; // to Hz
    sd.reference_offset = dimensions[i].reference_offset * 1e3; // to Hz
    sd.origin_offset = dimensions[i].origin_offset * 1e6; // to Hz

    for (j = 0; j < sd.events.length; j++) {
      ev = sd.events[i];
      if (ev.user_variables.includes("magnetic_flux_density")) {
        ev.magnetic_flux_density = magnetic_flux_density; // in T
      }
      if (ev.user_variables.includes("rotor_angle")) {
        ev.rotor_angle = deg_to_rad(rotor_angle); // in rad
      }
      if (ev.user_variables.includes("rotor_frequency")) {
        ev.rotor_frequency = rotor_frequency * 1e3; // in Hz
      }
    }
  }
  return method;
}

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
}
