<script>
    import {signUp} from "$lib/queries/users.js";
    import ErrorSector from "./UI/ErrorSector.svelte";
    import TextField from "./UI/TextField.svelte";
    import FormButton from "./UI/FormButton.svelte";

    let login = $state()
    let password = $state()
    let confirm = $state()
    let error_msg = $state()

    async function submit() {
        error_msg = await signUp(login, password, confirm)
    }
</script>
<main>
    <div class="error-sector">
        {#if (error_msg)}
            <ErrorSector msg="{error_msg}"/>
        {/if}
    </div>
    <div class="text-field">
        <TextField
                placeholder="логин"
                oninput="{(v) => login = v}"
                onclick={()=> error_msg = undefined}
        />
    </div>
    <div class="text-field">
        <TextField
                placeholder="пароль"
                type="password"
                oninput="{(v) => password = v}"
                onclick={()=> error_msg = undefined}
        />
    </div>

        <TextField
                placeholder="пароль еще раз"
                type="password"
                oninput="{(v) => confirm = v}"
                onclick={()=> error_msg = undefined}
        />

    <section>
        <div class="form-button">
            <FormButton
                    text="зарегистрироваться"
                    action={async () => await submit()}
            />
        </div>
        <a href="/signup">войти</a>
    </section>

</main>

<style>
    main{
        display: grid;
        grid-gap: 3px;
        border: 1px solid blue;
        box-sizing: border-box;
    }
    section{
        display: flex;
        justify-content: space-around;
    }
    .text-field{
        width: 100%;
    }
    .form-button{
        display: inline-block;
    }
</style>
