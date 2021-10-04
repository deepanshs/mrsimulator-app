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
var doExternalIndexUpdate = true;
const sysPrefix = ["sys"];
const mthPrefix = ["mth", "SP"];
const maxFeatureButtons = 8;


/**
 * Takes JSON representation of LMFIT Parameters object
 * and groups Parameter objects into spin_systems and methods.
 */
var _reloadParamGroups = function () {
    // console.log("_reloadParamGroups");

    // If number of spin systems or methods is zero do not update
    if (!(storeData.data.spin_systems.length && storeData.data.methods.length)) {
        return;
    }

    // Logic for creating params JSON if not already present
    if (!storeData.data.params) {  // true if 'null', 'undefined' or empty str
        document.getElementById("make-lmfit-params").click();
        return;
    }

    // Get stored json string
    let params_json = storeData.data.params;

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
    let params = JSON.parse(params_json).params;

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
 */
var _refreshTables = function (_n1, _n2) {
    let sys_idx = storeData.spin_system_index;
    let mth_idx = storeData.method_index;
    // console.log(`_refreshTables: sys - ${sys_idx}, mth - ${mth_idx}`);
    _loadSys(sys_idx);
    _loadMth(mth_idx);
}


/**
 * Clears the rows of both tables and buttons of feature select
 */
var _clearParamGroupsAndTables = function () {
    paramGroups = {
        modal_name: null,
        spin_systems: [],
        methods: [],
    };

    // Clear table rows
    let sys_rows = document.getElementById("sys-feature-rows");
    sys_rows.innerHTML = "";
    while (sys_rows.hasChildNodes()) {
        sys_rows.removeChild(sys_rows.lastChild);
    }

    let mth_rows = document.getElementById("mth-feature-rows");
    while (mth_rows.hasChildNodes()) {
        mth_rows.removeChild(mth_rows.lastChild);
    }

    // Set table titles to Spin System and Methods (no numbers)
    document.getElementById("sys-feature-title").textContent = "Spin System"
    document.getElementById("mth-feature-title").textContent = "Method"
}


/**
 * Serializes paramGroups variable into LMFIT compliant JSON string
 *
 * @returns {String} updated JSON
 */
var _serializeParamGroups = function () {
    // console.log("_serializeParamGroups");

    // console.log(paramGroups);

    let old_json = storeData.data.params;

    // Make temporary array for parameters
    let tmp_arr = [];

    // Iterate through spin_systems
    // TODO: Clean up for loop code
    paramGroups.spin_systems.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
            tmp_arr.push(tmp);
        }
    });

    // Iterate through methods
    paramGroups.methods.forEach(element => {
        for (const [key, value] of Object.entries(element)) {
            let tmp = [key].concat(value);
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
 * @param {String} which: flag for which to trigger ("sim" or "fit")
 */
var _triggerSimOrFit = function (_trig, which) {
    // console.log("_triggerSimOrFit");
    _saveSys();
    _saveMth();

    // console.log(which)

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
 * @param {tbody} rows: HTML tbody element to add param rows to
 * @param {Object} params
 */
var _updateRows = function (rows, params) {
    // Remove currently stored rows
    while (rows.hasChildNodes()) {
        rows.removeChild(rows.lastChild);
    }

    // Check if rows is none
    if (rows == null) {
        console.log("Rows is undefined. Halting update");
        return;
    }

    // Check if params is none
    if (params == null) {
        console.log("Params is undefined. Halting update");
        document.getElementById("make-lmfit-params").click();
        return;
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
 * @param {number} idx: index of spin_system table to load
 */
var _loadSys = function (idx) {
    // console.log(`_loadSys ${idx}`);

    document.getElementById("sys-feature-title").textContent = "Spin System " + idx;
    let rows = document.getElementById("sys-feature-rows");
    let params = paramGroups.spin_systems[idx];
    _updateRows(rows, params);
};


/**
 * Loads elements of method at idx into the features method table.
 *
 * @param {number} idx: index of method table to load
 */
var _loadMth = function (idx) {
    // console.log(`_loadMth ${idx}`);

    document.getElementById("mth-feature-title").textContent = "Method " + idx;
    let rows = document.getElementById("mth-feature-rows");
    let params = paramGroups.methods[idx];
    _updateRows(rows, params);
};


/**
 * Saves the JSON serialization of Parameter objects at current spin_system
 * table.
 *
 * @param {number} idx: system index to save. Current index if not provided
 * @returns {number} index of saved spin system
 */
var _saveSys = function (idx = null) {
    // console.log("_saveSys");

    // Set idx to current spin_system index of not specified
    if (idx == null) {
        idx = document.getElementById("sys-feature-title").textContent.slice(-1);
        idx = parseInt(idx);
    }
    // console.log(idx)

    // Only continue if paramGroups.spin_system[idx] is defined
    if (paramGroups.spin_systems[idx]) {
        let group = paramGroups.spin_systems[idx];

        // const num_params = paramGroups.spin_systems[idx].length
        let rows = document.getElementById("sys-feature-rows").childNodes;
        for (let i = 0; i < rows.length; i++) {
            let name = rows[i].cells[1].childNodes[0].textContent;

            // Update vary parameter
            group[name][1] = rows[i].cells[0].childNodes[0].checked;

            // Update value parameter
            group[name][0] = parseFloat(rows[i].cells[2].childNodes[0].value);
        }
    }
    return idx;
};


/**
 * Saves the JSON serialization of Parameter objects at current method table.
 *
 * @param {Number} idx: index of method to save. Current index if not provided
 * @returns {Number} index of saved method
 */
var _saveMth = function (idx = null) {
    // console.log("_saveMth");

    // Set idx to current method index of not specified
    if (idx == null) {
        idx = document.getElementById("mth-feature-title").textContent.slice(-1);
        idx = parseInt(idx);
    }

    // Only continue if paramGroups.methods[idx] is defined
    if (paramGroups.methods[idx]) {
        let group = paramGroups.methods[idx];

        // const num_params = paramGroups.spin_systems[idx].length
        let rows = document.getElementById("mth-feature-rows").childNodes;
        // console.log(rows.length)
        for (let i = 0; i < rows.length; i++) {
            // console.log(i)
            let name = rows[i].cells[1].childNodes[0].textContent;

            // Update vary parameter
            group[name][1] = rows[i].cells[0].childNodes[0].checked;

            // Update value parameter
            // console.log(`val: ${(rows[i].cells[2].childNodes[0].value)}`);
            group[name][0] = parseFloat(rows[i].cells[2].childNodes[0].value);
        }
    }
    return idx;
};


/**
 * Sets the fields of the features modal and opens the modal
 *
 * @param {String} param_name: name of parameter to load
 */
var _loadModal = function (param_name) {
    // console.log(`_loadModal ${param_name}`);
    const prefix = param_name.split("_")[0];
    let param_attrs = null;

    // Determine if param is part of spin_systems or methods
    if (sysPrefix.includes(prefix)) {
        param_attrs = paramGroups.spin_systems[storeData.spin_system_index][param_name];
    } else if (mthPrefix.includes(prefix)) {
        param_attrs = paramGroups.methods[storeData.method_index][param_name];
    }

    // Set modal fields from attributes
    document.getElementById("features-modal-subtitle").textContent = param_name;
    document.getElementById("features-modal-min").value = param_attrs[3];
    document.getElementById("features-modal-max").value = param_attrs[4];
    document.getElementById("features-modal-expr").value = param_attrs[2];
}


/**
 * Saves the fields from the features modal and closes the modal
 */
var _saveModal = function () {
    const param_name = paramGroups.modal_name;
    // console.log(`_saveModal: ${param_name}`);
    const prefix = param_name.split("_")[0];
    let param_attrs = null;

    // Determine if param is part of spin_systems or methods
    if (sysPrefix.includes(prefix)) {
        param_attrs = paramGroups.spin_systems[storeData.spin_system_index][param_name];
    } else if (mthPrefix.includes(prefix)) {
        param_attrs = paramGroups.methods[storeData.method_index][param_name];
    }

    // Grab attributes from inputs
    param_attrs[3] = parseFloat(document.getElementById("features-modal-min").value);
    param_attrs[4] = parseFloat(document.getElementById("features-modal-max").value);
    param_attrs[2] = document.getElementById("features-modal-expr").value;
}


/**
 * Reloads feature select buttons by updating number of buttons, button labels,
 * updating EventLiseners and showing/hiding page buttons
 */
var _onFeaturesReload = function () {
    // console.log("_onFeaturesreload");

    // Update paramGroups before updating options and tables
    _reloadParamGroups();

    let num_sys = storeData.data.spin_systems.length;
    let num_mth = storeData.data.methods.length;
    let sys_page_idx = document.getElementById("sys-feature-select").getAttribute("pageindex");
    let mth_page_idx = document.getElementById("mth-feature-select").getAttribute("pageindex");
    if (sys_page_idx) {
        sys_page_idx = parseInt(sys_page_idx);
    } else {
        document.getElementById("sys-feature-select").setAttribute("pageindex", 0);
        sys_page_idx = 0;
    }
    if (mth_page_idx) {
        mth_page_idx = parseInt(mth_page_idx);
    } else {
        document.getElementById("mth-feature-select").setAttribute("pageindex", 0);
        mth_page_idx = 0;
    }

    _reloadSysFeatureButtons(num_sys, sys_page_idx);
    _reloadMthFeatureButtons(num_mth, mth_page_idx);

    _setSysPageVisibility(num_sys);
    _setMthPageVisibility(num_mth);

    let sys_idx = storeData.spin_system_index;
    let mth_idx = storeData.method_index;
    _loadSys(sys_idx)
    _loadMth(mth_idx)
}


/**
 * Updates buttons on spin system feature select
 *
 * @param {Number} num_sys: Number of spin_systems
 * @param {Number} sys_page_idx: Spin system feature select page index
 * @param {boolean} ignore_page: default true, do not skip if same page
 */
var _reloadSysFeatureButtons = function (num_sys, sys_page_idx, ignore_page=true) {
    // Set sys_page_idx to 0 if null
    if  (sys_page_idx == null) {
        sys_page_idx = 0;
    }

    // Check if already on page
    let current_page_idx = parseInt(document.getElementById("sys-feature-select").getAttribute("pageindex"));
    if (ignore_page || sys_page_idx != current_page_idx) {
        // Get and clear current system features
        let sys_options = document.getElementById("sys-feature-select");
        while (sys_options.firstChild) {
            sys_options.removeChild(sys_options.firstChild);
        }

        // Reload all buttons for this page
        let min = sys_page_idx * maxFeatureButtons;
        let max = Math.min(num_sys, min + maxFeatureButtons)
        for (let i = min; i < max; i++) {
            sys_options.appendChild(_makeOption(i, "sys"));
        }
    }
}


/**
 * Updates buttons on method feature select
 *
 * @param {Number} num_mth: Number of spin_systems
 * @param {Number} mth_page_idx: Spin system feature select page index
 * @param {boolean} ignore_page: default true, do not skip if same page
 */
var _reloadMthFeatureButtons = function (num_mth, mth_page_idx, ignore_page=true) {
    // Set sys_page_idx to 0 if null
    if  (mth_page_idx == null) {
        mth_page_idx = 0;
    }

    // Check if already on page
    let current_page_idx = parseInt(document.getElementById("mth-feature-select").getAttribute("pageindex"));
    if (ignore_page || mth_page_idx != current_page_idx) {
        // Get and clear current system features
        let mth_options = document.getElementById("mth-feature-select");
        while (mth_options.firstChild) {
            mth_options.removeChild(mth_options.firstChild);
        }

        // Reload all buttons for this page
        let min = mth_page_idx * maxFeatureButtons;
        let max = Math.min(num_mth, min + maxFeatureButtons)
        for (let i = min; i < max; i++) {
            mth_options.appendChild(_makeOption(i, "mth"));
        }
    }
}


/**
 * Makes radio button option with event listener to save and update table index
 *
 * @param {Number} idx: index for button to display
 * @param {String} which: "sys" or "mth"
 * @returns {Element} new div with raido button and label
 */
var _makeOption = function (idx, which) {
    let div = document.createElement("div");
    div.id = `${which}-feature-${idx}`;
    div.className = `select-spot ${which}`;
    div.innerHTML = idx;
    div.setAttribute("which", which);
    div.onclick = function () {
        let index = parseInt(this.innerText);
        let which = this.getAttribute("which");

        // Do nothing if already active
        if (this.classList.contains("active")) {
            return;
        }

        // Update active element for CSS
        let buttons = document.getElementsByClassName(`select-spot ${which}`)
        for (let btn of buttons) {
            btn.classList.remove("active");
        }
        this.classList.add("active");

        // Save and load new table
        if (which == "sys") {
            _saveSys();
            _loadSys(index);
            if (doExternalIndexUpdate) {
                window.spinSystem.select(null, index);
            }
            storeData.spin_system_index = index;
        }
        if (which == "mth") {
            _saveMth();
            _loadMth(index);
            if (doExternalIndexUpdate) {
                window.method.select(null, index);
            }
            storeData.method_index = index;
        }

    }

    return div
}


/**
 * Sets the visibility of spin system page buttons based on num_sys
 *
 * @param {Number} num_sys: Number of spin systems
 */
var _setSysPageVisibility = function (num_sys) {
    if (num_sys > maxFeatureButtons) {
        document.getElementById("page-sys-feature-left").classList.remove("hidden");
        document.getElementById("page-sys-feature-right").classList.remove("hidden");
    } else {
        document.getElementById("page-sys-feature-left").classList.add("hidden");
        document.getElementById("page-sys-feature-right").classList.add("hidden");
    }
}


/**
 * Sets the visibility of method page buttons based on num_mth
 *
 * @param {Number} num_mth: Number of methods
 */
 var _setMthPageVisibility = function (num_mth) {
    if (num_mth > maxFeatureButtons) {
        document.getElementById("page-mth-feature-left").className = "";
        document.getElementById("page-mth-feature-right").className = "";
    } else {
        document.getElementById("page-mth-feature-left").className = "hidden";
        document.getElementById("page-mth-feature-right").className = "hidden";
    }
}


/**
 * Pages spin_system feature select buttons to the left (decreases page index)
 */
var _pageSysLeft = function() {
    // console.log("_pageSysLeft");
    let sys_features = document.getElementById("sys-feature-select");
    let sys_page_idx = parseInt(sys_features.getAttribute("pageindex"));
    let num_sys = storeData.data.spin_systems.length;

    // Already on leftmost page
    if (sys_page_idx == 0) {
        return;
    }

    _reloadSysFeatureButtons(num_sys, --sys_page_idx);
    sys_features.setAttribute("pageindex", sys_page_idx);
    document.getElementById(`sys-feature-${sys_page_idx * maxFeatureButtons}`).click();
}


/**
 * Pages spin_system feature select buttons to the right (increases page index)
 */
 var _pageSysRight = function() {
    // console.log("_pageSysLeft");
    let sys_features = document.getElementById("sys-feature-select");
    let sys_page_idx = parseInt(sys_features.getAttribute("pageindex"));
    let num_sys = storeData.data.spin_systems.length;

    // Already on rightmost page
    if (sys_page_idx == Math.floor((num_sys - 1) / maxFeatureButtons)) {
        return;
    }

    _reloadSysFeatureButtons(num_sys, ++sys_page_idx);
    sys_features.setAttribute("pageindex", sys_page_idx);
    document.getElementById(`sys-feature-${sys_page_idx * maxFeatureButtons}`).click();
}


/**
 * Pages method feature select buttons to the left (decreases page index)
 */
 var _pageMthLeft = function() {
    // console.log("_pageMthLeft");
    let mth_features = document.getElementById("mth-feature-select")
    let mth_page_idx = parseInt(mth_features.getAttribute("pageindex"));
    let num_mth = storeData.data.spin_systems.length;

    // Already on leftmost page
    if (mth_page_idx == 0) {
        return;
    }

    _reloadMthFeatureButtons(num_mth, --mth_page_idx);
    mth_features.setAttribute("pageindex", mth_page_idx);
    document.getElementById(`mth-feature-${mth_page_idx * maxFeatureButtons}`).click();
}


/**
 * Pages method feature select buttons to the right (increases page index)
 */
 var _pageMthRight = function() {
    // console.log("_pageSysLeft");
    let mth_features = document.getElementById("mth-feature-select")
    let mth_page_idx = parseInt(mth_features.getAttribute("pageindex"));
    let num_mth = storeData.data.spin_systems.length;

    // Already on rightmost page
    if (mth_page_idx == Math.floor((num_mth - 1) / maxFeatureButtons)) {
        return;
    }

    _reloadMthFeatureButtons(num_mth, ++mth_page_idx);
    mth_features.setAttribute("pageindex", mth_page_idx);
    document.getElementById(`mth-feature-${mth_page_idx * maxFeatureButtons}`).click();
}


window.dash_clientside.features = {
    clearTables: _clearParamGroupsAndTables,
    reloadParamGroups: _reloadParamGroups,  // Unpacks JSON
    serializeParamGroups: function () {  // Searilaizes paramGroups to JSON
        _saveSys();
        _saveMth();
        return _serializeParamGroups();
    },
    triggerSimOrFit: _triggerSimOrFit,  // Triggers simulation or fitting
    refreshTables: _refreshTables,  // Refreshes both table fields
    openOrCloseModal: function (_n1, _n2, _n3) {  // Opens the features modal
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
    populateModalFields: function (is_open) {  // Update modal fields after wait
        // Fires on modal open
        if (is_open) {
            _loadModal(paramGroups.modal_name);
        }
    },
    pageFeatureSelect: function (_1, _2, _3, _4) { //Page sys/mth feature select
        const trig_id = ctxTriggerID()[0].split(".")[0];

        switch (trig_id) {
            case "page-sys-feature-left":
                // Page spin_system choices to the left
                return _pageSysLeft();

            case "page-sys-feature-right":
                // Page spin_system choices to the right
                return _pageSysRight();

            case "page-mth-feature-left":
                // Page method choices to the left
                return _pageMthLeft();

            case "page-mth-feature-right":
                // Page method choices to the right
                return _pageMthRight();

            default:
                return;

        }
    }
}

window.features = {
    selectSystem: function (idx) {
        // update options if index not on current page
        let page_idx = Math.floor(idx / maxFeatureButtons);
        _reloadSysFeatureButtons(storeData.data.spin_systems.length, page_idx, false);

        doExternalIndexUpdate = false;
        document.getElementById(`sys-feature-${idx}`).click();
        doExternalIndexUpdate = true;
    },
    selectMethod: function (idx) {
        // update options if index not on current page
        let page_idx = Math.floor(idx / maxFeatureButtons);
        _reloadMthFeatureButtons(storeData.data.methods.length, page_idx, false);

        doExternalIndexUpdate = false;
        document.getElementById(`mth-feature-${idx}`).click();
        doExternalIndexUpdate = true;
    },
}
