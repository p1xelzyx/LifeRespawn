<script>
    let isShown = $state(false);
    export function show() {
        isShown = true;
    }

    function clickOutside(node) {
        const handleOutside = (event) => {
            if (!node.contains(event.target)) {
                isShown = false;
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
        hello
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
        position: absolute;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100vw;
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
        border-radius: 30px;
    }
</style>