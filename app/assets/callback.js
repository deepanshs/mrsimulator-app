// clear session storage on refresh
window.sessionStorage.clear();
window.sessionStorage.setItem('current-isotopomer-index', 0)

const ISOTOPE_DATA = ['1H',
    '3He',
    '13C',
    '15N',
    '19F',
    '29Si',
    '31P',
    '57Fe',
    '77Se',
    '89Y',
    '103Rh',
    '109Ag',
    '107Ag',
    '111Cd',
    '119Sn',
    '117Sn',
    '115Sn',
    '125Te',
    '129Xe',
    '169Tm',
    '171Yb',
    '183W',
    '187Os',
    '195Pt',
    '199Hg',
    '205Tl',
    '203Tl',
    '207Pb',
]


const to_deg = 180 / 3.14159265359;
const ATTR_PER_SITE = 12;
var i, j;
const euler_angle = ['alpha', 'beta', 'gamma'];
const ALL_KEYS = ["isotope", "isotropic_chemical_shift", "shielding_symmetric-zeta", "shielding_symmetric-eta", "shielding_symmetric-alpha", "shielding_symmetric-beta", "shielding_symmetric-gamma", "quadrupolar-Cq",
    "quadrupolar-eta", "quadrupolar-alpha", "quadrupolar-beta", "quadrupolar-gamma"
];

if (!window.dash_clientside) { window.dash_clientside = {}; }
window.dash_clientside.clientside = {
    initialize: function (x) {
        // Hide quadrupolar section if the isotope is spin 1/2
        $('#isotope').on('change', function (e) {
            var val;
            $("#isotope option:selected").each(function () {
                val = $(this).text();
            });
            val = this.value;
            console.log('value', val);
            hide_quad();
            e.preventDefault();
        });
        window.onscroll = function () {
            var graph = document.getElementById("spectrum-body");
            var sticky = graph.parentElement.offsetTop;

            if (window.pageYOffset > sticky - 5) {
                graph.classList.add("sticky");
            } else {
                graph.classList.remove("sticky");
            }

            var h = document.getElementById("dimension-body").offsetTop;
            if (window.pageYOffset > h) {
                graph.classList.remove('hide-display')
            }
        };
        return null;
    },
    on_load: function (x, config) {
        var listomers = $('#isotopomer-read-only div.display-form ul li');

        // Clear all previous selections and unbind the click event.
        listomers.each(function () {
            $(this).unbind('click');
        });

        // Add a fresh bind events.
        listomers.each(function () {
            var index = 0;
            $(this).click(function (e) {
                // Toggle classname to slide the contents on smaller screens
                if (document.getElementById('slide').classList.contains("slide-offset")) {
                    document.getElementById('slide').classList.toggle("slide-offset");
                    document.getElementById('slide').classList.toggle("slide");
                }

                // Remove all highlights.
                var ul = this.parentElement;
                for (i = 0; i < ul.childNodes.length; i++) {
                    ul.childNodes[i].classList.remove("display-form-checked");
                }

                // store the current-isotopomer-index in the session
                index = $(this).index();
                set_isotopomer_index(index);

                // Update the isotopomer fields
                update_field_from_isotopomer_at_index(index);

                // Trigger hide quad for spin-1/2
                hide_quad();

                // Scroll to the selection.
                scrollTo(this.parentElement.parentElement.parentElement, this.offsetTop - 50, 300);

                // Highlight the selected list.
                this.classList.toggle("display-form-checked");
                e.preventDefault();
            });
        });

        // Select the entry at index 0 by initiating a click.
        var index = get_isotopomer_index();
        if (config == null) { select_isotopomer(listomers, 0); return null; }
        if (config['is_new_data']) { select_isotopomer(listomers, 0); return null; }
        if (index == null) { return null; }
        select_isotopomer(listomers, index);

        return null;
    },
    create_json: function (n1, n2, n3, n4) {
        // n1 is the trigger time for apply isotopomer changes.
        // n2 is the trigger time for add new isotopomer.
        // n3 is the trigger time for duplicate isotopomer.
        // n4 is the trigger time for delete isotopomer.\
        var max, l, new_val;
        if (n1 == null && n2 == null && n3 == null && n4 == null) {
            throw window.dash_clientside.PreventUpdate;
        }
        if (n1 == null) { n1 = -1; }
        if (n2 == null) { n2 = -1; }
        if (n3 == null) { n3 = -1; }
        if (n4 == null) { n4 = -1; }

        max = Math.max(n1, n2, n3, n4);
        var data = JSON.parse(window.sessionStorage.getItem('local-isotopomers-data'));

        l = (data == null) ? 0 : data['isotopomers'].length;
        var result = {};
        if (n1 == max) { // modify
            result['data'] = extract_site_object_from_fields();
            result['index'] = get_isotopomer_index();
            result['operation'] = 'modify';
        }
        if (n2 == max) { // add
            result['data'] = n2;
            result['index'] = get_isotopomer_index();
            result['operation'] = 'add';
            set_isotopomer_index(l);
        }
        if (n3 == max) { // duplicate
            result['data'] = n3;
            result['index'] = get_isotopomer_index();
            result['operation'] = 'duplicate';
            set_isotopomer_index(l);
        }
        if (n4 == max) { // delete
            result['data'] = n4;
            result['index'] = get_isotopomer_index();
            result['operation'] = 'delete';
            new_val = (result['index'] == l - 1) ? result['index'] - 1 : result['index']
            set_isotopomer_index((new_val < 0) ? null : new_val);
        }
        return result;
    },
    selected_isotopomer: function (clickData, map, decompose) {
        if (clickData == null) { throw window.dash_clientside.PreventUpdate };
        var index = (decompose) ? clickData["points"][0]["curveNumber"] : null;

        var listomers = $('#isotopomer-read-only div.display-form ul li')
        var length = listomers.length

        if (index == null || index >= length) {
            throw window.dash_clientside.PreventUpdate;
        }

        // get the correct index from the mapping array
        index = map[index];

        // highlight the corrresponding isotopomer by initialing a click.
        listomers[index].click();

        return null;
    }
}

