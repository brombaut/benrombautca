export default class Point {
  x: number;

  y: number;

  lifetime: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
    this.lifetime = 0;
  }
}
