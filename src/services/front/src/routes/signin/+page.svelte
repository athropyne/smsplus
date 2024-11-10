<script>
    import "$lib/static/form.css"
    import {signIn} from "./queries.js";

    let login = $state()
    let password = $state()
    let error_msg = $state()

    async function submit() {
        error_msg = await signIn(login, password)
    }
</script>
<main class="form">
    <div class="error-sector">
        {#if (error_msg)}
            <p>{error_msg}</p>
        {/if}
    </div>
    <input
            bind:value={login}
            placeholder="логин"
            onclick={onclick}
    />
    <input
            bind:value={password}
            placeholder="пароль"
            type="password"
            onclick={onclick}
    />
    <section>
        <div class="form-button">
            <button onclick={submit}>Войти</button>
        </div>
        <a href="/signup">Зарегистрироваться</a>
    </section>
</main>
