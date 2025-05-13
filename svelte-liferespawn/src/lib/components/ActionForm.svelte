<script>
    import { Window } from "$components";

    let window = $state();

    export function show() {
        window.show();
    }
</script>

<Window bind:this={window}>
    <h1>hello!</h1>
</Window>

<style>
    h1 {
        color: red;
    }
</style>
