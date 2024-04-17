const checkboxes = document.querySelectorAll('.form-check-input');
const checkedCheckboxesDomain = document.querySelectorAll('.checkbox-domain:checked');
const checkedCheckboxesType = document.querySelectorAll('.checkbox-type:checked');

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

        // page number
        const pathname = url.pathname;
        const number = pathname.split('/')[2];

        // domains
        const domain = Array.from(checkedCheckboxesDomain).map(checkbox => checkbox.id);

        // types
        const type = Array.from(checkedCheckboxesType).map(checkbox => checkbox.id);

        // set the new url
        window.location.href = `/manual_search/${number}?search=${search}&domain=${domain}&type=${type}`;
    });
});