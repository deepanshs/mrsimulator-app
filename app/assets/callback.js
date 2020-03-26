
const ATTR_PER_SITE = 12;
var i, j;
const ALL_KEYS = ["isotope", "isotropic_chemical_shift", "shielding_symmetric-zeta", "shielding_symmetric-eta", "shielding_symmetric-alpha", "shielding_symmetric-beta", "shielding_symmetric-gamma", "quadrupolar-Cq",
    "quadrupolar-eta", "quadrupolar-alpha", "quadrupolar-beta", "quadrupolar-gamma"
];

if (!window.dash_clientside) { window.dash_clientside = {}; }
window.dash_clientside.clientside = {
    update_isotopomer_dropdown_options: function (local_isotopomer_data) {
        var options = [];
        if (local_isotopomer_data == null) {
            return options;
        }
        var isotopomer = local_isotopomer_data["isotopomers"]
        var site_isotope;
        for (i = 0; i < isotopomer.length; i++) {
            site_isotope = "Isotopomer-" + i.toString() + ' (';
            for (j = 0; j < isotopomer[i]['sites'].length; j++) {
                site_isotope += isotopomer[i]['sites'][j]['isotope'] + '-';
            }
            site_isotope = site_isotope.slice(0, -1) + ')'
            options.push({
                "label": site_isotope,
                "value": i,
            });
        }
        return options;
    },
    populate_isotopomer_fields: function (index, is_advanced_editor_open, local_isotopomer_data) {
        // Extract the values from the local isotopomer data and populate the input fields
        // in the isotopomer UI.
        // # The argument `is_advanced_editor_open` is for checking if the fields are in view.
        // # If this argument is true, the advanced editor is open and, therefore, the
        // # isotopomer UI fields are hidden. In this case, we want to prevent any updates
        // # from the `populate_isotopomer_fields` (this function) to improve the performance.
        var trigger_values = [];
        if (is_advanced_editor_open) {
            throw window.dash_clientside.PreventUpdate;
        }
        if (local_isotopomer_data == null) {
            for (i = 0; i < ATTR_PER_SITE; i++) {
                trigger_values.push(window.dash_clientside.no_update);
            }
            return trigger_values;
        }

        for (i = 0; i < ATTR_PER_SITE; i++) {
            trigger_values.push(null);
        }
        if (is_advanced_editor_open | local_isotopomer_data == null | index == null) {
            return trigger_values;
        }


        var site = local_isotopomer_data["isotopomers"][index]["sites"][0]
        var root_keys = Object.keys(site);
        i = 0;
        var k0, k1;
        for (ids in ALL_KEYS) {
            keys = ALL_KEYS[ids].split("-");
            k0 = keys[0];
            // when only one key is present, use the value of site[site_index][key1]
            if (keys.length == 1) {
                if (root_keys.includes(k0)) {
                    trigger_values[i] = site[k0]
                }
            }

            // when two keys are present, use the value of site[site_index][key1][key2]
            if (keys.length == 2) {
                k1 = keys[1];
                if (root_keys.includes(k0)) {
                    if (site[k0] != null) {
                        if (Object.keys(site[k0]).includes(k1)) {
                            trigger_values[i] = site[k0][k1];
                        }
                    }
                }
            }
            i += 1;
        }
        // values = extract_isotopomer_UI_field_values_from_dictionary(
        //     local_isotopomer_data["isotopomers"][index]["sites"][0]
        // )
        return trigger_values;
    }
}

// import React from 'react';
// class Input extends React.Component {
//     componentDidMount() {
//         jQuery('.numbersOnly').keyup(function () {
//             window.write('blah')
//             this.value = this.value.replace(/[^0-9\.]/g, '');
//         });
//     }
// }



// function init() {
//     mouseCtrl("ictrl", getFloatCtrl, scaledIntCtrl);
// }
// function getFloatCtrl(o) { return (parseFloat(o.value)); }
// function getIntCtrl(o) { return (parseInt(o.value)); }
// function mouseCtrl(n, getCtrl, setCtrl) {
//     var ctrl; // DOM object for the input control
//     var startpos; // starting mouse position
//     var startval; // starting input control value
//     // find the input element to allow mouse control on
//     ctrl = document.getElementById(n);
//     // on mousedown start tracking mouse relative position
//     ctrl.onmousedown = function (e) {
//         startpos = e.clientX;
//         startval = getCtrl(ctrl);
//         if (isNaN(startval)) startval = 0;
//         document.onmousemove = function (e) {
//             var delta = Math.ceil(e.clientX - startpos);
//             setCtrl(ctrl, startval, delta);
//         };
//         document.onmouseup = function () {
//             document.onmousemove = null; // remove mousemove to stop tracking
//         };
//     };
//     /*
//     ctrl.addEventListener('touchstart', function(e) {
//       e.preventDefault();
//       startpos = e.touches[0].pageX;
//       startval = getCtrl(ctrl);
//     }, false);
//     ctrl.addEventListener('touchmove', function(e) {
//       e.preventDefault();
//       var delta = Math.ceil(e.touches[0].clientX - startpos);
//       setCtrl(ctrl, startval, delta);
//     }, false);
//     */
// }

// // takes current value and relative mouse coordinate as arguments
// function scaledIntCtrl(o, i, x) {
//     var incVal = Math.round(Math.sign(x) * Math.pow(Math.abs(x) / 10, 1.6));
//     document.getElementById("log").innerHTML = (x + ' ' + incVal + ", i=" + i);
//     var newVal = i + incVal;
//     if (newVal < 0) newVal = 0;
//     if (Math.abs(incVal) > 1) o.value = newVal; // allow small deadzone
// }

// if (window.addEventListener) { /*W3C*/ window.addEventListener('load', init, false) }
// else if (window.attachEvent) { /*MS*/  window.attachEvent('onload', init) }
// else { /*def*/ window.onload = init }
