export function handleDropdown(e) {
    const dropdown_id = e.target.id;
    const id = dropdown_id + '_div';
    const element = document.getElementById(id);
    const dropdown = document.getElementById(dropdown_id);
    if (element.classList.contains('d-none')) {
        element.classList.remove('d-none');
        dropdown.classList.add('bi-caret-up-fill');
        dropdown.classList.remove('bi-caret-down-fill');
    } else {
        element.classList.add('d-none');
        dropdown.classList.remove('bi-caret-up-fill');
        dropdown.classList.add('bi-caret-down-fill');
    }
}


export function isDict(value) {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}
