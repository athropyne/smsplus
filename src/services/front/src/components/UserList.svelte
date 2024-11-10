<script>
    import {getList} from "$lib/queries/users.js";
    import Store from "$lib/store.svelte.js"

    const {onselect} = $props()
    let selected_user = $state()
    const select_user = (id) => {
        Store.SELECTED_USER = id
        onselect(id)
    }

    $effect(async () => {
        Store.USER_LIST = await getList()
    })
    $inspect(Store.USER_LIST)
</script>

<ul>
    {#each Store.USER_LIST as user (user.id)}
        <li
                onclick={() => select_user(user.id)}
                class={selected_user === user.id ? "selected-user" : ""}
        >
            {user.login}
        </li>
    {/each}
</ul>

<style>
    li{
        list-style: none;
    }
    .selected-user {
        color: red;
        list-style: circle;
    }
</style>