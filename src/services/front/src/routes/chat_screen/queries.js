import {goto} from "$app/navigation";
import {API_URI} from "../../config.js";
import {Fisher, GetOptions} from "$lib/scripts/fisher.ts";

export const getUserList = async () => {
    // let result = await fetch(`${API_URI}/users`, {
    //     headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
    // })
    // if (result.status === 401) {
    //     localStorage.removeItem("access_token")
    //     await goto("/signin")
    // } else if (!result.ok) {
    //     let data = await result.json()
    //     alert(data["detail"])
    // }
    // return await result.json()
    let result = new Fisher().get(new GetOptions(
        "/users"
    ))
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