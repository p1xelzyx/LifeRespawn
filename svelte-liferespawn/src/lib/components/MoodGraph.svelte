<script>
    import { logout } from "$utils/logout";

    let selectedAvg = $state("1");
    $inspect(selectedAvg);

    let tmpData = $state([]);
    let offset = $state(0);
    let zoom = $state(0.1);

    $effect(async () => {
        tmpData = (await getData(Number(selectedAvg)))?.reverse();
    });

    $inspect(tmpData);

    async function getData(avg) {
        const response = await fetch("/api/post", {
            method: "post",
            body: JSON.stringify({
                endpoint: "mood_graph",
                data: { avg: avg },
            }),
        });
        if (response.status === 401) logout();
        if (!response.ok) alert("error");

        let data = await response.json();

        if (data.status === "success") {
            return data.history;
        } else {
            return [];
        }
    }

    let canvas = $state();

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
                d.value > 0
                    ? canvas.height -
                      (d.value / 10) * canvas.height * 0.8 -
                      canvas.height * 0.1
                    : false;

            if (x + difX * 3 < 0) {
                break;
            }
            if (x <= canvas.width + difX * 3) {
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
                points.find((e) => Math.floor(e.x) === Math.floor(xL) && e.name && e.y !== false)
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
            if (p.y === false) continue;
            ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();

        for (let p of points) {
            if (p.y !== false) {
                ctx.fillStyle = "rgb(37,37,37)";
                ctx.beginPath();
                ctx.arc(p.x, p.y, 7, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "#1461de";
                ctx.beginPath();
                ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
                ctx.fill();
            }
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
    <select bind:value={selectedAvg}>
        <option value="1">1 day</option>
        <option value="7">1 week</option>
        <option value="30">1 month</option>
        <option value="365">1 year</option>
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
