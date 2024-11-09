import {API_URI} from "../../config.js";
import {signIn} from "$lib/queries/security.js";
import {goto} from "$app/navigation";

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
        await signIn(login, password)
        alert("вы зарегистрированы")
    } else {
        let data = await result.json()
        if ("detail" in data) return data["detail"]
    }
}


export const getList = async () => {
    let result = await fetch(`${API_URI}/users`, {
        headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
    })
    if (result.status === 401) {
        localStorage.removeItem("access_token")
        await goto("/signin")
    } else if (!result.ok) {
        let data = await result.json()
        alert(data["detail"])
    }
    return await result.json()
}