import {goto} from "$app/navigation";
import {API_URI} from "../../config.js";

export const getUserList = async () => {
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


export const getMessageHistory = async (receiver_id) => {
    let result = await fetch(`${API_URI}/messages/?interlocutor_id=${receiver_id}`, {
        headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
    })
    if (result.status === 401) await goto("/signin")
    else if (!result.ok) {
        let data = await result.json()
        console.log(data)
        alert(data["detail"])
    }
    return await result.json()
}