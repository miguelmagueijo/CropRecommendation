<script lang="ts">
	import { onMount } from 'svelte';

	let datasets: string[] = [];
	let finished = false;
	let loadFail = false;

	onMount(async () => {
		try {
			const response = await fetch('http://localhost:5000/datasets');

			datasets = (await response.json()).datasets;

			finished = datasets.length > 0;
		} catch (e) {
			finished = true;
			loadFail = true;
		}
	});
</script>

{#if !finished}
	<div class="mx-auto my-60 w-fit">
		<div class="mb-4 text-3xl font-bold">Loading</div>
		<svg
			class="mx-auto h-20 w-20 animate-spin fill-green-500"
			version="1.1"
			xmlns="http://www.w3.org/2000/svg"
			xmlns:xlink="http://www.w3.org/1999/xlink"
			x="0px"
			y="0px"
			width="122.315px"
			height="122.88px"
			viewBox="0 0 122.315 122.88"
			enable-background="new 0 0 122.315 122.88"
			xml:space="preserve"
			><g
				><path
					fill-rule="evenodd"
					clip-rule="evenodd"
					d="M94.754,14.534c8.844,0,16.014,7.17,16.014,16.012 c0,8.844-7.17,16.015-16.014,16.015c-8.843,0-16.013-7.17-16.013-16.015C78.741,21.704,85.911,14.534,94.754,14.534L94.754,14.534z M109.265,52.121c-7.205,0-13.049,5.844-13.049,13.048c0,7.207,5.844,13.049,13.049,13.051c7.207,0,13.051-5.844,13.051-13.051 C122.315,57.965,116.472,52.121,109.265,52.121L109.265,52.121z M94.135,89.903c-5.032,0-9.114,4.082-9.114,9.113 c0,5.032,4.082,9.114,9.114,9.114c5.031,0,9.113-4.082,9.113-9.114C103.248,93.985,99.166,89.903,94.135,89.903L94.135,89.903z M59.275,104.65c-5.032,0-9.114,4.081-9.114,9.113c0,5.034,4.082,9.116,9.114,9.116s9.113-4.082,9.113-9.116 C68.389,108.731,64.308,104.65,59.275,104.65L59.275,104.65z M23.652,90.86c-4.717,0-8.54,3.823-8.54,8.54 c0,4.715,3.823,8.54,8.54,8.54c4.714,0,8.538-3.825,8.538-8.54C32.19,94.684,28.366,90.86,23.652,90.86L23.652,90.86z M9.096,54.872C4.072,54.872,0,58.944,0,63.968c0,5.021,4.072,9.093,9.096,9.093c5.021,0,9.093-4.072,9.093-9.093 C18.189,58.944,14.116,54.872,9.096,54.872L9.096,54.872z M23.652,17.026c-6.354,0-11.508,5.155-11.508,11.509 s5.154,11.506,11.508,11.506s11.506-5.152,11.506-11.506S30.006,17.026,23.652,17.026L23.652,17.026z M59.341,0 c-7.651,0-13.858,6.205-13.858,13.855c0,7.651,6.207,13.856,13.858,13.856s13.856-6.205,13.856-13.856 C73.197,6.205,66.992,0,59.341,0L59.341,0z"
				/></g
			></svg
		>
	</div>
{:else if loadFail}
	<div class="my-60">
		<svg
			class="mx-auto h-20 w-20 fill-orange-500"
			version="1.1"
			xmlns="http://www.w3.org/2000/svg"
			xmlns:xlink="http://www.w3.org/1999/xlink"
			x="0px"
			y="0px"
			viewBox="0 0 122.88 122.88"
			style="enable-background:new 0 0 122.88 122.88"
			xml:space="preserve"
			><style type="text/css">
				.st0 {
					fill-rule: evenodd;
					clip-rule: evenodd;
				}
			</style><g
				><path
					class="st0"
					d="M110.09,6.2l6.58,6.58c8.27,8.27,8.27,21.81,0,30.08L99.24,60.29c-6.52,6.53-16.33,7.89-24.24,4.12 l30.86-30.86c3.05-3.05,3.05-8.03,0-11.07l-5.97-5.97c-3.05-3.05-8.02-3.05-11.07,0L58.15,47.17c-3.37-7.78-1.9-17.2,4.43-23.53 L80.02,6.2C88.29-2.07,101.82-2.07,110.09,6.2L110.09,6.2z M79.93,116.8l6.38-1.32l-4.12-19.89l-6.37,1.34L79.93,116.8L79.93,116.8 L79.93,116.8z M36.38,2.15l6.31-1.56l4.95,19.66l-6.31,1.6L36.38,2.15L36.38,2.15z M102.86,105.79l4.53-4.67L92.82,86.98 l-4.53,4.68L102.86,105.79L102.86,105.79L102.86,105.79z M117.62,84.76l1.68-6.28l-19.6-5.26l-1.69,6.29L117.62,84.76L117.62,84.76 z M2.54,40.47l1.81-6.25l19.5,5.55l-1.77,6.27L2.54,40.47L2.54,40.47z M13.38,17.17l4.61-4.6l14.34,14.35l-4.59,4.61L13.38,17.17 L13.38,17.17L13.38,17.17z M6.2,110.09l6.58,6.58c8.27,8.27,21.8,8.27,30.08,0l17.43-17.43c6.53-6.52,7.89-16.33,4.12-24.24 l-30.86,30.86c-3.05,3.05-8.03,3.05-11.07,0l-5.97-5.97c-3.05-3.05-3.05-8.03,0-11.08l30.67-30.66c-7.79-3.37-17.2-1.9-23.54,4.44 L6.2,80.02C-2.07,88.29-2.07,101.82,6.2,110.09L6.2,110.09L6.2,110.09z"
				/></g
			>
		</svg>
		<div class="mx-auto mt-8 w-fit rounded text-center text-3xl font-bold text-orange-500">
			Could not connect to the API.<br />Try again later.
		</div>
	</div>
{:else}
	<div class="flex items-center justify-center" style="min-height: 50vh;">
		<div>
			<h1 class="text-center text-3xl font-bold text-green-950">Choose dataset</h1>
			<div class="text-center text-lg">
				Each dataset has it's own crops and models!<br />
				Feel free to use the one that suits you better.
			</div>
			<div class="mt-4 flex flex-wrap justify-center gap-4">
				{#each datasets as dName}
					<a
						class="block w-64 rounded border-2 border-green-950 bg-green-500 py-3 text-center text-xl font-bold duration-300 hover:bg-green-800 hover:text-white"
						href="/dataset/{dName}"
					>
						{dName}
					</a>
				{/each}
			</div>
		</div>
	</div>
{/if}
