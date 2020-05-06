const checkSlide = function(elem: HTMLElement, elemEventListener: () => void) {
  const boundingRect: DOMRect = elem.getBoundingClientRect();
  const { width, height } = boundingRect;
  const slideInAt = (window.scrollY + window.innerHeight - height / 2);
  const imageBottom = elem.offsetTop + height;
  const isHalfShown = slideInAt > elem.offsetTop;
  const isHalfScrolledPast = window.scrollY < imageBottom;
  if (isHalfShown && isHalfScrolledPast) {
    elem.classList.add("active");
    window.removeEventListener("scroll", elemEventListener);
  }
};

export default {
  checkSlide
};
