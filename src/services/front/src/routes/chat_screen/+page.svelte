<script>
    import {API_URI, EVENTS_CHANNEL_URL} from "../../config.js";
    // import {connect} from "./store.svelte.js";
    import {getMessageHistory, getUserList} from "./queries.js";
    import {sendMessage} from "$lib/queries/messages.js";
    import {onDestroy, onMount} from "svelte";

    let ws = $state()
    let user_list = $state([])
    let selected_user = $state(null)
    let messages = $state([])
    let msg = $state(null)

    // @ts-ignore
    // $effect(async () => {
    //     ws = connect(`${EVENTS_CHANNEL_URL}`)
    //     ws.addEventListener("message", (event) => {
    //         console.log(event.data)
    //         messages.push(event.data)
    //     })
    //     // user_list = await getUserList([])
    //
    // })

    onMount(async () => {
        // if (ws) ws.close()
        let socket = new WebSocket(`${EVENTS_CHANNEL_URL}`)
        socket.onopen = () => {
            alert("connected")
            socket.send(localStorage.getItem("access_token"))
        }
        socket.onmessage = (event) => {
            messages.push(event.data)
        }
        socket.onclose = (event) => {
            alert("disconected")
        }
        ws = socket
        let result = await fetch(`${API_URI}/users/`, {
            headers: {"Authorization": `Bearer ${localStorage.getItem("access_token")}`}
            }
        )
        if (result.ok){
            user_list = await result.json()
        }
    });
    $inspect(selected_user)
</script>

<main>
    <div class="user_list_wrapper">
        <ul>
            {#each user_list as user (user.id)}
                <li
                        class={user.id === selected_user ? "selected_class" : ""}
                        onclick={
                            async () => {
                                selected_user = user.id
                                messages = await getMessageHistory(user.id)
                            }
                        }>
                    {user.login}
                </li>
            {/each}
        </ul>
    </div>
    <div class="messages_screen">
        {#each messages as message (message.created_at)}
            <p
                    class={message.receiver === selected_user ? "align_left" : "align_right"}
            >{message.text}</p>
        {/each}
    </div>
    <div class="send_message_form">
        <input
                bind:value={msg}
                type="text"
                placeholder="сообщение"
        >
        <button
                onclick={
                    async () => {
                        let last_message = await sendMessage(selected_user, msg)
                        if(last_message) messages.push(last_message)
                    }
                }
        > >>>
        </button>
    </div>
</main>

<style>
    li {
        list-style-type: none;
    }

    .selected_class {
        list-style-type: circle;
        color: red;
    }

    .align_left {
        text-align: left;
    }

    .align_right {
        text-align: right;
    }
</style>