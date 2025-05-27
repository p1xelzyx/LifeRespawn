export const load = async ({ params, fetch }) => {

    const response = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({
            endpoint: "get_missions"
        }),
        headers: {
            "content-type": "application/json",
        },
    });

    return await response.json();
};