<script>
	import { goto } from "$app/navigation";
	import { logout } from "$utils/logout";

	let username = $state("");
	let password = $state("");

	async function login() {
		const response = await fetch("/api/post", {
			method: "POST",
			body: JSON.stringify({
				endpoint: "login",
				data: { username, password },
			}),
			headers: {
				"content-type": "application/json",
			},
		});

		let data = await response.json();
		if (data?.status === "success") {
			goto("/dashboard");
		}
	}
	async function register() {
		const response = await fetch("/api/post", {
			method: "POST",
			body: JSON.stringify({
				endpoint: "register",
				data: { username, password },
			}),
			headers: {
				"content-type": "application/json",
			},
		});

		console.log(await response.json());
	}
</script>

<div class="wrap">
	<p class="mini">username</p>
	<input class:focused={username} type="text" bind:value={username} />
	<p class="mini">password</p>
	<input class:focused={password} type="password" bind:value={password} />
	<button onclick={login}>login</button>
	<button onclick={register}>register</button>
</div>

<style>
	.wrap {
		display: flex;
		flex-direction: column;
		width: 300px;
		color: white;
		align-items: center;
	}

	input {
		margin-bottom: 10px;
		border: none;
		background-color: transparent;
		outline: 1px solid gray;
		border-radius: 10px;
		padding: 10px;
		color: white;
		width: 100%;
	}
	input:focus,
	.focused {
		outline: 1px solid white;
	}

	p {
		margin-bottom: 5px;
		align-self: flex-start;
		margin-left: 10px;
	}

	.mini {
		color: gray;
		font-size: 0.8em;
	}
	button {
		margin-top: 20px;
		width: 60%;
		color: white;
		background-color: #3a4db4;
		border: 0;
		border-radius: 15px;
		padding: 10px;
		font-size: 1.1em;

		position: relative;
		overflow: hidden;

		transition: box-shadow 0.3s ease;
	}

	button::before {
		content: "";
		position: absolute;
		top: -50%;
		left: -50%;
		width: 200%;
		height: 200%;
		background: linear-gradient(
			0deg,
			transparent,
			transparent 30%,
			rgba(0, 255, 255, 0.3)
		);
		transform: rotate(-45deg);
		transition: all 0.3s ease;
		opacity: 0;
	}

	button:hover::before {
		opacity: 1;
		transform: rotate(-45deg) translateY(150%);
	}

	button:hover {
		box-shadow: 0 0 20px #3a4db4;
	}

	button:active {
		scale: 1.05;
	}
</style>
