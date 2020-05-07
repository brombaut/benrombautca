<template>
  <canvas ref="mouseTrailerCanvas" :width="cWidth" :height="cHeight" />
</template>

<script lang="ts">
/**
 * Ported to this Vue Class Component from https://noahyamamoto.com/blog/mousetrailanimation
 */
import { Component, Vue } from "vue-property-decorator";
import { ResizeObserver } from "resize-observer";
import Point from "../types/point";

@Component
export default class MouseTrailer extends Vue {
  private cHeight = 0;

  private cWidth = 0;

  private canvas!: HTMLCanvasElement;

  private ctx!: CanvasRenderingContext2D;

  private points: Point[] = [];

  private duration!: number;

  mounted() {
    this.canvas = this.$el as HTMLCanvasElement;
    this.setStateDimensions();
    this.setDuration();
    if (matchMedia("(pointer:fine)").matches) {
      this.startAnimation();
    }

    const resizeObserver = new ResizeObserver(() => {
      this.setStateDimensions();
    });
    resizeObserver.observe(this.$parent.$el);
  }

  beforeDestroy() {
    document.removeEventListener("mousemove", this.mouseMoveListener);
  }

  setStateDimensions() {
    this.cHeight = this.$parent.$el.clientHeight - 8;
    this.cWidth = this.$parent.$el.clientWidth - 8;
  }

  setDuration() {
    this.duration = 0.7 * (1 * 1000); // Last 80% of a frame per point
    this.duration /= 60;
  }

  startAnimation() {
    this.canvas = this.$refs.mouseTrailerCanvas as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;
    document.addEventListener("mousemove", this.mouseMoveListener);
    this.animatePoints();
  }

  mouseMoveListener(e: MouseEvent) {
    const x = e.clientX - this.canvas.offsetLeft;
    const y = e.pageY - this.canvas.offsetTop;
    this.addPoint(x, y);
  }

  addPoint(x: number, y: number) {
    const point = new Point(x, y);
    this.points.push(point);
  }

  animatePoints() {
    if (!this.ctx) {
      return;
    }
    this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);

    for (let i = 0; i < this.points.length; ++i) {
      const point = this.points[i];
      const lastPoint = this.getLastPoint(i);
      point.lifetime += 1;
      if (point.lifetime > this.duration) {
        this.points.shift();
      } else {
        this.animatePoint(point, lastPoint);
      }
    }
    requestAnimationFrame(this.animatePoints);
  }

  getLastPoint(i: number) {
    if (this.points[i - 1] !== undefined) {
      return this.points[i - 1];
    }
    return this.points[i];
  }

  animatePoint(point: Point, lastPoint: Point) {
    // As the lifetime goes on, lifePercent goes from 0 to 1.
    const lifePercent = point.lifetime / this.duration;
    const spreadRate = 7 * (1 - lifePercent);

    this.ctx.lineJoin = "round";
    this.ctx.lineWidth = spreadRate;

    // As time increases decrease r and b, increase g to go from purple to green.
    const red = Math.floor(51 - 51 * lifePercent);
    const green = Math.floor(129 - 129 * lifePercent);
    const blue = Math.floor(219 + 219 * lifePercent);
    this.ctx.strokeStyle = `rgb(${red},${green},${blue}`;

    this.ctx.beginPath();
    this.ctx.moveTo(lastPoint.x, lastPoint.y);
    this.ctx.lineTo(point.x, point.y);
    this.ctx.stroke();
    this.ctx.closePath();
  }
}
</script>

<style lang="scss">
canvas {
  position: absolute;
  z-index: 1;
}
</style>
