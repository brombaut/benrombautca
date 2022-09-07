<template>
  <div class="image-carousel">
    <div class="images">
      <!-- Full-width images with number and caption text -->
      <div
        class="image-slide fade"
        v-for="img in images"
        :key="img.src">
        <!-- <div class="numbertext">{{ i+1 }} / {{ images.length }}</div> -->
        <img :src="img.src" />
      </div>

      <a class="prev" @click="plusSlides(-1)">&#10094;</a>
      <a class="next" @click="plusSlides(1)">&#10095;</a>
    </div>
    <div class="caption-text">
      {{ selectedImgCaptionText }}
    </div>
    <div class="dots">
      <span
        v-for="(image, i) in images"
        :key="image.src"
        class="dot"
        @click="currentSlide(i)">
      </span>
    </div>

  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { RunningImage } from "./types";

export default Vue.extend({
  name: "ImageCarousel",
  props: {
    images: {
      type: Array as PropType<RunningImage[]>,
      required: true,
    },
  },
  data() {
    return {
      slideIndex: 1,
    };
  },
  computed: {
    selectedImgCaptionText(): String {
      return this.images[this.slideIndex - 1].caption;
    },
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
      const slides: HTMLCollectionOf<HTMLDivElement> = this.$el.getElementsByClassName("image-slide") as HTMLCollectionOf<HTMLDivElement>;
      const dots = this.$el.getElementsByClassName("dot");
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
      slides[this.slideIndex - 1].style.display = "flex";
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
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  /* Slideshow container */
  .images {
    position: relative;
    background-color: $secondary;
    width: 520px;
    height: 500px;
    display: flex;
    // margin: auto;

    @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
      width: 320px;
      height: 300px;
    }

    @media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
      width: 220px;
      height: 200px;
    }

    .image-slide {
      /* Hide the images by default */
      display: none;
      align-items: center;
      justify-content: center;
      width: 100%;

      /* Number text (1/3 etc) */
      .numbertext {
        color: $primary;
        font-size: 12px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
      }

      img {
        display: block;
        max-width: 520px;
        max-height: 500px;
        width: auto;
        height: auto;
        margin-left: auto;
        margin-right: auto;
        margin-top: auto;
        margin-bottom: auto;

        @media only screen and (max-width: $SMALL_DISPLAY_SIZE) {
          max-width: 320px;
          max-height: 300px;
        }

        @media only screen and (max-width: $PHONE_DISPLAY_SIZE) {
          max-width: 220px;
          max-height: 200px;
        }
      }
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

    /* Next & previous buttons */
    .prev, .next {
      cursor: pointer;
      position: absolute;
      top: 50%;
      width: auto;
      margin-top: -22px;
      padding: 16px;
      color: $primary;
      font-weight: bold;
      font-size: 18px;
      transition: 0.6s ease;
      border-radius: 0 3px 3px 0;
      user-select: none;

      &:hover {
        background-color: rgba(0,0,0,0.8);
      }
    }

    /* Position the "next button" to the right */
    .next {
      right: 0;
      border-radius: 3px 0 0 3px;
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
  }

  .caption-text {
    margin-top: 8px;
  }

  .dots {
    text-align: center;
    margin: 8px 0;

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
  }

}
</style>
