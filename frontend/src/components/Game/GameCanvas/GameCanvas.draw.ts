/**
 * Canvas drawing logic
 */

export interface Point {
  x: number;
  y: number;
}

export class CanvasDrawer {
  private ctx: CanvasRenderingContext2D;
  private points: Point[] = [];
  private maxPoints = 1000;
  
  constructor(ctx: CanvasRenderingContext2D) {
    this.ctx = ctx;
  }
  
  addPoint(multiplier: number, width: number, height: number) {
    const x = (this.points.length / this.maxPoints) * width;
    const y = height - (multiplier - 1) * (height / 10); // Scale for multipliers up to 10x
    
    this.points.push({ x, y });
    
    if (this.points.length > this.maxPoints) {
      this.points.shift();
    }
  }
  
  draw() {
    if (this.points.length < 2) return;
    
    this.ctx.beginPath();
    this.ctx.moveTo(this.points[0].x, this.points[0].y);
    
    for (let i = 1; i < this.points.length; i++) {
      this.ctx.lineTo(this.points[i].x, this.points[i].y);
    }
    
    this.ctx.stroke();
  }
  
  clear() {
    this.points = [];
  }
}
