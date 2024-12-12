<script>
    import {EVENTS_CHANNEL_URL} from "../../config.js";
    import {getMessageHistory} from "./queries.js";
    import {sendMessage} from "$lib/queries/messages.js";
    import {onMount} from "svelte";
    import {Fisher, GetOptions} from "$lib/scripts/fisher.ts";
    import {goto} from "$app/navigation";
    import '../../app.css'

    let ws = $state()
    let user_list = $state([])
    let selected_user = $state(null)
    let messages = $state([])
    let msg = $state(null)

    onMount(async () => {
        // if (ws) ws.close()
        let socket = new WebSocket(`${EVENTS_CHANNEL_URL}`)
        socket.onopen = () => {
            console.log("connected")
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
                        console.log("Authorized");
                        break;
                    default:
                        console.log(data.data)

                }
            } else {
                messages.push(data.data)
                let height = document.body.scrollHeight
                window.scroll(0, height)
            }

        }
        socket.onclose = (event) => {
            console.log("disconected")
        }
        ws = socket
        let result = await new Fisher().get(new GetOptions("/users"))
        if (result.ok) {
            user_list = await result.json()
        }
    });
</script>

<main>
    <div class="col col-1">
        <div class="user_list_wrapper">
            <ul class="user_list">
                {#each user_list as user (user.id)}
                    <li
                            class='user_login {user.id === selected_user ? "selected_user" : ""}'
                            onclick={
                            async () => {
                                selected_user = user.id
                                messages = await getMessageHistory(user.id)
                            }
                        }>{user.login}
                    </li>
                {/each}
            </ul>
        </div>
    </div>
    <div class="col col-2">
        <div class="messages_screen">
            {#each messages as message (message["created_at"])}
                <div class='message-block {message.receiver === selected_user ? "align_right" : "align_left"}'>
                    <p
                            class='message_text'
                    >{message.text}
                    </p>
                </div>
            {/each}
        </div>
        {#if selected_user}
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
                        msg = null
                    }
                }
                > >>>
                </button>
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        height: 100vh;
        background-color: lightblue;
        display: flex;
        gap: 10px;
    }

    .col-1 {
        width: 20%;
        min-width: 10em;
    }

    .col-2 {
        width: 80%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .user_list_wrapper .user_list {
        display: flex;
        flex-direction: column;
        gap: 3px;
        background-color: #f5c5f3;
        height: 100vh;
    }

    .user_list {
        padding-left: 0;
    }

    .user_login {
        list-style-type: none;
        background-color: #aae6d4;
        height: 2em;
        font-size: 20px;
        padding-left: 1em;
        display: flex;
        flex-wrap: wrap;
        align-content: center;
        word-wrap: break-word;
    }

    .user_login:hover {
        background-color: #3feab6;
        padding-left: 1.2em;
    }

    .user_login:active {
        background-color: #ff4e10;
        padding-left: 1.3em;
        box-shadow: goldenrod 0 0 5px;
    }

    .selected_user {
        color: #ffff33;
    }

    .messages_screen {
        display: flex;
        flex-direction: column;
        gap: 1em;
        overflow-y: scroll;
        padding: 1em 1em 4em;
    }

    .message-block {
    }

    .align_right {
        text-align: right;
    }

    .align_left {
        text-align: left;
    }

    .align_right .message_text {
        margin-right: 1em;
        background-color: darkorange;
        border-bottom-right-radius: 0;
    }

    .align_left .message_text {
        margin-left: 1em;
        background-color: darkturquoise;
        border-bottom-left-radius: 0;
    }

    .message_text {
        display: inline-block;
        margin: 0;
        padding: 0.5em;
        border-radius: 10px;
        max-width: 70%;
        word-wrap: break-word;
    }

    .send_message_form {
        display: flex;
        height: 2.7em;
        position: fixed;
        bottom: 3px;
        width: inherit;
    }

    .send_message_form input {
        width: 85%;
        height: 2em;
        font-size: 1.2em;
    }

    .send_message_form button {
        width: 15%;
    }

</style>