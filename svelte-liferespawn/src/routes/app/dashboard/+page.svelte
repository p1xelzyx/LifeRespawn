<script></script>

<section class="app-section section-1">
    <div class="log-info">
        <p>Write down how you feel right now, or what you just did.</p>
        <p>You can always log your actions at the end of the day down below.</p>
    </div>
    <div class="log-buttons">
        <button>Log mood</button>
        <button>Log action</button>
    </div>
</section>

<style>
    .log-info p {
        font-size: 1.1em;
        margin-bottom: 15px;
    }
    .section-1 {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .log-buttons button {
        margin: 40px;
        font-size: 1.3em;
        color: white;
        width: 150px;
        height: 150px;
        padding: 30px;
        background-color: var(--main-color);
        border-radius: 50%;
        box-shadow: 0px 8px 0px 0px rgba(82, 100, 202, 0.6);
        transition: all 0.1s;
    }
    .log-buttons button:hover {
        box-shadow: 0px 5px 0px 0px rgba(82, 100, 202, 0.6);
        transform: translateY(3px);
    }
    .log-buttons button:active {
        box-shadow: 0px 3px 0px 0px rgba(82, 100, 202, 0.6);
        transform: translateY(5px);
    }
</style>
