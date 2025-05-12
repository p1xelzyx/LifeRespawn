<script>
    import { XIcon } from 'svelte-feather-icons'


    let isShown = $state(false);
    let moodValue = $state(5);
    let valueDisplayColor = $derived(`hsl(${moodValue * 12}, 100%, 50%)`);

    export function show() {
        isShown = true;
    }

    export function hide() {
        isShown = false;
    }

    function clickOutside(node) {
        const handleOutside = (event) => {
            if (!node.contains(event.target)) {
                hide();
            }
        };
        document.addEventListener("click", handleOutside, true);
        return {
            destroy() {
                document.removeEventListener("click", handleOutside, true);
            },
        };
    }
</script>

<div class="wrap" class:hidden={!isShown} class:shown={isShown}>
    <div use:clickOutside class="content">
        <button onclick={hide} class="close-x"><XIcon size=30 strokeWidth=2/></button>
        <h1>How do you feel?</h1>
        <input type="range" step=0.1 min=0 max=10 bind:value={moodValue}>
        <h1 style="color: {valueDisplayColor}">{moodValue}/10</h1>
        <div class="form-buttons">
            <button class="end-button" >Ok</button>
            <button class="end-button" onclick={hide}>Cancel</button>
        </div>
    </div>
</div>

<style>
    h1 {
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 50px;
    }

    input {
        width: 500px;
        margin-bottom: 20px;
    }

    .hidden {
        display: none;
    }
    .shown {
        display: flex;
    }

    .wrap {
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px);
    }
    .content {
        box-shadow: 0 0 25px 4px rgba(0, 0, 0, 0.459);
        position: relative;
        width: 80%;
        height: 80%;
        color: white;
        padding: 30px;
        background-color: var(--bg-color);
        border-radius: 15px;
        overflow: hidden;

        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }

    .close-x {
        position: absolute;
        right: 0;
        top: 0;
        width: 50px;
        height: 50px;
        color: white;
        background-color: transparent;
        transition: all 0.2s;
    }

    .close-x:hover {
        background-color: red;
    }

    .end-button {
        font-size: 1.4em;
        border: 2px solid var(--main-color);
        color: var(--main-color);
        border-radius: 15px;
        padding: 20px;
        margin: 15px;
        transition: 0.1s all;
        background-color: transparent;
    }
    .end-button:hover {
        color: white;
        background-color: var(--main-color);
    }


</style>
