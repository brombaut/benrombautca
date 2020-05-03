<template>
  <canvas ref="mouseTrailerCanvas" :width="cWidth" :height="cHeight" />
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Point from "../types/point";

@Component
export default class MouseTrailer extends Vue {
  private cHeight = 0;

  private cWidth = 0;

  private canvas!: HTMLCanvasElement;

  mounted() {
    this.canvas = this.$el as HTMLCanvasElement;
    this.setStateDimensions();

    window.addEventListener("resize", this.setStateDimensions, false);

    // If the device supports cursors, start animation.
    if (matchMedia("(pointer:fine)").matches) {
      this.startAnimation();
    }
  }

  setStateDimensions() {
    this.cHeight = document.body.clientHeight - 8;
    this.cWidth = document.body.clientWidth - 8;
  }

  startAnimation = () => {
    const canvas = this.$refs.mouseTrailerCanvas as HTMLCanvasElement;
    const ctx = canvas.getContext("2d");

    const points: Point[] = [];

    const addPoint = (x: number, y: number) => {
      const point = new Point(x, y);
      points.push(point);
    };

    document.addEventListener(
      "mousemove",
      e => {
        const x = e.clientX - canvas.offsetLeft;
        const y = e.pageY - canvas.offsetTop;
        addPoint(x, y);
      },
      false
    );

    const animatePoints = () => {
      if (!ctx) {
        return;
      }
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      let duration = 0.7 * (1 * 1000); // Last 80% of a frame per point
      duration /= 60;

      for (let i = 0; i < points.length; ++i) {
        const point = points[i];
        let lastPoint;

        if (points[i - 1] !== undefined) {
          lastPoint = points[i - 1];
        } else {
          lastPoint = point;
        }

        point.lifetime += 1;

        if (point.lifetime > duration) {
          // If the point dies, remove it.
          points.shift();
        } else {
          // Otherwise animate it:

          // As the lifetime goes on, lifePercent goes from 0 to 1.
          const lifePercent = point.lifetime / duration;
          const spreadRate = 7 * (1 - lifePercent);

          ctx.lineJoin = "round";
          ctx.lineWidth = spreadRate;

          // As time increases decrease r and b, increase g to go from purple to green.
          const red = Math.floor(51 - 51 * lifePercent);
          const green = Math.floor(129 - 129 * lifePercent);
          const blue = Math.floor(219 + 219 * lifePercent);
          ctx.strokeStyle = `rgb(${red},${green},${blue}`;

          ctx.beginPath();

          ctx.moveTo(lastPoint.x, lastPoint.y);
          ctx.lineTo(point.x, point.y);

          ctx.stroke();
          ctx.closePath();
        }
      }
      requestAnimationFrame(animatePoints);
    };

    animatePoints();
  };
}
</script>

<style lang="scss">
canvas {
  position: absolute;
  z-index: 1;
}
</style>
