<script lang="ts">
    import "../app.css";
</script>

<nav class="mt-4 mb-12 p-4 border-2 rounded border-green-500 flex justify-between items-center">
    <h1 class="font-bold text-2xl text-green-900">
        Crop Recommendation
    </h1>
    <div class="text-sm font-bold text-green-900/40 select-none">
        This is a prototype
    </div>
</nav>

<main class="text-green-950">
    <slot />
</main>

<footer class="mt-12 mb-6 border-2 p-4 rounded border-green-500 text-green-900 flex justify-between gap-4 flex-wrap">
    <div>
        Source code can be found <a class="font-bold underline" href="https://github.com/miguelmagueijo/CropRecommendation" target="_blank">here</a>
    </div>
    <div>
        Icons by <a class="font-bold underline" href="https://uxwing.com" target="_blank">UxWing</a>
    </div>
    <div>
        Developed by <a class="font-bold underline" href="https://www.miguelmagueijo.pt" target="_blank">Miguel Magueijo</a>
    </div>
</footer>