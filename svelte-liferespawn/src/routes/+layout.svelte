<script>
    import "../app.css";

    import { setContext } from "svelte";
    import { page } from "$app/state";
    import { redirect } from "@sveltejs/kit";

    let { children, data } = $props();


    if(data?.username) {
        setContext('username', data.username);

        if(page.url.pathname === "/") {
            redirect(303, "/app");
        }
    } else if(page.url.pathname !== "/") {
        redirect(303, "/");
    }



</script>

{@render children()}
