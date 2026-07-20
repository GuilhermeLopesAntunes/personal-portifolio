const RADIUS_X = 300;
const RADIUS_Y = 100;
const SPEED = 0.0005;
const MIN_SCALE = 0.5;
const MAX_SCALE = 1.1;
const MIN_OPACITY = 0.35;
const Y_OFFSET = 80;
const RADIUS_Y_FRONT = 120;  
const RADIUS_Y_BACK = 100;  

async function loadStacks() {
    const res = await fetch("http://127.0.0.1:8000/stacks");
    const stacks = await res.json()

    const container = document.getElementById("orbitIcons");
    const step = (Math.PI * 2) / stacks.length;

    stacks.forEach((stack, i) => {
        const img = document.createElement("img");
        img.src = `http://127.0.0.1:8000/assets/${stack.svg_icon}`;
        img.alt = stack.name;
        img.className = "orbit-icon";
        img.dataset.angle = step * i;
        container.appendChild(img);
    });

    animateOrbit();
}

function animateOrbit() {
    const icons = document.querySelectorAll(".orbit-icon");

    function frame(time) {
    icons.forEach(el => {
        const angle = parseFloat(el.dataset.angle) + time * SPEED;

        const depth = Math.sin(angle);      // ainda decide frente/trás
        const t = (depth + 1) / 2;

        const radiusY = depth < 0 ? RADIUS_Y_FRONT : RADIUS_Y_BACK;

        const x = Math.cos(angle) * RADIUS_X;
        const y = -depth * radiusY + Y_OFFSET;   // <- só inverti o sinal aqui (era: depth * radiusY)

        const scale = MAX_SCALE - t * (MAX_SCALE - MIN_SCALE);
        const opacity = (1 - t) * (1 - MIN_OPACITY) + MIN_OPACITY;
        const zIndex = t > 0.5 ? 1 : 10;

        el.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
        el.style.opacity = opacity;
        el.style.zIndex = zIndex;
    });

    requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
}

loadStacks();