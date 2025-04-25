export const check_session = async (customFetch) => {
    customFetch = customFetch ?? fetch
    let res = await customFetch("/api/post", {
        method: "POST",
        body: JSON.stringify({endpoint: "check_session"})
    });
    return await res.json();
};