<script lang="ts">
    import { page } from "$app/stores";
</script>

<div>
    <h1 class="text-6xl font-bold text-center">{$page.status}</h1>
    <div class="text-2xl text-center mt-2">
        {$page.error?.message}
    </div>
    <a class="mt-8 block w-fit mx-auto text-center px-6 py-2 rounded border-2 border-green-950 bg-green-500 text-lg font-bold duration-300 hover:bg-green-800 hover:text-white" href="/">
        Go home
    </a>
</div>