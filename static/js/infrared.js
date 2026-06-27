$(document).ready(function () {
    $("h6").click(function () {
        event.preventDefault();
        $(this).closest('h6').next('div').toggle();
    });
    $("#toggle_sidebar").click(function (event) {
        event.preventDefault();
        $("#leftpane").toggle();
        $("#content").toggleClass("col-sm-10").toggleClass("col-sm-12");
    });
    $("#toggle_parameters").click(function () {
        $("#upstream").toggle();
    });

    // Table image preview: position the popup with fixed coordinates so it is
    // never clipped by the table's overflow, and clamp it to the viewport so
    // its bottom aligns with the bottom of the page for low rows.
    function positionPreview(wrap) {
        var popup = wrap.querySelector(".preview-popup");
        if (!popup) return;
        var margin = 8;
        var rect = wrap.getBoundingClientRect();
        popup.style.display = "block";
        popup.style.visibility = "hidden";
        var pw = popup.offsetWidth, ph = popup.offsetHeight;
        var vw = window.innerWidth, vh = window.innerHeight;
        var left = rect.right + margin;
        if (left + pw + margin > vw) left = rect.left - pw - margin; // flip left
        left = Math.max(margin, Math.min(left, vw - pw - margin));
        var top = Math.max(margin, Math.min(rect.top, vh - ph - margin));
        popup.style.left = left + "px";
        popup.style.top = top + "px";
        popup.style.visibility = "visible";
        // Re-clamp once the image has loaded and its real height is known.
        var img = popup.querySelector("img");
        if (img && !img.complete) {
            img.addEventListener("load", function () {
                if (popup.style.display === "block") positionPreview(wrap);
            }, { once: true });
        }
    }
    $(document).on("mouseenter", ".image-hover-preview", function () {
        positionPreview(this);
    });
    $(document).on("mouseleave", ".image-hover-preview", function () {
        var popup = this.querySelector(".preview-popup");
        if (popup) popup.style.display = "none";
    });
    // TODO: source is not a valid HTML attribute, use data-source instead
    $('[source], [data-source]').map(function () {
        var elementID = $(this).attr('name');
        var source = $(this).attr('source') ? $(this).attr('source') : $(this).data('source');
        $(this).autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "../../suggest/?",
                    dataType: "json",
                    data: {
                        q: request.term,
                        elementID: elementID,
                        source: source
                    },
                    success: function (data) {
                        response(data);
                    }
                });
            },
            minLength: 1
        });
    });
});
