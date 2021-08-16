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
    spin_systems: [],
    methods: [],
};
const sysPrefix = ["sys"];
const mthPrefix = ["mth", "SP"];


/**
 * Takes JSON representation of LMFIT Parameters object
 * and groups Parameter objects into spin_systems and methods.
 *
 * @param {String} mrsim_data JSON string of local-mrsim-data
 * @param {String} params_data JSON string of params-data
 */
var _reloadParamGroups = function (_n1, mrsim_data, params_data) {
    console.log("_reloadParamGroups");
    const trig_id = ctxTriggerID()[0].split(".")[0];

    let params = {};
    if (trig_id == "local-mrsim-data") {
        if (mrsim_data.params == null) {
            // Click the hidden button to make lmfit params in python callback
            document.getElementById("make-lmfit-params").click();
            throw window.dash_clientside.PreventUpdate;
        }
        params_data = mrsim_data.params;
    }
    // Clean 'NaN' and 'Infinity' out of JSON string.
    params_data = params_data.replaceAll("NaN", null);
    params_data = params_data.replaceAll("-Infinity", null);
    params_data = params_data.replaceAll("Infinity", null);
    params = JSON.parse(params_data).params;

    // Add dict elements to storage array
    let num_sys = storeData.data.spin_systems.length;
    let num_mth = storeData.data.methods.length;
    for (num_sys; num_sys > 0; num_sys--) {
        paramGroups.spin_systems.push({});
    }
    for(num_mth; num_mth > 0; num_mth--) {
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
var _serializeParamGroups = function (old_json) {
    console.log("_serializeParamGroups");

    // Make new str for parameters JSON
    let new_json = '"params":[';

    // Iterate through spin_systems
    paramGroups.spin_systems.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
            // Replace null min/max with str to replace in json
            if (tmp[4] == null) {
                tmp[4] = "~rep -inf~";
            }
            if (tmp[5] == null) {
                tmp[5] = "~rep inf~";
            }
            new_json = new_json.concat(JSON.stringify(tmp));
        }
    });

    // Iterate through methods
    paramGroups.methods.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
            // Replace null min/max with str to replace in json
            if (tmp[4] == null) {
                tmp[4] = "~rep -inf~";
            }
            if (tmp[5] == null) {
                tmp[5] = "~rep inf~";
            }
            new_json = new_json.concat(JSON.stringify(tmp));
        }
    });

    // Replace unbound min/max to comply with LMFIT serialization
    new_json = new_json.replaceAll("~rep -inf~", "-Infinity");
    new_json = new_json.replaceAll("~rep inf~", "Infinity");

    // Replace "params" key in old data with new json
    old_json = old_json.substring(0, old_json.indexOf('"params":'));
    return old_json.concat(new_json, ']');
};


/**
 * Serialize data in tables and trigger a simulation or fit
 *
 * @param {String} which flag for which to trigger ("sim" or "fit")
 * @param {Object} mrsim_data stored data in local-mrsim-data
 * @param {String} params_data JSON str of Parameters object
 * @returns
 */
var _triggerSimOrFit = function (_trig, which, mrsim_data, params_data) {
    console.log("_triggerSimOrFit");
    saveSys();
    saveMth();

    let data = params_data;
    if (data == null) {
        data = mrsim_data.params;
    }

    let new_data = _serializeParamGroups(data);
    if (which == "sim") {
        return new_data, Date.now(), window.dash_clientside.no_update;
    }
    if (which == "fit") {
        return new_data, window.dash_clientside.no_update, Date.now();
    }
    return window.dash_clientside.PreventUpdate;
}


// Reduce resuded code by completing this method
/**
 *
 * @param {tbody} rows HTML tbody element to add param rows to
 * @param {Object} params
 */
 var updateRows = function (rows, params) {
    // Remove currently stored rows
    while(rows.hasChildNodes()) {
        rows.removeChild(rows.lastChild);
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
        name.innerText = key;

        // Add value
        let val = document.createElement("input");
        val.type = "number";
        val.step = "any";
        val.value = value[0];
        new_row.insertCell().appendChild(val);

        // More options button
        let button = document.createElement("button");
        button.innerText = "btn";
        new_row.insertCell().appendChild(button);
    }
};


/**
 * Loads elements of method at idx into the features spin_system table
 *
 * @param {number} idx index of spin_system table to load
 */
var loadSys = function (idx) {
    console.log("loadSys");

    document.getElementById("sys-feature-title").innerText = "Spin System " + idx;
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
    console.log("loadMth");

    document.getElementById("mth-feature-title").innerText = "Method " + idx;
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
        idx = document.getElementById("sys-feature-title").innerText.slice(-1);
        idx = parseInt(idx);
    }

    let group = paramGroups.spin_systems[idx];

    // const num_params = paramGroups.spin_systems[idx].length
    let rows = document.getElementById("sys-feature-rows");
    for (let i = 0; i < rows.length; i++) {
        let name = rows[i].cells[1].childNodes[0].innerText;

        // Update vary parameter
        group[name][1] = rows[i].cells[0].childNodes[0].checked;

        // Update value parameter
        group[name][0] = rows[i].cells[0].childNodes[0].value;

        // Update modal parameters
        // NEED TO IMPLEMENT
    }
};


/**
 * Saves teh SJON serialization of Parameter objects at current method table.
 */
var saveMth = function (idx = null) {
    console.log("saveMth");

    // Set idx to current method index of not specified
    if (idx == null) {
        idx = document.getElementById("mth-feature-title").innerText.slice(-1);
        idx = parseInt(idx);
    }

    let group = paramGroups.methods[idx];

    // const num_params = paramGroups.spin_systems[idx].length
    let rows = document.getElementById("mth-feature-rows");
    for (let i = 0; i < rows.length; i++) {
        let name = rows[i].cells[1].childNodes[0].innerText;

        // Update vary parameter
        group[name][1] = rows[i].cells[0].childNodes[0].checked;

        // Update value parameter
        group[name][0] = rows[i].cells[0].childNodes[0].value;

        // Update modal parameters
        // NEED TO IMPLEMENT
    }
};


window.dash_clientside.features = {
    triggerSimOrFit: _triggerSimOrFit,
    reloadParamGroups: _reloadParamGroups,
    refreshTables: _refreshTables,
    serializeParamGroups: function (data) {
        saveSys();
        saveMth();
        return _serializeParamGroups(data);
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
}
