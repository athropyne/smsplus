<script lang="ts">
    let value = $state('')
    const {oninput, placeholder, type, onclick} = $props()
</script>
    <input
            bind:value={value}
            oninput="{() => oninput(value)}"
            placeholder={placeholder}
            type="{type ? type : 'text'}"
            onclick={onclick}
    />



<style>
    input{
        height: 2em;
        box-sizing: border-box;
        width: 100%;
        font-size: 24px;
        border-width: 0 0 1px 0;
    }
</style>