<script>
    const hoursArr = Array.from({ length: 25 }, (_, i) => i);
    const minutesArr = Array.from({ length: 61 }, (_, i) => i);

    function animatedScroll(node) {
        $effect(() => {
            console.log(node.scrollTop);

            let startingDragY;
            let startingY;

            let scrolling = false;
            let animFrameId = 0;
            function scrollTo(target) {
                cancelAnimationFrame(animFrameId);

                function step() {
                    const dif = target - node.scrollTop;
                    node.scrollTop +=
                        dif < 0
                            ? Math.min(-1, dif * 0.2)
                            : Math.max(1, dif * 0.2);
                    if (Math.abs(target - node.scrollTop) < 2) {
                        node.scrollTop = target;
                        window.cancelAnimationFrame(animFrameId);
                    } else {
                        animFrameId = window.requestAnimationFrame(step);
                    }
                }
                animFrameId = window.requestAnimationFrame(step);

            }
            let lastScroll = Date.now();
            let toScroll = 30;
            let resetScrollTMID = 0;
            function handleWheel(e) {

                e.preventDefault();
                let now = Date.now();
                if (now - lastScroll < 80) {
                    toScroll = Math.min(toScroll * 1.4, 500);
                } else {
                    toScroll = 30;
                }
                clearTimeout(resetScrollTMID);
                resetScrollTMID = setTimeout(() => {
                    window.cancelAnimationFrame(animFrameId);
                    scrollTo(Math.round(node.scrollTop / 30) * 30);
                }, 100);
                scrollTo(node.scrollTop + Math.sign(e.deltaY) * toScroll);

                lastScroll = now;
            }

            function handleTouchStart(e) {
                startingDragY = e.touches[0].clientY;
                startingY = node.scrollTop;
            }
            function handleTouchMove(e) {
                e.preventDefault();
                let y = e.touches[0].clientY;
                node.scrollTop = startingY + startingDragY - y;
            }
            function handleTouchEnd(e) {
                //scrollTo(Math.round(node.scrollTop / 30) * 30);
            }
            /*function handleTouchCancel(e) {
            }*/

            //node.addEventListener("touchcancel", handleTouchCancel);
            node.addEventListener("touchstart", handleTouchStart);
            node.addEventListener("touchmove", handleTouchMove, {
                passive: false,
            });
            node.addEventListener("touchend", handleTouchEnd);
            node.addEventListener("wheel", handleWheel, { passive: false });
            return () => {
                node.removeEventListener("touchstart", handleTouchStart);
                node.removeEventListener("touchmove", handleTouchMove, {
                    passive: false,
                });
                node.removeEventListener("touchend", handleTouchEnd);
                node.removeEventListener("wheel", handleWheel, {
                    passive: false,
                });
                //node.removeEventListener("touchcancel", handleTouchCancel);
            };
        });
    }
</script>

<div class="wrap">
    <div class="scroll" use:animatedScroll>
        <p>&nbsp;</p>
        {#each hoursArr as h}
            <p>{h}</p>
        {/each}
        <p>&nbsp;</p>
    </div>
    <div>:</div>
    <div class="scroll" use:animatedScroll>
        <p>&nbsp;</p>
        {#each minutesArr as m}
            <p>{m}</p>
        {/each}
        <p>&nbsp;</p>
    </div>
</div>

<style>
    .wrap {
        align-items: center;
        display: flex;
        gap: 5px;
        font-size: 2em;
        height: 90px;
    }

    .scroll {
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        text-align: center;
    }
    .scroll p {
        display: block;
        font-size: 25px;
        height: 30px;
    }
</style>
