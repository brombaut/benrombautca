
const checkSlide = function (elem: HTMLElement, elemEventListener: () => void) {
  if (elementIsVisible(elem)) {
    elem.classList.add("active");
    window.removeEventListener("scroll", elemEventListener);
  }
};

const checkHorizontalFadeIn = function (elem: HTMLElement, elemEventListener: () => void) {
  if (elementIsVisible(elem)) {
    window.removeEventListener("scroll", elemEventListener);
    setTimeout(() => {
      elem.classList.add("active");
    }, calculateHorizontalElemFadeInDelay(elem));
  }
};

const elementIsVisible = function (elem: HTMLElement) {
  const boundingRect: DOMRect = elem.getBoundingClientRect();
  const { width, height } = boundingRect;
  const slideInAt = (window.scrollY + window.innerHeight - height / 4);
  const imageBottom = elem.offsetTop + height;
  const isShown = slideInAt > elem.offsetTop;
  const isScrolledPast = window.scrollY < imageBottom;
  return isShown && isScrolledPast;
};

const calculateHorizontalElemFadeInDelay = function (elem: HTMLElement) {
  const boundingRect: DOMRect = elem.getBoundingClientRect();
  const parentElem: HTMLElement = elem.parentNode as HTMLElement;
  const parendBoundingRect: DOMRect = parentElem.getBoundingClientRect();
  const elemX: number = boundingRect.x;
  const parentWidth: number = parendBoundingRect.width;
  const xPositionRatio: number = elemX / parentWidth;
  const maxFadeInDelayMilliseconds = 800;
  const elemFadeIn: number = xPositionRatio * maxFadeInDelayMilliseconds;
  return elemFadeIn;
};

const loadImage = function (imageFileName: string) {
  if (!imageFileName) {
    return "";
  }
  const images = require.context("../assets/images/", false, /(\.jpg || \.png)$/);
  return images(`./${imageFileName}`);
};

export default {
  checkSlide,
  checkHorizontalFadeIn,
  loadImage,
};
