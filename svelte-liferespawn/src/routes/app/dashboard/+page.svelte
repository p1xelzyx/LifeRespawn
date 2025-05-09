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

<section class="app-section section-2">
    <button> Finish your day </button>
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
        flex-wrap: wrap;
    }
    /*@media only screen and (max-width: 1000px) {
        .section-1 {
            flex-direction: column;
        }
        .log-buttons {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }
    }*/
    .log-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-left: auto;
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

    .section-2 {
        padding: 40px;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }

    .section-2 button {
        padding: 30px;
        font-size: 1.5em;
        background-color: var(--main-color);
        color: white;
        border-radius: 20px;
    }
</style>
