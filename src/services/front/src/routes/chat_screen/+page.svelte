<script>
    import {API_URI, EVENTS_CHANNEL_URL} from "../../config.js";
    // import {connect} from "./store.svelte.js";
    import {getMessageHistory, getUserList} from "./queries.js";
    import {sendMessage} from "$lib/queries/messages.js";
    import {onDestroy, onMount} from "svelte";
    import {Fisher, GetOptions} from "$lib/scripts/fisher.ts";
    import {goto} from "$app/navigation";
    import '../../app.css'

    let ws = $state()
    let user_list = $state([])
    let selected_user = $state(null)
    let messages = $state([])
    let msg = $state(null)

    onMount(async () => {
        if (ws) ws.close()
        let socket = new WebSocket(`${EVENTS_CHANNEL_URL}`)
        socket.onopen = () => {
            alert("connected")
            console.log(localStorage.getItem("access_token"))
            socket.send(localStorage.getItem("access_token"))
        }
        socket.onmessage = async (event) => {
            let data = JSON.parse(event.data)
            console.log(data)
            if (data.type === "signal") {
                switch (data.data) {
                    case "disconnected" :
                        await goto("/signin");
                        break;
                    case "authorized":
                        alert("Authorized");
                        break;
                    default:
                        alert(data.data)

                }
            } else {
                messages.push(data.data)
                let heigth = document.body.scrollHeight
                window.scroll(0, heigth)
            }

        }
        socket.onclose = (event) => {
            alert("disconected")
        }
        ws = socket
        let result = await new Fisher().get(new GetOptions("/users"))
        if (result.ok) {
            user_list = await result.json()
        }
    });
    $inspect(selected_user)
    $inspect(messages)
</script>

<main>
    <div class="col col-1">
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
                        {user.id} {user.login}
                    </li>
                {/each}
            </ul>
        </div>
    </div>
    <div class="col col-2">
        <div class="messages_screen">
            {#each messages as message (message["created_at"])}
                <p
                        class={message.receiver === selected_user ? "align_right" : "align_left"}
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
    </div>
</main>

<style>
    main {
        height: 100vh;
        background-color: lightblue;
        display: flex;
        gap: 10px;
    }

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

    .col-1 {
        width: 20%;
    }

    .col-2 {
        width: 80%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .messages_screen {
        overflow-y: scroll;
        padding-right: 10px;
    }

    .send_message_form {
        display: flex;
        height: 2.7em;
    }

    .send_message_form input {
        width: 100%;
    }
</style>