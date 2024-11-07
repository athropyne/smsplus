import {EVENTS_CHANNEL_URL} from "../../config.js";
import State from "$lib/states/token.svelte.js";

let messageStore = $state("")

export const connect = async (url) => {
    const ws = new WebSocket(url)
    ws.addEventListener("open", (event) => {
        alert("connected")
    })

    ws.addEventListener("close", (event) => {
        alert("disconnected")
    })

    ws.addEventListener("message", (event) => {
        messageStore = event.data
    })
    return ws
}


export default {
    messageStore: messageStore
}
