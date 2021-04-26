/* Utility function */

/*
 * Author = "Deepansh J. Srivastava"
 * Email = "srivastava.89@osu.edu"
 */
/* jshint esversion: 6 */

/* Assign the value to the UI fields using UI id.
 * @param id: The id of the UI field.
 * @param val: The value to assign.
 */
const TO_DEG = 180 / 3.14159265359;

var setValue = function (id, val) {
  document.getElementById(id).value = val;
};

var parseQuantityValue = function (val) {
  val = (val == null) ? val : val.split(" ")[0];
  return isNaN(+val) ? val : +val;
  // document.getElementById(id).value = val;
};

/* Get the value from the UI fields using UI id. Convert the value from string
 * to float, if possible.
 * @param id: The id of the UI field.
 */
var getValue = function (id) {
  let element = document.getElementById(id);
  if (element.validity.valid == false) {
    alert(`Invalid value encounter.`);
    throw window.dash_clientside.PreventUpdate;
  }
  let val = element.value;
  if (val.trim() === "") return null;
  return isNaN(+val) ? val : +val;
};

var toQuantityValue = function (val, unit) {
  if (val === null) return null;
  return val.toString().concat(` ${unit}`).trim();
};

/* Convert angle from radians to degrees and round to the 10 decimal place. */
function rad_to_deg(angle) {
  return Math.round((angle * TO_DEG + Number.EPSILON) * 1e10) / 1e10;
}

/* Convert angle from degrees to radians. */
function deg_to_rad(angle) {
  return angle / TO_DEG;
}

/* Check if two arrays are equal. */
function checkArrayEquality(a, b) {
  if (a.length !== b.length) {
    return false;
  }
  let len = a.length;
  for (var i = 0; i < len; i++) {
    if (a[i] !== b[i]) {
      return false;
    }
  }
  return true;
}

function checkObjectEquality(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}
