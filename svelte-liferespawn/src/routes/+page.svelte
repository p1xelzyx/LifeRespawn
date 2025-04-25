<script>
    import { AccountCreationForm, PopUp } from "$components";
</script>

<section class="wrap">
    <div class="welcome">
        <h1>Welcome to Life Respawn</h1>
        <p>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Sunt aut
            voluptatem praesentium delectus autem commodi blanditiis, architecto
            atque libero cum? Eveniet hic in voluptatem similique amet
            necessitatibus officia, voluptates iste illo, quo minus alias, nihil
            ullam sint quis impedit dolorem modi autem labore aliquid ea
            aspernatur fugiat. Cupiditate, minima ad?
        </p>
    </div>

    <div class="center">
        <AccountCreationForm />
    </div>
</section>


<style>
    h1 {
        text-align: center;
        color: var(--main-color);
        font-size: 2em;
        font-weight: 500;
        margin-bottom: 20px;
        font-size: 3em;
    }
    .center {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 50%;
    }
    p {
        color: gray;
    }

    .welcome {
        padding: 50px;
        width: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .wrap {
        height: 100vh;
        display: flex;
        flex-direction: row;
    }
    @media (max-width: 850px) {
        .wrap {
            flex-direction: column;
        }
        .welcome {
            width: 100%;
        }
        .center {
            width: 100%;
        }
    }
</style>
