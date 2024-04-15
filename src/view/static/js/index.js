function scrollHideWhileDown(class_name) {
  const scrollPos = $(window).scrollTop();
  const element = $(class_name);

  if (scrollPos > 0) {
    element.addClass('hide');
  } else {
    element.removeClass('hide');
  }
}

function scrollHideWhileUp(class_name) {
  const scrollPos = $(window).scrollTop();
  const element = $(class_name);

  if (scrollPos > 0) {
    element.removeClass('hide');
  } else {
    element.addClass('hide');
  }
}

function scrollingMouse() {
  const class_name= '.mouse';
  const element = $(class_name);


  const scrollPos = $(window).scrollTop();

  if (scrollPos > 0) {
    element.css('margin-bottom', '0px')
    element.addClass('hide');
  } else {
    element.css('margin-bottom', '25px')
    element.removeClass('hide');
  }

}

$(window).scroll(function() {
  scrollingMouse();
  scrollHideWhileDown('.big-logo');
  scrollHideWhileUp('.small-logo');
  scrollHideWhileUp('.description');
});