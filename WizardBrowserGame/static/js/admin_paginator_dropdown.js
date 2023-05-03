window.addEventListener('load', function () {
    (function ($) {
        // Jquery should be loaded now
        // Table paginator has class paginator. We want to append to this
        var paginator = $(".paginator");
        var list_per_page = $(`
            <select id='list_per_page_selector'>
                <option value=${5}>5</option>
                <option value=${10}>10</option>
                <option value=${25} selected>25</option>
                <option value=${50}>50</option>
                <option value=${100}>100</option>
            </select>
        `)
        var url = new URL(window.location);
        // Retrieve the current value for updating the selected dropdown on page refresh
        var initial_list_per_page = url.searchParams.get("list_per_page")
        paginator.prepend(list_per_page)
        if (initial_list_per_page === null) {
            // No choice has been made, set dropdown to default value
            $("#list_per_page_selector").val("25")
        }
        else {
            // If he clicked show all remove dropdown
            var checkIfShowAll = url.searchParams.get("all")
            if (checkIfShowAll != null) $("#list_per_page_selector").remove()

            // User has a query parameter with a selection. Update the selected accordingly
            $("#list_per_page_selector").val(initial_list_per_page)
        }
        $("#list_per_page_selector").on("change", function (event) {
            // Add the list_per_page parameter to the url to be used in admin.py
            url.searchParams.set("list_per_page", event.target.value);
            //Take us to the new page.
            window.location.href = url.href;
        });

        allPagLinks = $(".paginator a");
        for (let index = 0; index < allPagLinks.length; index++) {
            link = allPagLinks[index];
            link.href = link.href +  "&list_per_page="+url.searchParams.get("list_per_page")

        }
    })(django.jQuery);
});