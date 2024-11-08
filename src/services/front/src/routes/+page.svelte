<script>
    import {goto} from "$app/navigation";
    import {onMount} from "svelte";
    import State from "$lib/states/token.svelte.js"
    import TextField from "../components/UI/TextField.svelte";

    // onMount(async () => {
    //     if (State.token === null) {
    //         await goto("/signin")
    //     } else {
    //         await goto("/chat_screen")
    //     }
    // })
    let value = $state()
    let update = (v) => {value = v}

</script>

<TextField
    placeholder="тест"
    oninput={(v) => value = v}
/>

