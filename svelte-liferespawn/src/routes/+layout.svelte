<script>
    import "../app.css";


    let { children } = $props();

    import { check_session } from "$utils";
    import { onMount } from "svelte";

	onMount(async () => {
		let data = await check_session();

        if(data?.username) {
            console.log(`Logged in as ${data?.username}`);
        } else {
            console.log("no session, go login");
        }
	});


</script>

{@render children()}
