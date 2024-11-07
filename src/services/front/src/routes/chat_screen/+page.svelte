<script>
    import {EVENTS_CHANNEL_URL} from "../../config.js";
    import {connect} from "./store.svelte.js";
    import State from "$lib/states/token.svelte.js";
    import {getList} from "./connectors.js";


    // const { data, status, ws, close, open, send } = websocket(`${EVENTS_CHANNEL_URL}/${TokenSvelte}`, {
    //     onConnected: () => console.log("connected"),
    //     onDisconnected: () => console.log("disconnected"),
    //     onError: (e) => console.log(e),
    //     onMessage: (data) => console.log(data),
    //     immediate: true,
    //     autoClose: true,
    //     protocols: [],
    //     heartbeat: true,
    //     // autoReconnect: true,
    // })

    let ws = $state()
    let user_list = $state([])

    $effect(async () => {
        ws = await connect(`${EVENTS_CHANNEL_URL}/${State.token}`)
        user_list = await getList()
    })

</script>

<main>
    <div class="user_list_wrapper">
        <ul>
            {#each user_list as user (user.id)}
                <li>{user.login}</li>
            {/each}
        </ul>
    </div>
    <div class="messages_screen">

    </div>
    <div class="send_message_form">

    </div>
</main>