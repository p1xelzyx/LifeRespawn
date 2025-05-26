<script>
    let isHidden = $state(true);

    let intervalId = 0;

    let duration = $state(0);
    let information = $state("");
    
    let barColor = $state("neutral");
    let barColors = {positive: "lime", neutral: "var(--main-color)", negative: "red"};


    export async function start(config) {
        if(!isHidden) {
            stop();
            await new Promise((resolve) => {
                setTimeout(resolve, 210);
            });
        }


        config = config ?? {}

        duration = config.time ?? 5000;
        information = config.text ?? "";
        barColor = config.type ?? "neutral";

        isHidden = false;
        clearInterval(intervalId);
        intervalId = setTimeout(() => {
            isHidden = true;
        }, duration);
    }

    export function stop() {
        isHidden = true;
    }
</script>

<div class:hidden={isHidden} role="alert" onfocus={stop} onmouseover={stop}>
    <div class="bar" class:movebar={!isHidden} style="--duration: {duration}ms; --bar-color: {barColors[barColor]}"></div>
    <p>{information}</p>
</div>

<style>
    div {
        width: 400px;
        max-width: 100vw;
        background-color: #111111;
        position: fixed;
        left: 50%;
        bottom: 0px;
        transform: translateX(-50%);
        overflow: hidden;
        transition: all 0.1s;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        box-shadow: 0px 12px 16px 0px #111111;
        z-index: 10;
    }
    .hidden {
        /*visibility: hidden;*/
        transform: translate(-50%, 100%);
    }
    .bar {
        border-radius: 0;
        position: absolute;
        top: 0;
        height: 7px;
        width: 100%;
        background-color: var(--bar-color);
        transform: translateX(-50%);
        box-shadow: none;
    }
    .movebar {
        transform: translateX(-150%);
        transition: transform var(--duration) linear;
    }

    p {
        color: white;
        font-size: 1.2em;
        margin: 22px;
    }
</style>