/* Hides the quadrupolar attribute from the user, if the isotope is not  quadrupolar. */
var hide_quad = function () {
    var isotope_id = getValue('isotope');
    if (isotope_id === null) { window.dash_clientside.PreventUpdate; }
    quad_collapse = document.getElementById('quadrupolar-feature-collapse');
    if (quad_collapse === null) { window.dash_clientside.PreventUpdate; }
    check_quad = (ISOTOPE_DATA.includes(isotope_id)) ? false : true;
    if (check_quad) {
        quad_collapse.classList.add('show');
        quad_collapse.attributes[2].value = 'true';
    }
    else {
        quad_collapse.classList.remove('show');
        quad_collapse.attributes[2].value = 'false';
    }
}

/* Return the selected li index from the session storage. */
var get_isotopomer_index = function () {
    return parseInt(window.sessionStorage.getItem('current-isotopomer-index'));
}

var set_isotopomer_index = function (index) {
    return window.sessionStorage.setItem('current-isotopomer-index', index);
}

/* Intiate a click event for the li.
 * @param listomer: A list of li, each summarizing an isotopomer.
 * @param index: The index of li to initiate the click.
 */
var select_isotopomer = function (listomers, index) {
    if (listomers.length > 0) { listomers[index].click(); }
}

/* Assign the value to the UI fields using UI id.
 * @param id: The id of the UI field.
 * @param val: The value to assign.
 */
var setValue = function (id, val) { document.getElementById(id).value = val; }

/* Get the value from the UI fields using UI id. Convert the value from string to
 * float, if possible.
 * @param id: The id of the UI field.
 */
var getValue = function (id) {
    var val = document.getElementById(id).value;
    if (val.trim() === "") { return null };
    return (isNaN(+(val))) ? val : +(val)
}

/* Extract the site attributes and set it to the UI fields.
 * @param site: The site dictionary.
 */
var set_site_attributes = function (site) {
    // isotope and isotropic chemical shift
    setValue('isotope', site['isotope']);
    setValue('isotropic_chemical_shift', site['isotropic_chemical_shift']);

    // shielding symmetric
    var key = 'shielding_symmetric';
    if (site.hasOwnProperty(key)) {
        var ss = site[key];
        setValue(`${key}-zeta`, ss['zeta']);
        setValue(`${key}-eta`, ss['eta']);
        // Convert Euler angles in radians.
        setValue(`${key}-alpha`, (ss.hasOwnProperty('alpha')) ? ss['alpha'] * to_deg : null);
        setValue(`${key}-beta`, (ss.hasOwnProperty('beta')) ? ss['beta'] * to_deg : null);
        setValue(`${key}-gamma`, (ss.hasOwnProperty('gamma')) ? ss['gamma'] * to_deg : null);
    }
    else {
        setValue(`${key}-zeta`, null);
        setValue(`${key}-eta`, null);
        setValue(`${key}-alpha`, null);
        setValue(`${key}-beta`, null);
        setValue(`${key}-gamma`, null);
    }

    // quadrupolar
    key = 'quadrupolar';
    if (site.hasOwnProperty(key)) {
        var ss = site[key];
        setValue(`${key}-Cq`, ss['Cq'] / 1e6); // Convert Cq in MHz.
        setValue(`${key}-eta`, ss['eta']);
        // Convert Euler angles in radians.
        setValue(`${key}-alpha`, (ss.hasOwnProperty('alpha')) ? ss['alpha'] * to_deg : null);
        setValue(`${key}-beta`, (ss.hasOwnProperty('beta')) ? ss['beta'] * to_deg : null);
        setValue(`${key}-gamma`, (ss.hasOwnProperty('gamma')) ? ss['gamma'] * to_deg : null);
    }
    else {
        setValue(`${key}-Cq`, null);
        setValue(`${key}-eta`, null);
        setValue(`${key}-alpha`, null);
        setValue(`${key}-beta`, null);
        setValue(`${key}-gamma`, null);
    }
}

