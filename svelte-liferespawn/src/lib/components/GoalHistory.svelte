<script>
    import {
        ChevronLeftIcon,
        ChevronRightIcon,
        Edit3Icon,
        RefreshCcwIcon,
    } from "svelte-feather-icons";

    let originalYear = new Date().getFullYear();
    let originalMonth = new Date().getMonth();

    let selectedYear = $state(new Date().getFullYear());
    let selectedMonth = $state(new Date().getMonth());

    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    function makeCalendar(year, month) {
        const firstDate = new Date(year, month, 1);
        const lastDate = new Date(year, month + 1, 0);

        let weekDay = firstDate.getDay() - 1;
        if (weekDay === -1) weekDay = 6;

        let cal = [];
        let i = 0; // za časno za vsak slučaj če se pokvar da ni infinite loop

        let row = 0;
        let col = 0;
        let length = lastDate.getDate() - firstDate.getDate();
        let realIndex = 0;

        while (true) {
            let xy = row * 7 + col;

            if (col > 6) {
                row++;
                col = 0;
            }
            if (!Array.isArray(cal[row])) {
                cal[row] = [];
            }

            if (xy >= weekDay && xy <= weekDay + length) {
                cal[row][col] = ++realIndex;
            } else {
                cal[row][col] = null;
            }

            col++;

            if (cal[row][6] === null) {
                break;
            }
            if (i > 70) {
                alert("ERROR DATE GENERATOR");
                break;
            }
            i++;
        }
        if (
            JSON.stringify(cal[cal.length - 1]) ===
            JSON.stringify([null, null, null, null, null, null, null])
        )
            cal.pop();
        return cal;
    }

    let calendar = $derived(makeCalendar(selectedYear, selectedMonth));

    function upMonth() {
        if (selectedMonth >= 11) {
            selectedYear++;
            selectedMonth = 0;
        } else {
            selectedMonth++;
        }
    }
    function downMonth() {
        if (selectedMonth <= 0) {
            selectedYear--;
            selectedMonth = 11;
        } else {
            selectedMonth--;
        }
    }
    let formYear = $state();
    let formActive = $state(false);
    function toggleForm() {
        if (!formActive) {
            formYear = selectedYear;
        }
        formActive = !formActive;
    }
    let todayDate = new Date().getDate();

    async function getGoalHistory(year, month) {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "goal_history",
                data: {
                    year,
                    month,
                },
            }),
        });
        if (response.status === 401) return logout();
        if (!response.ok) return alert("error");

        let data = await response.json();
        if (data.status === "success") {
            return data.history;
        } else {
            alert("problem");
            return {};
        }
    }

    let history = $state({});
    $inspect(history);
    let latestCallId = 0; // tak sistem je potreben ker če spamas te fetche na slabmu internetu se parkrat hitr zloada pa flasha na koledarju tko pa lepo počakas da se sam tazadn shran in pokaže
    $effect(async () => {
        const callId = ++latestCallId;
        history = {};

        const result = await getGoalHistory(selectedYear, selectedMonth);
        if (callId !== latestCallId) {
            return;
        }
        latestCallId = 0;
        history = result;
    });

    function checkGoals(day) {
        if (!history[day]) return [null];

        let arr = [];
        let isGood = null;
        for (let g of history[day]) {
            let correct = g.positive ? g.total >= g.goal : g.total <= g.goal;
            if (correct && isGood === null) {
                isGood = true;
            } else if (!correct) {
                isGood = false;
            }

            let total =
                g.unit == "amount"
                    ? g.total
                    : `${Math.floor(g.total / 60)}h ${g.total % 60}m`;
            let goal =
                g.unit == "amount"
                    ? g.goal
                    : `${Math.floor(g.goal / 60)}h ${g.goal % 60}m`;
            arr.push([
                correct,
                `${g.name} - ${total}/ ${g.positive ? "at least" : "max"} ${goal}`,
            ]);
        }

        return [isGood, arr];
    }
</script>

<!--
    flask nej posle sam vse gole pa action history
    pol sortiramo po dnevih
    
    oz. funkcija check day?

    caki

    - dobimo vse dni v mescu trenutnem  (leto, mesec izbran na tem komponentu)
    - generiramo 
-->

