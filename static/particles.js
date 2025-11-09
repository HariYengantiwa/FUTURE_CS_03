(function(){
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let w, h, particles;


function resize(){
w = canvas.width = window.innerWidth;
h = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();


function rand(min,max){ return Math.random()*(max-min)+min }


function createParticles(n){
particles = [];
for(let i=0;i<n;i++){
particles.push({
x: rand(0,w), y: rand(0,h),
vx: rand(-0.3,0.3), vy: rand(-0.3,0.3),
r: rand(0.6,2.6),
life: rand(60,300)
});
}
}
createParticles(Math.round((w*h)/90000));


function tick(){
ctx.clearRect(0,0,w,h);
// mild additive glow
for(let p of particles){
p.x += p.vx; p.y += p.vy;
p.life -= 1;
if(p.x< -10) p.x = w+10; if(p.x> w+10) p.x=-10;
if(p.y< -10) p.y = h+10; if(p.y> h+10) p.y=-10;
if(p.life<=0){ p.x=rand(0,w); p.y=rand(0,h); p.vx=rand(-0.3,0.3); p.vy=rand(-0.3,0.3); p.life = rand(60,300)}
// draw
const grad = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*8);
grad.addColorStop(0, 'rgba(85,170,255,0.85)');
grad.addColorStop(0.25, 'rgba(85,170,255,0.5)');
grad.addColorStop(1, 'rgba(85,170,255,0)');
ctx.fillStyle = grad;
ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
}
requestAnimationFrame(tick);
}
tick();
})();