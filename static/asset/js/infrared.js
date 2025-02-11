$(document).ready(function () {
    $("h6").click(function () {
        event.preventDefault();
        $(this).closest('h6').next('div').toggle();
    });
    $("#toggle_sidebar").click(function () {
        $("#leftpane").toggle();
        $("#content").toggleClass("col-sm-9", "col-sm-12");
    });
    $("#toggle_parameters").click(function () {
        $("#upstream").toggle();
    });
});
