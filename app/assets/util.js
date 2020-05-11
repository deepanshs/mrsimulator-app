/* Utility function */

/*
 * Author = "Deepansh J. Srivastava"
 * Email = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]
 */

/* Assign the value to the UI fields using UI id.
 * @param id: The id of the UI field.
 * @param val: The value to assign.
 */
var setValue = function(id, val) {
  document.getElementById(id).value = val;
};

/* Get the value from the UI fields using UI id. Convert the value from string
 * to float, if possible.
 * @param id: The id of the UI field.
 */
var getValue = function(id) {
  var val = document.getElementById(id).value;
  if (val.trim() === '') {
    return null;
  };
  return (isNaN(+(val))) ? val : +(val);
};

/* Convert angle from radians to degrees and round to the 10 decimal place. */
function rad_to_deg(angle) {
  angle *= to_deg;
  return Math.round((angle + Number.EPSILON) * 1e10) / 1e10;
}

/* Convert angle from degrees to radians. */
function deg_to_rad(angle) {
  angle /= to_deg;
  return angle;
}

/* Check if two arrays are equal. */
function checkArrayEquality(a, b) {
  if (a.length !== b.length) {
    return false
  };
  let len = a.length;
  for (var i = 0; i < len; i++) {
    if (a[i] !== b[i]) {
      return false;
    }
  }
  return true;
}

function checkObjectEquality(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2)
}
