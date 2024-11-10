import {goto} from "$app/navigation";

let messageStore = $state("")

// @ts-ignore
export const connect = async (url) => {
    const ws = new WebSocket(url)
    ws.addEventListener("open", (event) => {
        alert("connected")
    })

    ws.addEventListener("close", async (event) => {
        alert("disconnected")
        await goto("/signin")
    })


    return ws
}

export default {
    messageStore: messageStore
}

