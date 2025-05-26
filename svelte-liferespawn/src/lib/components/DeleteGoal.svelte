<script>
    import { invalidateAll } from "$app/navigation";
    import { Window } from "$components";
    import { logout } from "$utils/logout";
    let window = $state();

    let currentGoalId = $state(-1);

    export function show(goal_id) {
        window.show();
        currentGoalId = goal_id;
    }

    async function deleteGoalById(id) {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "delete_goal",
                data: {
                    goal_id: id,
                },
            }),
        });
        if (response.status === 401) return logout();
        if (!response.ok) return alert("error");

        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
            window.hide();

        }
    }
</script>

<Window bind:this={window}>
    <h1>Are you sure?</h1>
    <div class="end-buttons">
        <button class="window-end-button" onclick={() => window.hide()}>Cancel</button>
        <button class="window-end-button delete" onclick={() => deleteGoalById(currentGoalId)}>Delete</button>
    </div>
</Window>

<style>
    h1 {
        text-align: center;
        margin-bottom: 30px;
    }

    .window-end-button {
        margin: 20px;
    }

    .end-buttons {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
    }

    .delete {
        border: 2px solid red;
        color: red;
    }
    .delete:hover {
        color: white;
        background-color: red;
    }
</style>

