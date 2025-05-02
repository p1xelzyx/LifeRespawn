<script>
    import { logout } from "$utils/logout";
    let { children } = $props();

    let profileShown = $state(false);

</script>

<header>
    <div class="header-top">
        <h1>Life Respawn</h1>

        <div class="profile-container">
            <button class="profile-button" onclick={() => profileShown = !profileShown}>User</button>
            {#if profileShown}
                <ul class="profile-dropdown">
                    <li>Hi</li>
                    <li>Test</li>
                    <li>Log out</li>
                </ul>
            {/if}
        </div>
    </div>
    <div class="line"></div>
    <nav>
        <ul>
            <li>Main</li>
            <li>Nekej</li>
            <li>Bla bla bla</li>
            <li>Test</li>
            <li>Rezultati</li>
            <li>History</li>
            <li>Test test</li>
            <li>hehe</li>
        </ul>
    </nav>
</header>

{@render children()}

<style>
    .header-top {
        display: flex;
        justify-content: space-between;
        padding: 20px 10px;
        align-items: center;
    }
    .line {
        height: 2px;
        background: linear-gradient(90deg, var(--main-color), white);
    }

    nav {
        display: none;
    }
    nav ul {
        list-style-type: none;
    }
    .profile-button {
        color: white;
        font-size: 1.4em;
        border: none;
        background-color: var(--main-color);
        padding: 10px;
        border-radius: 10px;
    }
    .profile-container {
        position: relative;
    }
    .profile-dropdown {
        list-style-type: none;
        position: absolute;
        top: 120%;
    }
    .profile-dropdown {
        background-color: white;
        color: var(--bg-color);
        padding: 10px;
    }
</style>
