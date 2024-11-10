<script>
    import "$lib/static/form.css"
    import {signUp} from "./queries.js";

    let login = $state()
    let password = $state()
    let confirm = $state()
    let error_msg = $state()

    async function submit() {
        error_msg = password === confirm ? null : "Пароли не совпадают"
        if (error_msg) return
        error_msg = await signUp(login, password)
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
    <input
            bind:value={confirm}
            placeholder="пароль"
            type="password"
            onclick={onclick}
    />
    <section>
        <div class="form-button">
            <button onclick={submit}>Зарегистрироваться</button>
        </div>
        <a href="/signin">Войти</a>
    </section>
</main>
