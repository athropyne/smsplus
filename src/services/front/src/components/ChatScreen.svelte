<script>
    import {getHistory} from "$lib/queries/messages.js";
    import Store from "../routes/chat_screen/store.svelte.js";

    let messages = $state([])
    let {interlocutor_id, socket} = $props()
    $effect(async () => {
        if (interlocutor_id) {
            let result = await getHistory(interlocutor_id)
            console.log(result)
            messages = [...messages, ...result]
        }
    })

</script>
<div class="messages">
    {#each messages as message (message.created_at)}
        <p
                class={message.receiver === interlocutor_id ? "received" : "sent" }
        >{message.text}</p>
    {/each}
</div>


<style>
    .messages{
        display: flex;
        flex-direction: column;
    }
    .messages .received{
        text-align: left;
    }
    .messages .sent{
        text-align: right;
    }
</style>
