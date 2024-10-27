<script>
    import {token} from "../states/token";
    import {goto} from "$app/navigation";
    import {onMount} from "svelte";
    let go_signin = async () => await goto("signin")

    onMount(async ()=> {
        if(token === null){
            await go_signin()
        }
    })

</script>

