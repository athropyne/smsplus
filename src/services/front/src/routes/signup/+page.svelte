<script lang="ts">
    import {signUp} from "./connectors";

    let login: string = $state("")
    let password: string = $state("")
    let confirm: string = $state("")
    let error_msg: string | null = $state(null)
    let submit = async () => {
        error_msg = await signUp(login, password, confirm)
    }
    let error_reset = () => {
        error_msg = null
    }
</script>
<main>
    <div id="form">
        <header class="errors">
            {#if error_msg !== null}
                {error_msg}
            {/if}
        </header>
        <div class="input-wrapper">
            <input
                    on:click={error_reset}
                    bind:value={login}
                    type="text"
                    placeholder="логин"
                    maxlength="30">
        </div>
        <div>
            <input
                    on:click={error_reset}
                    bind:value={password}
                    type="password"
                    placeholder="пароль"
                    maxlength="100">
        </div>
        <div>
            <input
                    on:click={error_reset}
                    bind:value={confirm}
                    type="password"
                    placeholder="пароль"
                    maxlength="100">
        </div>
        <div class="submit-wrapper">
            <button on:click={submit}>Регистрация</button>
            <a href="/signin">войти</a>
        </div>
    </div>
</main>