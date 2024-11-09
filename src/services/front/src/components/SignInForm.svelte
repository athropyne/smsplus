<script>
    import {signUp} from "$lib/queries/users.js";
    import ErrorSector from "./UI/ErrorSector.svelte";
    import TextField from "./UI/TextField.svelte";
    import FormButton from "./UI/FormButton.svelte";
    import "./form.css"
    import {signIn} from "$lib/queries/security.js";

    let login = $state()
    let password = $state()
    let error_msg = $state()

    async function submit() {
        error_msg = await signIn(login, password, confirm)
    }
</script>
<main class="form">
    <div class="error-sector">
        {#if (error_msg)}
            <ErrorSector msg="{error_msg}"/>
        {/if}
    </div>
    <TextField
            placeholder="логин"
            oninput={(v) => login = v}
            onclick={()=> error_msg = undefined}
    />
    <TextField
            placeholder="пароль"
            type="password"
            oninput="{(v) => password = v}"
            onclick={()=> error_msg = undefined}
    />
    <section>
        <div class="form-button">
            <FormButton
                    text="Войти"
                    action={async () => await submit()}
            />
        </div>
        <a href="/signup">Зарегистрироваться</a>
    </section>
</main>
<style>

</style>