<div class="wrap">
    <div class="top">
        <button onclick={downMonth}><ChevronLeftIcon /></button>
        <div class="edit-wrap">
            <h2>
                <span
                    >{months[selectedMonth]}
                    {selectedYear}</span
                >
                <button onclick={toggleForm}><Edit3Icon size="19" /></button>
            </h2>
            <div class="edit-form" class:no-display={!formActive}>
                <input type="number" min="0" bind:value={formYear} /><button
                    onclick={() => {
                        selectedYear = formYear;
                        formActive = false;
                    }}>Set</button
                >
                <button
                    onclick={() => {
                        selectedMonth = originalMonth;
                        selectedYear = originalYear;
                        formActive = false;
                    }}><RefreshCcwIcon size="19" /></button
                >
            </div>
        </div>
        <button class="nav" onclick={upMonth}><ChevronRightIcon /></button>
    </div>
    <div class="days">
        {#each days as day}
            <div>{day}</div>
        {/each}
    </div>
    <div class="content">
        {#each calendar as week, i}
            {#each week as day}
                {@const info = checkGoals(day)}
                <div
                    class:marked-red={info[0] === false}
                    class:marked-green={info[0] === true}
                    class="calendar-day"
                    class:hidden={typeof day != "number"}
                    class:today={selectedMonth === originalMonth &&
                        selectedYear === originalYear &&
                        day === todayDate}
                >
                    {day}
                    <div class="day-info">
                        {#each info[1] as goal}
                            <p
                                class:bad-goal={!goal[0]}
                                class:good-goal={goal[0]}
                            >
                                {goal[1]}
                            </p>
                        {/each}
                    </div>
                </div>
            {/each}
        {/each}
    </div>
</div>

<style>
    .day-info {
        background-color: black;
        padding: 10px;
        display: none;
        position: absolute;
        border-radius: 10px;
        z-index: 20;
    }

    .calendar-day:hover .day-info {
        display: block;
    }
    .day-info:not(:has(*)) {
        opacity: 0;
    }

    .marked-red {
        background-image: linear-gradient(
            to bottom,
            transparent 70%,
            crimson 70%
        );
    }
    .marked-green {
        background-image: linear-gradient(
            to bottom,
            transparent 70%,
            lightgreen 70%
        );
    }
    .marked-red:hover {
        outline: 2px solid crimson;
    }
    .marked-green:hover {
        outline: 2px solid lightgreen;
    }

    .bad-goal {
        color: crimson;
    }
    .good-goal {
        color: lightgreen;
    }
    .day-info p:not(:last-child) {
        padding-bottom: 10px;
        border-bottom: 2px solid rgb(100, 100, 100);
        margin-bottom: 10px;
    }

    .edit-form {
        font-size: 1.2em;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: rgb(24, 24, 24);
        border: 2px solid var(--main-color-dark);
        padding: 10px;
        border-radius: 10px;
        position: absolute;
        gap: 5px;
    }
    .no-display {
        display: none;
    }

    input {
        background-color: transparent;
        padding: 5px 5px 2px 5px;
        width: 100%;
        color: white;
        font-size: 1em;
        border-bottom: 2px solid rgba(255, 255, 255, 0.555);
        margin-bottom: 10px;
    }

    h2 {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
        flex-wrap: wrap;
    }
    .edit-wrap {
        position: relative;
    }
    button {
        background-color: transparent;
        border: none;
        color: white;
    }

    .edit-form button {
        background-color: var(--main-color-dark);
        font-size: 1.1em;
        width: 100%;
        border-radius: 10px;
        transition: 0.1s all;
    }
    .edit-form button:hover {
        background-color: var(--main-color);
    }

    .top {
        display: flex;
        justify-content: space-between;
        background-color: rgb(36, 36, 36);
        margin-bottom: 20px;
        padding: 5px;
    }
    .wrap {
        width: 100%;
        max-width: 600px;
        border: 2px solid rgb(70, 70, 70);
        padding: 15px;
        border-radius: 10px;
        margin: 0 auto;
    }
    .days div {
        font-size: clamp(0.8rem, 2.5vw, 1.2rem);
        text-align: center;
        margin-bottom: 10px;
    }
    .content,
    .days {
        display: grid;
        grid-template-columns: repeat(7, 1fr); /* 7 equal-width columns */
        gap: 5px;
    }
    .content > div {
        padding: 5px;
        width: 100%;
        border: 1px solid rgb(70, 70, 70);
        border-radius: 5px;
        aspect-ratio: 1;
    }

    .hidden {
        visibility: hidden;
    }

    .today {
        outline: 1px solid white;
    }
</style>
