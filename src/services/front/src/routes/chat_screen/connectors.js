import {API_URI} from "../../config.js";
import State from "$lib/states/token.svelte.js";
import {goto} from "$app/navigation";
export const getList = async () => {
    let result = await fetch(`${API_URI}/users`, {
        headers: {"Authorization": `Bearer ${State.token}`}
    })
    if (result.status === 401) {
        State.token = null
        await goto("/signin")
    } else if (!result.ok) {
        let data = await result.json()
        alert(data["detail"])
    }
    return await result.json()
}