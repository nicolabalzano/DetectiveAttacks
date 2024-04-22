// scrollFunctions.js

export const handleScroll = () => {
  const bigLogo = document.querySelector('.big-logo');
  const subTitle = document.querySelector('.sub-title');
  const mouse = document.querySelector('.mouse');
  const description = document.querySelector('.description');
  const smallLogo = document.querySelector('.small-logo');

  if (window.pageYOffset > 0) {
    bigLogo.classList.add('hide');
    mouse.classList.add('hide');
    description.classList.remove('hide');
    smallLogo.classList.remove('hide');
    mouse.style.height = '0';
  } else {
    bigLogo.classList.remove('hide');
    mouse.classList.remove('hide');
    description.classList.add('hide');
    smallLogo.classList.add('hide');
    mouse.style.height = '90px';
  }
};