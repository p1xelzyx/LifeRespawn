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
            endpoint: "check_goals_today"
        }),
        headers: {
            "content-type": "application/json"
        }
    })

    let actions = (await response.json()).actions;
    let analysis = (await response2.json()).analysis;

    
    return { actions, analysis };
    //return { actions, goals };
};