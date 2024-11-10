import {API_URI} from "../../config.js";
import {signIn} from "../signin/queries.js";

export async function signUp(login, password, confirm) {
    let result = await fetch(`${API_URI}/users`, {
        method: "POST",
        body: JSON.stringify({
            "login": login,
            "password": password
        }),
        headers: {"Content-Type": "application/json"},

    })
    if (result.status === 201) {
        alert("вы зарегистрированы")
        await signIn(login, password)
    } else {
        let data = await result.json()
        if ("detail" in data) return data["detail"]
    }
}