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

function scrollHideWhileDownMouse() {
  const scrollPos = $(window).scrollTop();
  const mouse = $('.mouse');

  if (scrollPos > 0) {
    mouse.addClass('hide');
    mouse.on('transitionend', function() {
      $('.description').removeClass('hide');
      mouse.hide();
      mouse.off('transitionend');
    });
  } else {
    mouse.off('transitionend');
  }
}

function scrollHideWhileUpDescription() {
  const scrollPos = $(window).scrollTop();
  const description = $('.description');

  if (scrollPos > 0) {
    description.show();
    description.off('transitionend');
  } else {
    description.addClass('hide');
    description.on('transitionend', function() {
      $('.mouse').removeClass('hide');
      $('.mouse').show()
      description.off('transitionend');
    });
  }
}

$(window).scroll(function() {
  scrollHideWhileDownMouse()
  scrollHideWhileUpDescription();
  scrollHideWhileUp('.small-logo');
  scrollHideWhileDown('.big-logo');
});