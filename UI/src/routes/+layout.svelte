<script lang="ts">
	import '../app.css';
</script>

<div class="h-screen flex flex-col justify-between py-4">
	<nav class="mb-4 flex items-center justify-center sm:justify-between flex-wrap gap-2 rounded border-2 border-green-500 p-4">
		<a class="flex items-center gap-2" href="/">
			<svg class="h-8 w-8" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 114.86"
				><defs
					><style>
						.cls-1 {
							fill: #01a437;
						}
					</style></defs
				><title>leaves</title><path
					class="cls-1"
					d="M59.07,110.77C110.92,105,139.6,71.12,112.44,0c-21.29,14.9-50.39,24.6-65,44.55C57,52.94,64.89,62.23,67.08,74.37c13.19-16.08,27.63-30.72,35.23-47-7.79,39.07-20,53.84-38.78,73.81a93.64,93.64,0,0,1-4.46,9.62Zm-14.9,4C4,105-15.18,76.09,14.27,24.75c23.8,22.92,65.79,37.48,38.39,85.86a27.08,27.08,0,0,1-1.83,2.93C45.9,89.62,26.21,70.69,20.43,50.61,21.77,83.42,31.23,93,45.88,114.86c-.57,0-1.14-.06-1.71-.13Z"
				/>
			</svg>
			<h1 class="text-2xl font-bold text-green-900">Crops Recommendation</h1>
		</a>
		<div class="select-none text-sm font-bold text-green-900/40">This is a prototype</div>
	</nav>
	
	<main class="text-green-950 mb-auto">
		<slot />
	</main>
	
	<footer
		class="mt-12 flex flex-wrap justify-between gap-4 rounded border-2 border-green-500 p-4 text-green-900"
	>
		<div>
			Source code can be found <a
				class="font-bold underline"
				href="https://github.com/miguelmagueijo/CropRecommendation"
				target="_blank">here</a
			>
		</div>
		<div>
			Icons by <a class="font-bold underline" href="https://uxwing.com" target="_blank">UxWing</a>
		</div>
		<div>
			Developed by <a class="font-bold underline" href="https://www.miguelmagueijo.pt" target="_blank">Miguel Magueijo</a>
		</div>
	</footer>
</div>
