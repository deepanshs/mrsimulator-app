/*
 * Author = "Matthew D. Giammar"
 * Email = "giammar.7@osu.edu"
 */

/* jshint esversion: 6 */

/**
 * Example structure
 *
 *  methods: [
 *      {
 *          "mth_0_rotor_frequency": [
 *              5000,  // value
 *              true,  // vary
 *              null,  // expr
 *              4900,  // min
 *              5100,  // max
 *              (the following are stored but not used)
 *              null,  // brute_step
 *              null,  // stderr
 *              null,  // correl
 *              5000,  // init_value
 *              null,  // user_data
 *          ],
 *          "SP_0_operation_0_Scale_factor": [...],
 *          ...
 *          (more params)
 *      },
 *      ...
 *      (more methods)
 *  ]
 */
var paramGroups = {
    modal_name: null,
    spin_systems: [],
    methods: [],
};
const sysPrefix = ["sys"];
const mthPrefix = ["mth", "SP"];


/**
 * Takes JSON representation of LMFIT Parameters object
 * and groups Parameter objects into spin_systems and methods.
 *
 * @param {Object} _mrsim_data local-mrsim-data (unused)
 */
var _reloadParamGroups = function (_mrsim_data) {
    console.log("_reloadParamGroups");

    // Logic for creating params JSON if not already present
    if (!storeData.data.params) {  // true if 'null', 'undefined' or empty str
        // Create params JSON if at least 1 spin_system and 1 method
        if (storeData.data.methods.length && storeData.data.spin_systems.length) {
            document.getElementById("make-lmfit-params").click();
        }
        throw window.dash_clientside.PreventUpdate;
    }

    // Get stored json string
    params_json = storeData.data.params;

    // Remove old stored params
    paramGroups = {
        modal_name: null,
        spin_systems: [],
        methods: [],
    };

    // Clean 'NaN' and 'Infinity' out of JSON string.
    params_json = params_json.replaceAll("NaN", null);
    params_json = params_json.replaceAll("-Infinity", null);
    params_json = params_json.replaceAll("Infinity", null);
    params = JSON.parse(params_json).params;

    // Add dict elements to storage array
    let num_sys = storeData.data.spin_systems.length;
    let num_mth = storeData.data.methods.length;
    for (num_sys; num_sys > 0; num_sys--) {
        paramGroups.spin_systems.push({});
    }
    for (num_mth; num_mth > 0; num_mth--) {
        paramGroups.methods.push({});
    }

    // Iterate through parameters and add representations to list
    for (const element of params) {
        const prefix = element[0].split("_")[0];
        const idx = Number(element[0].split("_")[1]);

        // Add to spin_systems
        if (sysPrefix.includes(prefix)) {
            paramGroups.spin_systems[idx][element[0]] = element.slice(1);
        }

        // Add to methods
        if (mthPrefix.includes(prefix)) {
            paramGroups.methods[idx][element[0]] = element.slice(1);
        }
    }

    // console.log(paramGroups);
};


/**
 * Refreshes held values of both tabels
 *
 * @param {Number} sys_idx index of current system table
 * @param {Number} mth_idx index of current method table
 */
var _refreshTables = function (_n1, _n2, sys_idx, mth_idx) {
    if (sys_idx == null) {
        sys_idx = 0;
    }
    if (mth_idx == null) {
        mth_idx = 0;
    }
    loadSys(sys_idx);
    loadMth(mth_idx);
}


/**
 * Serializes paramGroups variable into LMFIT compliant JSON string
 *
 * @param {String} old_json JSON of currently held Parameters obj
 * @returns {String} updated JSON
 */
