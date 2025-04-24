<script>
    import { logout } from "$utils/logout"

    let username = $state("");
    let password = $state("");

    async function login() {
        console.log("try login");
        const response = await fetch('/api/post', {
			method: 'POST',
			body: JSON.stringify({endpoint: "login", data: { username, password }}),
			headers: {
				'content-type': 'application/json'
			}
		});

		console.log(await response.json());
    }
    async function register() {
        console.log("try register");
        const response = await fetch('/api/post', {
			method: 'POST',
			body: JSON.stringify({endpoint: "register", data: { username, password }}),
			headers: {
				'content-type': 'application/json'
			}
		});

		console.log(await response.json());
    }
    async function check_session() {
        console.log("try check session");
        const response = await fetch('/api/post', {
			method: 'POST',
			body: JSON.stringify({endpoint: "check_session"}),
			headers: {
				'content-type': 'application/json'
			}
		});

		console.log(await response.json());
    }


</script>

<p>username</p>
<input type="text" bind:value={username}>
<p>password</p>
<input type="password" bind:value={password}>
<button onclick={login}>login</button>
<button onclick={register}>register</button>
<button onclick={logout}>logout</button>
<button onclick={check_session}>check session</button>