/* Update the isotopomer UI field using the data from the isotopomers dictionary
 * at index, `index`.
 * @param index: The index of the isotopomer.
 */
var update_field_from_isotopomer_at_index = function (index) {
    // get the isotopomer dictionary from the session storage
    var data = window.sessionStorage.getItem('local-isotopomers-data');
    var isotopomer = JSON.parse(data)['isotopomers'][index];

    // name, description, and abundance of the isotopomer
    setValue('isotopomer-name', isotopomer['name']);
    setValue('isotopomer-description', isotopomer['description']);
    setValue('isotopomer-abundance', isotopomer['abundance']);

    // extract site information
    var site = isotopomer['sites'][0];
    set_site_attributes(site);
}

/* Convert Euler angles from degrees to radians.
 * @params obj: An object dictionary holding the three Euler angles
 */
var euler_angle_deg_to_rad = function (obj) {
    for (i = 0; i < euler_angle.length; i++) {
        if (obj.hasOwnProperty(euler_angle[i])) {
            obj[euler_angle[i]] /= to_deg;
        }
    }
}

/* Extract the site dictionary from the UI field using the UI ids. */
var extract_site_object_from_fields = function () {
    // Get the isotopomers data from the session storage.
    var data = window.sessionStorage.getItem('local-isotopomers-data');
    if (data === null) {
        throw window.dash_clientside.PreventUpdate;
    }
    // Extract the current isotopomer index, and get the respective isotopomer.
    var index = get_isotopomer_index();
    var isotopomer = JSON.parse(data)['isotopomers'][index];

    // Extract name and description information from the states and update the
    // isotopomer object
    isotopomer["name"] = getValue("isotopomer-name");
    isotopomer["description"] = getValue("isotopomer-description");
    isotopomer["abundance"] = getValue("isotopomer-abundance");

    // Set up a default site dictionary and then populate the key-value pairs.
    var site = {
        'isotope': null, 'isotropic_chemical_shift': null,
        'shielding_symmetric': {}, 'quadrupolar': {}
    };
    var val, id;
    for (i = 0; i < ATTR_PER_SITE; i++) {
        id = ALL_KEYS[i];
        val = getValue(id);
        if (val != null) {
            key = id.split("-");
            if (key.length === 1) { site[key[0]] = val; }
            if (key.length === 2) { site[key[0]][key[1]] = val; }
        }
    }
    // Convert Euler angles from degrees to radians.
    euler_angle_deg_to_rad(site['shielding_symmetric']);
    euler_angle_deg_to_rad(site['quadrupolar']);

    // Convert Cq from MHz to Hz.
    if (site['quadrupolar'].hasOwnProperty('Cq')) {
        site["quadrupolar"]["Cq"] *= 1.0e6;
    }

    // Check if the value of a key is an empty dictionary. If true, remove the
    // respective key-value pair.
    if (Object.keys(site['shielding_symmetric']).length === 0) {
        delete site['shielding_symmetric'];
    }
    if (Object.keys(site['quadrupolar']).length === 0) { delete site['quadrupolar']; }

    // Assign the new site object to the isotopomers at site index 0.
    isotopomer['sites'][0] = site;
    return isotopomer;
}

/* Creates a smooth scroll based on the selected index of li. */
function scrollTo(element, to, duration) {
    var start = element.scrollTop,
        change = to - start,
        currentTime = 0,
        increment = 20;

    var animateScroll = function () {
        currentTime += increment;
        var val = Math.easeInOutQuad(currentTime, start, change, duration);
        element.scrollTop = val;
        if (currentTime < duration) {
            setTimeout(animateScroll, increment);
        }
    };
    animateScroll();
}
//t = current time
//b = start value
//c = change in value
//d = duration
Math.easeInOutQuad = function (t, b, c, d) {
    t /= d / 2;
    if (t < 1) return c / 2 * t * t + b;
    t--;
    return -c / 2 * (t * (t - 2) - 1) + b;
};
