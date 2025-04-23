export const handleFetch = async ({ event, request, fetch }) => {
    if (request.url.startsWith('http://127.0.0.1:5000/')) {
		request.headers.set('cookie', event.request.headers.get('cookie'));
    }
	return fetch(request);
};