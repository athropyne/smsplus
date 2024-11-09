<script>
    import SignInForm from "../../components/SignInForm.svelte";
</script>

<!--<script lang="ts">-->
<!--    import {signIn} from "./connectors";-->

<!--    let login: string;-->
<!--    let password: string;-->
<!--    let error_msg: string | null = null-->
<!--    let submit = async () => {-->
<!--        error_msg = await signIn(login, password)-->
<!--    }-->

<!--    let error_reset = () => {-->
<!--        error_msg = null-->
<!--    }-->
<!--</script>-->
<!--<main>-->
<!--    <div id="form">-->
<!--        <header class="errors">-->
<!--            {#if error_msg !== null}-->
<!--                {error_msg}-->
<!--            {/if}-->
<!--        </header>-->
<!--        <div class="input-wrapper">-->
<!--            <input-->
<!--                    onclick={error_reset}-->
<!--                    bind:value={login}-->
<!--                    type="text"-->
<!--                    placeholder="логин">-->
<!--        </div>-->
<!--        <div>-->
<!--            <input-->
<!--                    onclick={error_reset}-->
<!--                    bind:value={password}-->
<!--                    type="password"-->
<!--                    placeholder="пароль">-->
<!--        </div>-->
<!--        <div class="submit-wrapper">-->
<!--            <button onclick={submit}>Войти</button>-->
<!--            <a href="/signup">регистрация</a>-->
<!--        </div>-->

<!--    </div>-->
<!--</main>-->
<SignInForm/>