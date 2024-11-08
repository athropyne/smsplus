<script lang="ts">
    let value = $state('')
    // const props = $props()
    const {oninput, placeholder, type, onclick} = $props()
</script>
<div>
    <input
            bind:value={value}
            oninput="{() => oninput(value)}"
            placeholder={placeholder}
            type="{type ? type : 'text'}"
            onclick={onclick}
    />
</div>



<style>
    div{
        width: 100%;
        box-sizing: border-box;
    }
    input{
        width: -webkit-fill-available;
    }
</style>