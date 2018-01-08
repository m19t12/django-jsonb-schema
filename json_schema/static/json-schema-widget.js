// IIFE - Immediately Invoked Function Expression

(function (library) {
    // The global jQuery object is passed as a parameter
    library(window.jQuery, window, document);

}(function ($, window, document) {
    $(document).on("click", ".add-schema-item", function () {
        var parentContainer = $(this).parent().parent(),
            item = $(this).parent().clone();

        $('.add-schema-item').remove();

        parentContainer.append(item);
    });
}));