var _serializeParamGroups = function () {
    console.log("_serializeParamGroups");

    old_json = storeData.data.params;

    // Make temporary array for parameters
    let tmp_arr = [];

    // Iterate through spin_systems
    paramGroups.spin_systems.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
            // Replace null min/max with str to replace in json
            if (tmp[4] == null) {
                tmp[4] = -Infinity;
            }
            if (tmp[5] == null) {
                tmp[5] = Infinity;
            }
            tmp_arr.push(tmp);
        }
    });

    // Iterate through methods
    paramGroups.methods.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
            // Replace null min/max with +-Infinity
            if (tmp[4] == null) {
                tmp[4] = -Infinity;
            }
            if (tmp[5] == null) {
                tmp[5] = Infinity;
            }
            tmp_arr.push(tmp);
        }
    });

    let new_json = '"params":' + JSON.stringify(tmp_arr);


    // Replace "params" key in old data with new json
    old_json = old_json.substring(0, old_json.indexOf('"params":'));
    return old_json + new_json + "}";
};


/**
 * Serialize data in tables and trigger a simulation or fit
 *
 * @param {String} which flag for which to trigger ("sim" or "fit")
 * @returns
 */
var _triggerSimOrFit = function (_trig, which) {
    console.log("_triggerSimOrFit");
    saveSys();
    saveMth();

    console.log(which)

    let new_data = _serializeParamGroups();
    if (which == "sim") {
        return [new_data, Date.now(), window.dash_clientside.no_update];
    }
    if (which == "fit") {
        return [new_data, window.dash_clientside.no_update, Date.now()];
    }
    console.log("which not recognized");
    throw window.dash_clientside.PreventUpdate;
}


// Reduce resuded code by completing this method
/**
 *
 * @param {tbody} rows HTML tbody element to add param rows to
 * @param {Object} params
 */
var updateRows = function (rows, params) {
    // Remove currently stored rows
    while (rows.hasChildNodes()) {
        rows.removeChild(rows.lastChild);
    }

    // Check if rows is none
    if (rows == null) {
        console.log("Rows is undefined. Halting update");
        throw window.dash_clientside.PreventUpdate;
    }

    // Check if params is none
    if (params == null) {
        console.log("Params is undefined. Halting update");
        throw window.dash_clientside.PreventUpdate;
    }

    // Iteerate through relevent stored parameters and update values
    for (const [key, value] of Object.entries(params)) {
        let new_row = rows.insertRow();

        // Add checkbox
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = value[1];
        new_row.insertCell().appendChild(checkbox);

        // Add name
        let name = new_row.insertCell();
        name.textContent = key;

        // Add value
        let val = document.createElement("input");
        val.type = "number";
        val.step = "any";
        val.value = value[0];
        new_row.insertCell().appendChild(val);

        // More options button
        let button = document.createElement("span");
        let icon = document.createElement("i");
        icon.className = "fas fa-sliders-h";
        button.appendChild(icon);
        button.setAttribute("data-edit-fit", "");
        button.onclick = function () {
            paramGroups.modal_name = key;
            document.getElementById("open-features-modal").click();
        }
        // button.id = `{'param':'${key}'}`  // NOTE: Single quotes here required

        new_row.insertCell().appendChild(button);
    }
};


/**
 * Loads elements of method at idx into the features spin_system table
 *
 * @param {number} idx index of spin_system table to load
 */
var loadSys = function (idx) {
    console.log(`loadSys ${idx}`);

    document.getElementById("sys-feature-title").textContent = "Spin System " + idx;
    let rows = document.getElementById("sys-feature-rows");
    let params = paramGroups.spin_systems[idx];
    updateRows(rows, params);
};


/**
 * Loads elements of method at idx into the features method table.
 *
 * @param {number} idx index of method table to load
 */
var loadMth = function (idx) {
    console.log(`loadMth ${idx}`);

    document.getElementById("mth-feature-title").textContent = "Method " + idx;
    let rows = document.getElementById("mth-feature-rows");
    let params = paramGroups.methods[idx];
    updateRows(rows, params);
};


/**
 * Saves the JSON serialization of Parameter objects at current spin_system
 * table.
 *
 * @param {number} idx index of system to save
 */
var saveSys = function (idx = null) {
    console.log("saveSys");

    // Set idx to current spin_system index of not specified
    if (idx == null) {
        idx = document.getElementById("sys-feature-title").textContent.slice(-1);
        idx = parseInt(idx);
    }

    let group = paramGroups.spin_systems[idx];

    // const num_params = paramGroups.spin_systems[idx].length
    let rows = document.getElementById("sys-feature-rows");
    for (let i = 0; i < rows.length; i++) {
        let name = rows[i].cells[1].childNodes[0].textContent;

        // Update vary parameter
        group[name][1] = rows[i].cells[0].childNodes[0].checked;

        // Update value parameter
        group[name][0] = rows[i].cells[0].childNodes[0].value;
    }
};


