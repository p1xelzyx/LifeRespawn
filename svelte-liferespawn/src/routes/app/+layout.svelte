<script>
    import { page } from "$app/state";
    import { logout } from "$utils/logout";
    import { onMount } from "svelte";
    let { children } = $props();

    let profileShown = $state(false);

    function clickOutside(node) {
        const handleOutside = (event) => {
            if (!node.contains(event.target)) {
                profileShown = false;
            }
        };
        document.addEventListener("click", handleOutside, true);
        return {
            destroy() {
                document.removeEventListener("click", handleOutside, true);
            },
        };
    }

    let currentPage = $derived(page.url.pathname.split("/").at(-1));
</script>

<header>
    <div class="header-top">
        <h1>Life Respawn</h1>

        <div class="profile-container" use:clickOutside>
            <button
                class:profile-opened={profileShown}
                class="profile-button"
                onclick={() => (profileShown = !profileShown)}>User</button
            >
            {#if profileShown}
                <ul class="profile-dropdown">
                    <li><button>Profile</button></li>
                    <div class="dropdown-line"></div>
                    <li><button>Other</button></li>
                    <div class="dropdown-line"></div>
                    <li>
                        <button onclick={logout} class="logout-button"
                            >Log out</button
                        >
                    </li>
                </ul>
            {/if}
        </div>
    </div>
    <div class="line"></div>
    <nav>
        <ul>
            <li>
                <button class:nav-button-selected={currentPage === "dashboard"}
                    >DASHBOARD</button
                >
            </li>
            <li><button>NEW ACTIVITY</button></li>
            <li><button>HISTORY</button></li>
            <li><button>CREDITS</button></li>
            <li><button>ABOUT</button></li>
            <li><button>TEST</button></li>
        </ul>
    </nav>
</header>

<div class="middle-page">
    {@render children()}
</div>

<style>
    .middle-page {
        margin: 0px 20px;
    }

    header {
        margin: 30px 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 20px 8px rgba(0, 0, 0, 0.6);
        background-color: rgb(20, 20, 20);
        padding: 20px;
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .line {
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, white, rgba(255, 255, 255, 0));
    }

    nav ul button {
        padding: 10px 20px;
        color: white;
        background-color: rgba(255, 255, 255, 0.05);

        font-size: 1em;
        border: none;
        white-space: pre;
        transition: 0.2s all;
    }
    nav ul button:hover,
    .nav-button-selected {
        background-color: var(--main-color);
        height: 110%;
    }
    nav ul button:hover:not(.nav-button-selected) {
        cursor: pointer;
    }
    nav ul button:active {
        filter: brightness(1.2);
    }
    nav ul {
        display: flex;
        flex-wrap: wrap;
        list-style-type: none;
    }

    .profile-button {
        color: white;
        font-size: 1.1em;
        border: none;
        background-color: var(--main-color);
        padding: 10px;
        border-radius: 10px;
    }

    .profile-button:hover,
    .profile-opened {
        outline: 2px solid white;
    }
    .profile-button:hover {
        cursor: pointer;
    }
    .profile-button:active {
        outline: 3px solid white;
    }

    .profile-container {
        position: relative;
        display: flex;
        justify-content: end;
    }
    .profile-dropdown {
        list-style-type: none;
        position: absolute;
        top: 120%;
        width: 200px;
        padding: 12px;
        color: white;
        background-color: rgb(31, 31, 31);
        box-shadow: 0px 7px 22px 2px rgba(0, 0, 0, 0.75);
        font-size: 1.2em;
        border-radius: 12px;
    }

    .profile-dropdown button:not(.logout-button) {
        font-size: 1em;
        background-color: unset;
        color: white;
    }

    .logout-button {
        color: red;
        font-size: 1em;
        background-color: unset;
        text-align: end;
        width: 100%;
    }

    .profile-dropdown button:hover {
        text-decoration: underline;
        cursor: pointer;
    }

    .dropdown-line {
        margin: 10px 0px;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, white, rgba(255, 255, 255, 0));
    }
</style>
