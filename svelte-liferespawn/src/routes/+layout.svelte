<script>
    import "../app.css";


    let { children } = $props();

    import { check_session } from "$utils";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { page } from "$app/state";

	onMount(async () => {
		let data = await check_session();

        if(data?.username) {
            console.log(`Logged in as ${data?.username}`);
            if(page.url.pathname === "/") {
                goto('/dashboard')
            }
        } else {
            console.log("no session, go login");
            goto('/');
        }
	});


</script>

{@render children()}
