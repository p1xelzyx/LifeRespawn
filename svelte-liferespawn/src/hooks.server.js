export const handleFetch = async ({ event, request, fetch }) => {
	console.log("HELLO")
    if (request.url.startsWith('http://127.0.0.1:5000/')) {
		request.headers.set('cookie', event.request.headers.get('cookie'));
        console.log(event.request.headers.get("cookie"));
    }
	return fetch(request);
};