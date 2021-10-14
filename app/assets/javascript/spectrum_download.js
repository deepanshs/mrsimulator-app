/*
 * Author = "Matthew D. Giammar"
 * Email = "giammar.7@osu.edu"
 */

/* jshint esversion: 6 */


var download_descriptions = {
    "download-img": "Download an image of the spectrum",
    "download-csdf": "Download spectrum data as a csdf file. For more info, see the ",
    "download-html": "Download an interactive Plotly html file",
};


/**
 * Changes download type from image, html, and csdf based on buttons pressed
 */
var _change_download_type = function (_n1, _n2, _n3) {
    const trig_id = ctxTriggerID()[0].split(".")[0];
    console.log(`_change_download_type ${trig_id}`);

    let arr;
    let descr_div = document.getElementById("download-description");

    if (trig_id == "download-img") {
        arr = [true, false, false];
        descr_div.innerHTML = download_descriptions["download-img"];
        document.getElementById("img-options-div").classList.remove("hidden");
    } else if (trig_id == "download-csdf") {
        arr = [false, true, false];
        descr_div.innerHTML = download_descriptions["download-csdf"];
        let doc_link = document.createElement("a");
        doc_link.href = "https://csdmpy.readthedocs.io/en/v0.4.1/index.html"
        doc_link.innerText = "csdmpy documentation"
        descr_div.appendChild(doc_link);
        document.getElementById("img-options-div").classList.add("hidden");
    } else if (trig_id == "download-html") {
        arr = [false, false, true];
        document.getElementById("img-options-div").classList.add("hidden");
        descr_div.innerHTML = download_descriptions["download-html"];
    }

    return arr;
}


window.dash_clientside.download_spectrum = {
    change_download_type: _change_download_type,
}
