import {API_URI} from "../../config.js";
import {goto} from "$app/navigation";

// @ts-ignore
export const signIn = async(login, password) => {
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
        localStorage.setItem("access_token",data["access_token"])
        localStorage.setItem("refresh_token",data["refresh_token"])
        await goto("/chat_screen")
    } else if (result.status === 400) {
        return "неверный логин или пароль"
    } else {
        let data = await result.json()
        if ("detail" in data) return data["detail"]
    }
}