$(document).ready(function () {
    $("h6").click(function () {
        event.preventDefault();
        $(this).closest('h6').next('div').toggle();
    });
    $("#toggle_sidebar").click(function () {
        $("#leftpane").toggle();
        $("#content").toggleClass("col-sm-10", "col-sm-12");
    });
    $("#toggle_parameters").click(function () {
        $("#upstream").toggle();
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
