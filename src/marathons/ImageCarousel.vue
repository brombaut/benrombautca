<template>
  <div class="image-carousel">
    <div class="images">
      <!-- Full-width images with number and caption text -->
      <div
        class="image-slide fade"
        v-for="(image, i) in images"
        :key="image">
        <div class="numbertext">{{ i }} / {{ images.length }}</div>
        <img :src="image" />
        <!-- TODO: Maybe add this later? -->
        <!-- <div class="text">Caption Text</div> -->
      </div>

      <a class="prev" @click="plusSlides(-1)">&#10094;</a>
      <a class="next" @click="plusSlides(1)">&#10095;</a>
    </div>
    <div class="dots">
      <span
        v-for="(image, i) in images"
        :key="image"
        class="dot"
        @click="currentSlide(i)">
      </span>
    </div>

  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

export default Vue.extend({
  name: "ImageCarousel",
  props: {
    images: {
      type: Array as PropType<String[]>,
      required: true,
    },
  },
  data() {
    return {
      slideIndex: 1,
    };
  },
  methods: {
    plusSlides(n: number) {
      this.slideIndex += n;
      this.showSlides(this.slideIndex);
    },
    currentSlide(n: number) {
      this.slideIndex = n;
      this.showSlides(this.slideIndex);
    },
    showSlides(n: number) {
      let i;
      const slides: HTMLCollectionOf<HTMLDivElement> = document.getElementsByClassName("image-slide") as HTMLCollectionOf<HTMLDivElement>;
      const dots = document.getElementsByClassName("dot");
      if (n > slides.length) {
        this.slideIndex = 1;
      }
      if (n < 1) {
        this.slideIndex = slides.length;
      }
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[this.slideIndex - 1].style.display = "block";
      dots[this.slideIndex - 1].className += " active";
    },
  },
  mounted() {
    this.showSlides(this.slideIndex);
  },
});
</script>

<style lang="scss">
.image-carousel {
  box-sizing: border-box;

  /* Slideshow container */
  .images {
    max-width: 1000px;
    position: relative;
    margin: auto;
  }

  /* Hide the images by default */
  .image-slide {
    display: none;
    width: 100%;
  }

  /* Next & previous buttons */
  .prev, .next {
    cursor: pointer;
    position: absolute;
    top: 50%;
    width: auto;
    margin-top: -22px;
    padding: 16px;
    color: white;
    font-weight: bold;
    font-size: 18px;
    transition: 0.6s ease;
    border-radius: 0 3px 3px 0;
    user-select: none;
  }

  /* Position the "next button" to the right */
  .next {
    right: 0;
    border-radius: 3px 0 0 3px;
  }

  /* On hover, add a black background color with a little bit see-through */
  .prev:hover, .next:hover {
    background-color: rgba(0,0,0,0.8);
  }

  /* Caption text */
  .text {
    color: #f2f2f2;
    font-size: 15px;
    padding: 8px 12px;
    position: absolute;
    bottom: 8px;
    width: 100%;
    text-align: center;
  }

  /* Number text (1/3 etc) */
  .numbertext {
    color: #f2f2f2;
    font-size: 12px;
    padding: 8px 12px;
    position: absolute;
    top: 0;
  }

  .dots {
    text-align: center;
  }

  /* The dots/bullets/indicators */
  .dot {
    cursor: pointer;
    height: 15px;
    width: 15px;
    margin: 0 2px;
    background-color: $primaryDark;
    border-radius: 50%;
    display: inline-block;
    transition: background-color 0.6s ease;
  }

  .active, .dot:hover {
    background-color: $primary;
  }

  /* Fading animation */
  .fade {
    animation-name: fade;
    animation-duration: 0.5s;
  }

  @keyframes fade {
    from {opacity: .7}
    to {opacity: 1}
  }

}
</style>
