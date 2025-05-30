<script>
    let tmpData = $state([
        { date: { month: 4, year: 2025, day: 28 }, value: 8.8 },
        { date: { month: 4, year: 2025, day: 27 }, value: 2 },
        { date: { month: 4, year: 2025, day: 26 }, value: 7 },
        { date: { month: 4, year: 2025, day: 25 }, value: 4 },
        { date: { month: 4, year: 2025, day: 24 }, value: 5 },
        { date: { month: 4, year: 2025, day: 23 }, value: 6 },
        { date: { month: 4, year: 2025, day: 22 }, value: 6 },
        { date: { month: 4, year: 2025, day: 21 }, value: 1 },
        { date: { month: 4, year: 2025, day: 20 }, value: 1 },
        { date: { month: 4, year: 2025, day: 19 }, value: 5 },
        { date: { month: 4, year: 2025, day: 18 }, value: 10 },
        { date: { month: 4, year: 2025, day: 17 }, value: 2.2 },
        { date: { month: 4, year: 2025, day: 16 }, value: 9 },
        { date: { month: 4, year: 2025, day: 15 }, value: 7 },
        { date: { month: 4, year: 2025, day: 14 }, value: 5 },
        { date: { month: 4, year: 2025, day: 13 }, value: 7 },
        { date: { month: 4, year: 2025, day: 12 }, value: 4 },
        { date: { month: 4, year: 2025, day: 11 }, value: 5 },
        { date: { month: 4, year: 2025, day: 10 }, value: 9 },
        { date: { month: 4, year: 2025, day: 9 }, value: 9.7 },
        { date: { month: 4, year: 2025, day: 8 }, value: 4.2 },
        { date: { month: 4, year: 2025, day: 7 }, value: 2 },
        { date: { month: 4, year: 2025, day: 6 }, value: 6.7 },
        { date: { month: 4, year: 2025, day: 5 }, value: 6.2 },
        { date: { month: 4, year: 2025, day: 4 }, value: 4.4 },
        { date: { month: 4, year: 2025, day: 3 }, value: 6 },
    ]);

    let canvas = $state();
    let offset = $state(0);

    let zoom = $state(0.1);

    function draw(canvas, offset, data) {
        let ctx = canvas.getContext("2d");
        canvas.width = canvas.clientWidth;
        canvas.height = canvas.clientHeight;

        const difX = canvas.width * zoom;

        ctx.fillStyle = "rgb(37,37,37)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.font = `bold ${Math.max(14, canvas.width * 0.027)}px montserrat, sans-serif`;

        let points = [];
        let i = 0;
        let lastNamePlaced = 0;
        for (let i in data) {
            let d = data[i];

            let x = canvas.width + offset - canvas.width * 0.1 - i * difX;
            let y =
                canvas.height -
                (d.value / 10) * canvas.height * 0.8 -
                canvas.height * 0.1;

            if (x + difX < 0) {
                break;
            }
            if (x <= canvas.width + difX) {
                //let prev = i > 0 ? points[points.length - 1] : false;

                let currentText = `${d.date.day}.${d.date.month}.${d.date.year}`;
                let w = ctx.measureText(currentText).width;
                //let w2 = prev ? ctx.measureText(pre.name).width : 0;
                //console.log(w, prev?.x - x);

                let ok = true;

                if (lastNamePlaced - x < w + 10 && points.length != 0) {
                    ok = false;
                } else {
                    lastNamePlaced = x;
                }

                points.push({
                    x,
                    y,
                    name: ok ? currentText : "",
                });
            }

            i++;
        }

        let xL =
            canvas.width -
            canvas.width * 0.1 +
            (offset % canvas.width) -
            difX * 0;
        while (xL >= 0) {
            //let x = canvas.width - canvas.width * 0.1 + offset - difX * i1;

            if (
                points.find((e) => Math.floor(e.x) === Math.floor(xL) && e.name)
            ) {
                ctx.strokeStyle = "rgba(20, 97, 222, 0.8)";
            } else {
                ctx.strokeStyle = "rgba(255,255,255, 0.2)";
            }
            ctx.beginPath();
            ctx.moveTo(xL, 0);
            ctx.lineTo(xL, canvas.height);
            ctx.stroke();

            xL -= difX;
        }
        ctx.strokeStyle = "rgba(255,255,255,0.2)";

        for (let i = 1; i <= 10; i++) {
            let y =
                canvas.height -
                (i / 10) * canvas.height * 0.8 -
                canvas.height * 0.1;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();

            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.fillText(i, 10, y - 5);
        }

        ctx.strokeStyle = "#1461de";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(points[0]?.x, points[0]?.y);
        for (let p of points.slice(1)) {
            ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();

        for (let p of points) {
            ctx.fillStyle = "rgb(37,37,37)";
            ctx.beginPath();
            ctx.arc(p.x, p.y, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#1461de";
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
            ctx.fill();
            if (p.name)
                ctx.fillText(
                    p.name,
                    p.x - ctx.measureText(p.name).width / 2,
                    canvas.height - 20,
                );
        }
    }

    $effect(() => {
        draw(canvas, offset, tmpData);
    });
    let mouseX = 0;
    function canvasAction(canvas) {
        const resizeObserver = new ResizeObserver(() => {
            draw(canvas, offset, tmpData);
        });

        resizeObserver.observe(canvas);

        function onWheel(e) {
            let prevZoom = zoom;
            e.preventDefault();
            if (!e.shiftKey) {
                offset = Math.min(
                    Math.max(offset + e.deltaY, 0),
                    canvas.width * zoom * tmpData.length,
                );
            } else {
                zoom = Math.max(
                    Math.min(zoom * (e.deltaY < 0 ? 1.3 : 1 / 1.3), 0.1),
                    0.1 / 1.3 ** 10,
                );
                offset = Math.min(
                    Math.max(
                        (offset + (canvas.width * 0.9 - mouseX)) *
                            (zoom / prevZoom) -
                            (canvas.width * 0.9 - mouseX),
                        0,
                    ),
                    canvas.width * zoom * tmpData.length,
                );
            }
        }
        function onMouse(e) {
            mouseX = e.offsetX;
        }

        let beginTouch = 0;
        function onTouchStart(e) {
            beginTouch = e.touches[0].clientX;
        }
        function onTouchMove(e) {
            e.preventDefault();


            offset = Math.min(
                Math.max(offset + e.touches[0].clientX - beginTouch, 0),
                canvas.width * zoom * tmpData.length,
            );
            beginTouch = e.touches[0].clientX;
        }
        canvas.addEventListener("touchstart", onTouchStart);
        canvas.addEventListener("touchmove", onTouchMove);

        canvas.addEventListener("wheel", onWheel);
        canvas.addEventListener("mousemove", onMouse);

        return {
            destroy: () => {
                canvas.removeEventListener("touchstart", onTouchStart);
                canvas.removeEventListener("touchmove", onTouchMove);
                resizeObserver.disconnect();
                canvas.addEventListener("mousemove", onMouse);
                canvas.removeEventListener("wheel", onWheel);
            },
        };
    }
</script>

<div class="wrap">
    <select>
        <option value="week">week</option>
        <option value="month">month</option>
        <option value="year">year</option>
        <option value="5years">5 years</option>
        <option value="max">max</option>
    </select>
    <canvas bind:this={canvas} use:canvasAction></canvas>
</div>

<style>
    .wrap {
        width: 100%;
        max-width: 700px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: end;
        margin-bottom: 40px;
    }
    select {
        margin-bottom: 10px;
        font-size: 1.2em;
        background-color: rgb(37, 37, 37);
        color: white;
        padding: 5px;
        outline: none;
    }

    canvas {
        width: 100%;
        aspect-ratio: 1;
        border: 2px solid rgb(110, 110, 110);
    }
</style>
