export function scrollHideWhileDown(class_name) {
    const scrollPos = window.pageYOffset;
    const element = document.querySelector(class_name);

    if (scrollPos > 0) {
        element.classList.add('hide');
    } else {
        element.classList.remove('hide');
    }
}

export function scrollHideWhileUp(class_name) {
    const scrollPos = window.pageYOffset;
    const element = document.querySelector(class_name);

    if (scrollPos > 0) {
        element.classList.remove('hide');
    } else {
        element.classList.add('hide');
    }
}

function transitionEndHandlerMouse() {
    const description = document.querySelector('.description');
    description.classList.remove('hide');
    this.classList.add('d-none');
    this.removeEventListener('transitionend', transitionEndHandlerMouse);
}

export function scrollHideWhileDownMouse() {
    const scrollPos = window.pageYOffset;
    const mouse = document.querySelector('.mouse');

    if (scrollPos > 0) {
        mouse.classList.add('hide');
        mouse.addEventListener('transitionend', transitionEndHandlerMouse);
    } else {
        mouse.removeEventListener('transitionend', transitionEndHandlerMouse);
    }
}

function transitionEndHandlerDescription() {
    const mouse = document.querySelector('.mouse');
    mouse.classList.remove('hide');
    mouse.classList.remove('d-none');
    this.removeEventListener('transitionend', transitionEndHandlerDescription);
}

export function scrollHideWhileUpDescription() {
    const scrollPos = window.pageYOffset;
    const description = document.querySelector('.description');

    if (scrollPos > 0) {
        description.removeEventListener('transitionend', transitionEndHandlerDescription);
    } else {
        description.classList.add('hide');
        description.addEventListener('transitionend', transitionEndHandlerDescription);
    }
}