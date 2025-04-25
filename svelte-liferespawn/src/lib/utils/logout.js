import { goto } from "$app/navigation";

export async function logout() {
    const response = await fetch('/api/post', {
        method: 'POST',
        body: JSON.stringify({ endpoint: "logout" }),
        headers: {
            'content-type': 'application/json'
        }
    });
    goto('/');
    return await response.json();
}