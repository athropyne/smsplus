<script>
    import {EVENTS_CHANNEL_URL} from "../../config.js";
    import {connect} from "./store.svelte.js";
    import {getList} from "$lib/queries/users.js";
    import UserList from "../../components/UserList.svelte";
    import ChatScreen from "../../components/ChatScreen.svelte";
    import SendMessageForm from "../../components/SendMessageForm.svelte";


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
    let selected_user = $state(null)

    $effect(async () => {
        ws = await connect(`${EVENTS_CHANNEL_URL}/${localStorage.getItem("access_token")}`)
    })

</script>

<main>
    <div class="user_list_wrapper">
        <UserList onselect={(v)=> selected_user = v}/>
    </div>
    <div class="messages_screen">
        <ChatScreen interlocutor_id={selected_user}
        socket={ws}/>
    </div>
    <div class="send_message_form">
        <SendMessageForm socket={ws}
        receiver_id={selected_user}/>
    </div>
</main>