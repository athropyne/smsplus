<script>
    let {msg} = $props()
</script>

<div>
    <p>{msg}</p>
</div>

<style>
    p{
        color: red;
    }
    p:before{
        content: "X ";
    }
</style>