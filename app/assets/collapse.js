function a() {
    var sliders = document.getElementsByClassName("slider-custom");
    var i;


    var test = document.getElementById('spectrometer_frequency-0_label')
    document.write(test)

    for (i = 0; i < sliders.length; i++) {
        sliders[i].addEventListener("mousedown", function () {
            // this.classList.toggle("active");
            var id_label = this.id.concat('_label')
            document.getElementById(id_label).innerHTML = this.value
            // var content = this.nextElementSibling;
            // if (content.style.display === "block") {
            //     content.style.display = "none";
            // } else {
            //     content.style.display = "block";
            // }
        });
    }
}
