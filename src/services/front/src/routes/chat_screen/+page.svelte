<script>
    import {EVENTS_CHANNEL_URL} from "../../config.js";
    import {connect} from "./store.svelte.js";
    import {getMessageHistory, getUserList} from "./queries.js";
    import {sendMessage} from "$lib/queries/messages.js";

    let ws = $state()
    let user_list = $state([])
    let selected_user = $state(null)
    let messages = $state([])
    let msg = $state(null)

    // @ts-ignore
    $effect(async () => {
        ws = await connect(`${EVENTS_CHANNEL_URL}/${localStorage.getItem("access_token")}`)
        ws.addEventListener("message", (event) => {
            console.log(event.data)
            messages.push(event.data)
        })
        user_list = await getUserList([])
    })

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
                        let last_message = await sendMessage(selected_user)
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