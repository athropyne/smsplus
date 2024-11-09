<script lang="ts">
    const {text, action} = $props()
</script>

<button onclick="{action}">{text}</button>

<style>
    button{
        height: 40px;
        border-radius: 5px;
        width: 100%;
    }
</style>

