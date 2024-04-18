const checkboxes = document.querySelectorAll('.form-check-input');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        console.log('checked');

        // search term
        const url = new URL(window.location.href);
        const searchParams = new URLSearchParams(url.search);
        var search = searchParams.get('search');
        if (search == null) {
            search = '';
        }

        // domains
        const checkedCheckboxesDomain = document.querySelectorAll('.checkbox-domain:checked');
        const domain = Array.from(checkedCheckboxesDomain).map(checkbox => checkbox.id);

        // types
        const checkedCheckboxesType = document.querySelectorAll('.checkbox-type:checked');
        const type = Array.from(checkedCheckboxesType).map(checkbox => checkbox.id);

        // set the new url
        window.location.href = `/manual_search/0?search=${search}&type=${type}&domain=${domain}`;
    });
});