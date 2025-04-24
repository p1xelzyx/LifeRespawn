<script>
    import "../app.css";


    let { children } = $props();

    import { check_session } from "$lib/utils/check_session"
    import { onMount } from "svelte";

	onMount(async () => {
		console.log(await check_session());
	});

</script>

{@render children()}
