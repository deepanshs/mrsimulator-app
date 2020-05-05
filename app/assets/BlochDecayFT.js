/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]
 */

const MAGIC_ANGLE = 54.73561;

/* Method function */
/* Return the selected li index from the methods. */
var get_method_index = function() {
  return storeData['method_index'];
};

var set_method_index = function(index) {
  storeData['method_index'] = index;
};

/* Intiate a click event for the li.
 * @param listomer: A list of li, each summarizing a method.
 * @param index: The index of li to initiate the click.
 */
var select_method = function(listomers, index) {
  if (listomers.length > 0) {
    listomers[index].click();
  }
};

if (!window.methods) {
  window.methods = {};
}

function searchMethods() {
  let input, filter, li, i, j, elements1, elements2, elements, txtValue;
  input = document.getElementById('search-method');
  filter = input.value.toUpperCase();
  li = $('#method-read-only div.display-form ul li');

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

window.methods = {
  BlochDecayFT: {
    setData: function(index) {
      let data = storeData['data'], method = data['methods'][index], sd, i;

      $('#method-title')[0].innerHTML = 'BlochDecayFT';

      setValue(`method-description`, method.description);
      setValue(`channel`, method.channels[0]);
      for (i = 0; i < method.spectral_dimensions.length; i++) {
        sd = method.spectral_dimensions[i];
        setValue(`count-${i}`, sd.count);
        setValue(`spectral_width-${i}`, sd.spectral_width / 1e3);      // to kHz
        setValue(`reference_offset-${i}`, sd.reference_offset / 1e3);  // to kHz

        setValue(
            `magnetic_flux_density-${i}`, sd.events[0].magnetic_flux_density);
        setValue(
            `rotor_frequency-${i}`,
            sd.events[0].rotor_frequency / 1e3);  // to kHz
        setValue(`rotor_angle-${i}`, rad_to_deg(sd.events[0].rotor_angle));
      }
    },
    getData: function() {
      let channel = getValue(`channel`);
      let description = getValue(`method-description`);

      let count = getValue(`count-0`);
      let reference_offset = getValue(`reference_offset-0`);
      let spectral_width = getValue(`spectral_width-0`);
      let magnetic_flux_density = getValue(`magnetic_flux_density-0`);
      let rotor_angle = getValue(`rotor_angle-0`);
      let rotor_frequency = getValue(`rotor_frequency-0`);
      let dimensions = [{
        'count': count,
        'spectral_width': spectral_width,
        'reference_offset': reference_offset
      }];
      return this.generateMethod(
          dimensions, magnetic_flux_density, rotor_angle, rotor_frequency,
          channel, description);
    },
    defaultMethod: function() {
      return this.generateMethod(
          [{'count': 2048, 'spectral_width': 25, 'reference_offset': 0}], 9.6,
          MAGIC_ANGLE, 0, '1H', 'Bloch decay Fourier Transform');
    },
    generateMethod: function(
        dimensions, magnetic_flux_density, rotor_angle, rotor_frequency,
        channel, description) {
      let method = {}, sd, ev, i, j;
      method.name = 'BlochDecayFT';
      method.description = description;
      method.channels = [channel];
      method.spectral_dimensions = [];
      for (i = 0; i < 1; i++) {
        sd = {};
        sd.count = dimensions[i].count;
        sd.reference_offset = dimensions[i].reference_offset * 1e3;  // to Hz
        sd.spectral_width = dimensions[i].spectral_width * 1e3;      // to Hz
        sd.label = '';
        sd.events = [];
        for (j = 0; j < 1; j++) {
          ev = {};
          ev.fraction = 1;
          ev.magnetic_flux_density = magnetic_flux_density;  // in T
          ev.rotor_angle = deg_to_rad(rotor_angle);          // in rad
          ev.rotor_frequency = rotor_frequency * 1e3;        // in Hz
          sd.events.push(ev);
        }
        method.spectral_dimensions.push(sd);
      }
      return method;
    }
  }
};
