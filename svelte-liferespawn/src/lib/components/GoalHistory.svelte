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
        if(JSON.stringify(cal[cal.length - 1]) === JSON.stringify([null,null,null,null,null,null,null])) cal.pop();
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
                <div
                    class:hidden={typeof day != "number"}
                    class:today={selectedMonth === originalMonth &&
                        selectedYear === originalYear &&
                        day === todayDate}
                >
                    {(() => {
                        console.log(day === null);
                        return day;
                    })()}
                </div>
            {/each}
        {/each}
    </div>
</div>

<style>
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
    .content div {
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
