/*
 * Author = "Matthew D. Giammar"
 * Email = "giammar.7@osu.edu"
 */

/* jshint esversion: 6 */


/**
 * Gets the raw html string from 'storeData.data.report' and updates the html
 * of the report body div
 */
var _updateFitReport = function () {
    console.log("_updateFitReport");

    // Check to make sure report string present
    let report_str = storeData.data.report;
    if (report_str) {
        let body = document.getElementById("fit-report-table-div");
        body.innerHTML = report_str;
    }

    return;
}


window.dash_clientside.report = {
    updateFitReport: _updateFitReport
}
