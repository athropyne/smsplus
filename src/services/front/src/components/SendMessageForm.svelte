<script>
    import TextField from "./UI/TextField.svelte";
    import FormButton from "./UI/FormButton.svelte";

    let message = $state()
    let {socket, receiver_id} = $props()
    let message_model = $derived({receiver: receiver_id, text: message})

    $inspect(socket)
    $inspect(message_model)
</script>

<TextField
        placeholder="сообщение"
        oninput={(v) => message = v}
/>
<FormButton
        text=">>>" ,
        action={() => socket.send(JSON.stringify(message_model))}/>