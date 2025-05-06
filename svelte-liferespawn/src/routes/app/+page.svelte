<script>
    import { goto } from "$app/navigation";
    import { page } from "$app/state";
    import { onMount } from "svelte";

    
    onMount(() => {
        goto(page.url.pathname + "/dashboard");
    })
</script>