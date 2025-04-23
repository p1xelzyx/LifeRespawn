import { json } from '@sveltejs/kit';

export const POST = async ({ request, fetch }) => {
    const { endpoint, data } = await request.json();

    return fetch(`http://127.0.0.1:5000/${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
};