interface PercentVisible {
  section: string;
  percentVisible: number;
}

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

const percentElementIsVisible = function(elem: HTMLElement): number {
  let percentVisible = 0.0;
  const boundingRect: DOMRect = elem.getBoundingClientRect();
  const elemTopPos = window.scrollY + boundingRect.top;
  const elemBottomPos = elemTopPos + boundingRect.height;
  const windowTopPos = window.scrollY;
  const windowBottomPos = window.scrollY + window.innerHeight;
  // Elem is above window viewport
  if (elemBottomPos < windowTopPos) {
    return percentVisible;
  }
  // Elem is below window viewport
  if (elemTopPos > windowBottomPos) {
    return percentVisible;
  }

  const windowHeight = windowBottomPos - windowTopPos;
  // Elem is fully visible in viewport
  if (elemTopPos >= windowTopPos && elemBottomPos <= windowBottomPos) {
    const elemHeight = boundingRect.height;
    percentVisible = elemHeight / windowHeight;
    return percentVisible;
  }

  // Element is fully visible, but top and bottom are cut off
  if (elemTopPos <= windowTopPos && elemBottomPos >= windowBottomPos) {
    percentVisible = 1.0;
    return percentVisible;
  }

  // Top of element is visible, but bottom is cut off in window viewport
  if (elemTopPos >= windowTopPos && elemBottomPos > windowBottomPos) {
    const elemVisibleHeight = windowBottomPos - elemTopPos;
    percentVisible = elemVisibleHeight / windowHeight;
    return percentVisible;
  }

  // Bottom of element is visible, but top is cut off in window viewport
  if (elemTopPos < windowTopPos && elemBottomPos <= windowBottomPos) {
    const elemVisibleHeight = elemBottomPos - windowTopPos;
    percentVisible = elemVisibleHeight / windowHeight;
    return percentVisible;
  }
  return percentVisible;
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

const percentSectionIsVisible = function(elId: string): number {
  let result = 0;
  const el = document.querySelector(`#${elId}`);
  if (el) {
    result = percentElementIsVisible(el as HTMLElement);
  }
  return result;
};

const getSectionsPercentVisible = function(): PercentVisible[] {
  const aboutMePercentVisible = {
    section: "about-me",
    percentVisible: percentSectionIsVisible("about-me"),
  };
  const workPercentVisible = {
    section: "work",
    percentVisible: percentSectionIsVisible("work"),
  };
  const educationPercentVisible = {
    section: "education",
    percentVisible: percentSectionIsVisible("education"),
  };
  const bookshelfPercentVisible = {
    section: "bookshelf",
    percentVisible: percentSectionIsVisible("bookshelf"),
  };
  const result: PercentVisible[] = [
    aboutMePercentVisible,
    workPercentVisible,
    educationPercentVisible,
    bookshelfPercentVisible,
  ];
  return result.sort((a: PercentVisible, b: PercentVisible) => {
    if (a.percentVisible > b.percentVisible) {
      return -1;
    }
    return 1;
  });
};

export default {
  checkSlide,
  checkHorizontalFadeIn,
  loadImage,
  percentElementIsVisible,
  getSectionsPercentVisible,
};
