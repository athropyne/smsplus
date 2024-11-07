<script>
    import {goto} from "$app/navigation";
    import {onMount} from "svelte";
    import State from "$lib/states/token.svelte.js"

    onMount(async () => {
        if (State.token === null) {
            await goto("/signin")
        } else {
            await goto("/chat_screen")
        }
    })

</script>

