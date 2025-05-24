<script>
    import {
        AlertTriangleIcon,
        ChevronDownIcon,
        ChevronUpIcon,
    } from "svelte-feather-icons";

    const hoursArr = Array.from({ length: 25 }, (_, i) => i);
    const minutesArr = Array.from({ length: 61 }, (_, i) => i);

    let selectedHour = $state();
    let selectedMinute = $state();

    $inspect(selectedHour);
    $inspect(selectedMinute);



    function animatedScroll(node, isHours) {
        $effect(() => {


            

            let resetScrollTMID = 0;
            let startingDragY;
            let startingY;
            let animateTouchId;
            let scrolling = false;
            let animFrameId = 0;
            let isDragging = false;

            function setTop(target) {
                node.scrollTop = target;

                if(isHours) {
                    selectedHour = Math.round(target / 30);
                } else {
                    selectedMinute = Math.round(target / 30);
                }

            }

            function scrollTo(target, dontFix) {
                cancelAnimationFrame(animFrameId);
                function step() {
                    const dif = target - node.scrollTop;
                    /*node.scrollTop +=
                        dif < 0
                            ? Math.min(-1, dif * 0.2)
                            : Math.max(1, dif * 0.2);*/
                    setTop(
                        node.scrollTop +
                            (dif < 0
                                ? Math.min(-1, dif * 0.2)
                                : Math.max(1, dif * 0.2)),
                    );
                    if (Math.abs(target - node.scrollTop) < 2) {
                        /*node.scrollTop = target;*/
                        setTop(target);
                        window.cancelAnimationFrame(animFrameId);
                    } else {
                        animFrameId = window.requestAnimationFrame(step);
                    }
                }
                animFrameId = window.requestAnimationFrame(step);

                clearTimeout(resetScrollTMID);
                if (!dontFix) {
                    resetScrollTMID = setTimeout(() => {
                        window.cancelAnimationFrame(animFrameId);
                        scrollTo(Math.round(node.scrollTop / 30) * 30, true);
                    }, 100);
                }
            }
            let lastScroll = Date.now();
            let toScroll = 30;
            let prevScrollSign = 0;
            function handleWheel(e) {
                e.preventDefault();
                let nowSign = Math.sign(e.deltaY);
                let now = Date.now();
                if (now - lastScroll < 80 && prevScrollSign == nowSign) {
                    toScroll = Math.min(toScroll * 1.4, 500);
                } else {
                    toScroll = 30;
                }

                scrollTo(node.scrollTop + nowSign * toScroll);

                prevScrollSign = nowSign;
                lastScroll = now;
            }

            let velocity = 0;
            function handleTouchStart(e) {
                velocity = 0;
                startingDragY = e.touches[0].clientY;
                startingY = node.scrollTop;
                isDragging = true;
            }

            let prevTouch = 0;
            let prevTime = Date.now();
            function handleTouchMove(e) {
                e.preventDefault();
                let now = Date.now();
                let y = e.touches[0].clientY;

                velocity = (50 * (prevTouch - y)) / (now - prevTime);
                /*node.scrollTop = startingY + startingDragY - y;*/
                setTop(startingY + startingDragY - y);
                //scrollTo(startingY + startingDragY - y, true);

                prevTouch = y;
                prevTime = now;
            }

            function handleTouchEnd(e) {
                isDragging = false;
                animateTouchId = window.requestAnimationFrame(animateTouch);
            }
            function handleTouchCancel(e) {
                isDragging = false;
                animateTouchId = window.requestAnimationFrame(animateTouch);
                console.log("hi");
            }

            function animateTouch() {
                if (Math.abs(velocity) > 3) {
                    velocity *= 0.95;
                    /*node.scrollTop += velocity / 10;*/
                    setTop(node.scrollTop + (velocity / 10));
                    animateTouchId = window.requestAnimationFrame(animateTouch);
                } else {
                    window.cancelAnimationFrame(animFrameId);
                    window.cancelAnimationFrame(animateTouchId);
                    scrollTo(Math.round(node.scrollTop / 30) * 30, true);
                }
            }

            node.addEventListener("touchcancel", handleTouchCancel);
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
                node.removeEventListener("touchcancel", handleTouchCancel);
            };
        });
    }
</script>

<div class="wrap">
    <div class="scroll" use:animatedScroll={true}>
        <p class="scroll-item"><ChevronDownIcon size="30" /></p>
        {#each hoursArr as h}
            <p class="scroll-item">{h}</p>
        {/each}
        <p class="scroll-item"><ChevronUpIcon size="30" /></p>
    </div>
    <div>:</div>
    <div class="scroll" use:animatedScroll={false}>
        <p class="scroll-item"><ChevronDownIcon size="30" /></p>
        {#each minutesArr as m}
            <p class="scroll-item">{m}</p>
        {/each}
        <p class="scroll-item"><ChevronUpIcon size="30" /></p>
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
