import {API_URI} from "../../config.js";
import {goto} from "$app/navigation";

// @ts-ignore
export async function getHistory(interlocutor_id) {
    let result = await fetch(`${API_URI}/messages/?interlocutor_id=${interlocutor_id}`, {
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


// @ts-ignore
export async function sendMessage(receiver_id, message){
    let result = await fetch(`${API_URI}/messages/${receiver_id}`, {
        headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`},
        method: "POST",
        body: JSON.stringify({text: message})
    })
    if (result.status === 401) await goto("/signin")
    else if (!result.ok) {
        let data = await result.json()
        console.log(data)
        alert(data["detail"])
    }
    return await result.json()
}