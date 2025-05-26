<script>
    import { Window } from "$components";

    let { analysis } = $props();

    let window = $state();

    export function show() {
        window.show();
    }

</script>

<Window>
    <h1>Analysis</h1>
</Window>

<style>
    h1 {
        text-align: center;
    }
</style>



