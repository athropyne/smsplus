<script lang="ts">
    let login: string;
    let password: string;
    let submit = async () => {
        let result = await fetch("http://localhost:8000/security/signin",
            {
                method: "POST",
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: JSON.stringify({
                    login: login,
                    password: password
                },
            )
            })
        console.log(result.status)
        let data = await result.json()
        console.log(data)
    }
</script>
<main>
    <div id="form-header">
        <div class="input-wrapper">
            <input bind:value={login} type="text" placeholder="логин">
        </div>
        <div>
            <input bind:value={password} type="password" placeholder="пароль">
        </div>
        <div class="submit-wrapper">
            <button on:click={submit}>Войти</button>
        </div>
    </div>
</main>
{login}
{password}