/**
 * Saves the JSON serialization of Parameter objects at current method table.
 */
var saveMth = function (idx = null) {
    console.log("saveMth");

    // Set idx to current method index of not specified
    if (idx == null) {
        idx = document.getElementById("mth-feature-title").textContent.slice(-1);
        idx = parseInt(idx);
    }

    let group = paramGroups.methods[idx];

    // const num_params = paramGroups.spin_systems[idx].length
    let rows = document.getElementById("mth-feature-rows");
    for (let i = 0; i < rows.length; i++) {
        let name = rows[i].cells[1].childNodes[0].textContent;

        // Update vary parameter
        group[name][1] = rows[i].cells[0].childNodes[0].checked;

        // Update value parameter
        group[name][0] = rows[i].cells[0].childNodes[0].value;
    }
};


/**
 * Sets the fields of the features modal and opens the modal
 */
var _loadModal = function (param_name) {
    console.log(`_loadModal ${param_name}`);
    const prefix = param_name.split("_")[0];
    let param_attrs = null;

    // Determine if param is part of spin_systems or methods
    if (sysPrefix.includes(prefix)) {
        param_attrs = paramGroups.spin_systems[storeData.spin_system_index][param_name];
    } else if (mthPrefix.includes(prefix)) {
        param_attrs = paramGroups.methods[storeData.method_index][param_name];
    }

    console.log(document.getElementById("features-modal-subtitle"))

    // Set modal fields from attributes
    document.getElementById("features-modal-subtitle").textContent = param_name;
    document.getElementById("features-modal-min").value = param_attrs[3];
    document.getElementById("features-modal-max").value = param_attrs[4];
    document.getElementById("features-modal-expr").value = param_attrs[2];

    console.log("step 2")
}


/**
 * Saves the fields from the features modal and closes the modal
 */
var _saveModal = function () {
    console.log("_saveModal");
    const param_name = paramGroups.modal_name;
    console.log(param_name);
    const prefix = param_name.split("_")[0];
    let param_attrs = null;

    // Determine if param is part of spin_systems or methods
    if (sysPrefix.includes(prefix)) {
        param_attrs = paramGroups.spin_systems[storeData.spin_system_index][param_name];
    } else if (mthPrefix.includes(prefix)) {
        param_attrs = paramGroups.methods[storeData.method_index][param_name];
    }

    // Grab attributes from inputs
    param_attrs[3] = document.getElementById("features-modal-min").value;
    param_attrs[4] = document.getElementById("features-modal-max").value;
    param_attrs[2] = document.getElementById("features-modal-expr").value;
}


window.dash_clientside.features = {
    triggerSimOrFit: _triggerSimOrFit,
    reloadParamGroups: _reloadParamGroups,
    refreshTables: _refreshTables,
    serializeParamGroups: function () {
        saveSys();
        saveMth();
        return _serializeParamGroups();
    },
    selectNewSys: function (idx) {
        saveSys();
        loadSys(idx);
        window.spinSystem.setIndex(idx);

    },
    selectNewMth: function (idx) {
        saveMth();
        loadMth(idx);
        window.method.setIndex(idx);
        return null;
    },
    openOrCloseModal: function (_n1, _n2, _n3) {
        const trig_id = ctxTriggerID()[0].split(".")[0];

        // Open the modal
        if (trig_id == "open-features-modal") { return true; }

        // Close features modal
        if (trig_id == "close-features-modal") {
            paramGroups.modal_name = null;
            return false;
        }
        // Save and close features modal
        if (trig_id == "features-modal-save") {
            _saveModal();
            paramGroups.modal_name = null;
            return false;
        }
    },
    //, _sub, _min, _max, _expr
    populateModalFields: function (is_open) {
        // Fires on modal open
        if (is_open) {
            _loadModal(paramGroups.modal_name);
        }
    }
}
