/**
 * Canvas animations
 */

export const animateMultiplier = (
  ctx: CanvasRenderingContext2D,
  from: number,
  to: number,
  duration: number,
  callback: (value: number) => void
) => {
  const startTime = performance.now();
  const difference = to - from;
  
  const animate = (currentTime: number) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function (ease-out)
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = from + difference * eased;
    
    callback(current);
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  };
  
  requestAnimationFrame(animate);
};

export const drawGradient = (
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  color1: string,
  color2: string
) => {
  const gradient = ctx.createLinearGradient(x, y, x, y + height);
  gradient.addColorStop(0, color1);
  gradient.addColorStop(1, color2);
  ctx.fillStyle = gradient;
  ctx.fillRect(x, y, width, height);
};
