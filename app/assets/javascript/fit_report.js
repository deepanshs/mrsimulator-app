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
    // console.log("_updateFitReport");

    // Check to make sure report string present
    let report_str = storeData.data.report;
    if (report_str) {
        let body = document.getElementById("fit-report-table-div");
        body.innerHTML = report_str;

        // Get the stats header and table to wrap in a div
        let stats_header = body.removeChild(body.childNodes[0]);
        let stats_table = body.removeChild(body.childNodes[0]);
        // Remove last column of table (unused)
        for (const row of stats_table.rows) {
            row.deleteCell(-1);
        }

        // Insert new wrapper div at 0th index
        let info_div = document.createElement("div");
        info_div.classList.add("flex-row");
        body.insertBefore(info_div, body.childNodes[0]);

        // Create overview info div from homepage info
        let overview_div = info_div.appendChild(document.createElement("div"));
        let title = overview_div.appendChild(document.createElement("H2"));
        title.innerText = document.querySelector("#info-read-only > div > div:nth-child(1) > h4").innerText.slice(0, -36);
        let about = overview_div.appendChild(document.createElement("div"));
        about.innerText = document.querySelector("#info-read-only > div > div.card > div").innerText;
        about.classList.add("card");
        // add spin system table
        let sys_info = overview_div.appendChild(document.createElement("H4"));
        sys_info.innerText = "Spin System Overview";
        let system_table = overview_div.appendChild(document.createElement("table"));
        system_table.innerHTML = document.getElementById("system-table").innerHTML;
        for (const row of system_table.rows) {
            row.deleteCell(-1);
          }
        // add method table
        let mth_info = overview_div.appendChild(document.createElement("H4"));
        mth_info.innerText = "Method Overview";
        let method_table = overview_div.appendChild(document.createElement("table"));
        method_table.innerHTML = document.getElementById("method-table").innerHTML;
        // remove last two columns (spinning speed and edit)
        for (const row of method_table.rows) {
            row.deleteCell(-1);
            row.deleteCell(-1);
          }

        // Readd stats header and table wrapped in div
        let stats_div = info_div.appendChild(document.createElement("div"));
        stats_div.appendChild(stats_header);
        stats_div.appendChild(stats_table);
    }

    return;
};


var _get_fit_report_html = function (n1) {
    // console.log("_get_fit_report_html");
    let report = document.createElement("div");
    report.id = "report-output-div";
    let temp_div = report.appendChild(document.createElement("div"));
    temp_div.outerHTML = document.getElementById("fit-report-table-div").outerHTML;
    let report_html_str = report.outerHTML;
    report.remove();
    return report_html_str + n1;
};


window.dash_clientside.report = {
    updateFitReport: _updateFitReport,
    get_fit_report_html: _get_fit_report_html
};
