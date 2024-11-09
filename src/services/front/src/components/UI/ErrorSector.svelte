<script>
    let {msg} = $props()
</script>

<div>
    <p>{msg}</p>
</div>

<style>
    p{
        color: red;
        margin: 5px;
        text-align: center;
        font-size: 12px;
    }
    p:before{
        content: "[X] ";
    }
</style>