
function animationNavbarTitle() {
  const navbarHeight = $('.navbar').height();

  const navbarColor = "62,195,246";//color attr for rgba
  const smallLogoHeight = $('.small-logo').height();
  const bigLogoHeight = $('.big-logo').height();


  const smallLogoEndPos = 0;
  const smallSpeed = (smallLogoHeight / bigLogoHeight);

  const ySmall = ($(window).scrollTop() * smallSpeed);

  let smallPadding = navbarHeight - ySmall;
  if (smallPadding > navbarHeight) {
    smallPadding = navbarHeight;
  }
  if (smallPadding < smallLogoEndPos) {
    smallPadding = smallLogoEndPos;
  }
  if (smallPadding < 0) {
    smallPadding = 0;
  }

  $('.small-logo-container ').css({"padding-top": smallPadding});

  var navOpacity = ySmall / smallLogoHeight;
  if (navOpacity > 1) {
    navOpacity = 1;
  }
  if (navOpacity < 0) {
    navOpacity = 0;
  }
  var navBackColor = 'rgba(' + navbarColor + ',' + navOpacity + ')';
  $('.navbar').css({"background-color": navBackColor});
}



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
  animationNavbarTitle();
  scrollingMouse();
  scrollHideWhileDown('.big-logo');
  scrollHideWhileUp('.description');
});