export const load = async ({ params, fetch }) => {

    const response = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({
            endpoint: "get_actions"
        }),
        headers: {
            "content-type": "application/json",
        },
    });

    const response2 = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({
            endpoint: "get_goals"
        }),
        headers: {
            "content-type": "application/json"
        }
    })

    let actions = (await response.json()).actions;
    let goals = (await response2.json()).goals;
    return { actions, goals };
};