import {API_URI} from "../../config.js";

// @ts-ignore
export async function signUp(login, password, confirm) {
    if (password !== confirm) return "пароли не совпадают"
    let result = await fetch(`${API_URI}/users`, {
        method: "POST",
        body: JSON.stringify({
            "login": login,
            "password": password
        }),
        headers: {"Content-Type": "application/json"},

    })
    if (result.status === 201) {
        // await this.signIn(login, password)
        alert("вы зарегистрированы")
    } else {
        let data = await result.json()
        if ("detail" in data) return data["detail"]
    }
}