<script>
    import { XIcon } from "svelte-feather-icons";

    let {
        children,
        flex,
        width = "auto",
        height = "auto",
        minWidth = "auto",
        minHeight = "auto",
    } = $props();

    let isShown = $state(false);

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
    <div
        style="--width: {width}; --height: {height}; --minWidth: {minWidth}; --minHeight:{minHeight}"
        use:clickOutside
        class="content"
        class:flex
    >
        <button onclick={hide} class="close-x">
            <XIcon size="30" strokeWidth="2" />
        </button>
        {@render children()}
    </div>
</div>

<style>
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
        box-shadow: 0px 0px 16px -5px rgba(0, 0, 0, 1);
        position: relative;

        width: var(--width);
        height: var(--height);
        min-width: var(--minWidth);
        min-height: var(--minHeight);

        color: white;
        padding: 60px;
        background-color: var(--bg-color);
        border-radius: 15px;
        overflow: hidden;
    }
    .flex {
        display: flex;
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
</style>
