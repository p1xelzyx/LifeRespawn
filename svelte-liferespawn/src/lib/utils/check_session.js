export const check_session = async () => {
    let res = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({endpoint: "check_session"})
    })
    return await res.json();
};