import {API_URI} from "../config.js";
import {TokenSvelte} from "$lib/states/token.svelte";
import {goto} from "$app/navigation";

export class UserConnector {


    async signIn(login, password) {
        const params = new URLSearchParams()
        params.append("username", login)
        params.append("password", password)
        let result = await fetch(`${API_URI}/security/sign_in`, {
            method: "POST",
            body: params,
            headers: {"Content-Type": "application/x-www-form-urlencoded"}
        })

        if (result.status === 200) {
            let data = await result.json()
            TokenSvelte.value = data["access_token"]
            await goto("/chat_screen")
        } else if (result.status === 400) {
            return "неверный логин или пароль"
        } else {
            let data = await result.json()
            if ("detail" in data) return data["detail"]
        }
    }

    async getList() {
        let result = await fetch(`${API_URI}/users`, {
            headers: {"Authorization": `Bearer ${TokenSvelte.value}`}
        })
        if (result.status === 401) {
            // @ts-ignore
            TokenSvelte.value = null
            await goto("/signin")
        } else if (!result.ok) {
            let data = await result.json()
            alert(data["detail"])
        }
        return await result.json()
    }
}

// export class MessageConnector {
