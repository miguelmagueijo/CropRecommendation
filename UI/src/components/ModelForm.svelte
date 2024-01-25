<script lang="ts">
    export let id: string;
    export let modelName: string;
    export let features: string[];


    let submitted = false;
    let requestOutput: string = "";
    let requestError = false;
    let outputDiv: HTMLElement;

    async function predictClass(e: Event) {
        outputDiv.classList.remove("hidden");
        outputDiv.classList.remove("bg-lime-400");
        outputDiv.classList.remove("bg-red-400");
        outputDiv.classList.add("bg-neutral-300");
        outputDiv.innerHTML = "<b>Loading...</b>";
        submitted = true;
        requestError = false;

        const TARGET_FORM = e.target as HTMLFormElement;
        const ACTION_URL = TARGET_FORM.action;

        const formData = new FormData(TARGET_FORM)
        const data = new URLSearchParams();

        for (const field of formData) {
            const [key, value] = field;
            data.append(key, String(value));
        }

        const response = await fetch(ACTION_URL, {
            method: "POST",
            body: data
        });

        outputDiv.classList.remove("bg-neutral-300");

        if (response.status != 200) {
            outputDiv.classList.add("bg-red-400");
            requestError = true;
            submitted = false;
            outputDiv.innerHTML = "<b>Error</b>, bad values. Make sure they are all numbers.";
            return;
        }

        
        outputDiv.classList.add("bg-lime-300");
        const PREDICTED_CLASS = (await response.json()).prediction;        
        outputDiv.innerHTML = `Model recommends: <span class="capitalize font-bold">${PREDICTED_CLASS}</span>`;
    }
</script>

<div class="p-4 bg-green-50 rounded border-2 border-green-500">
    <div class="mb-2 text-xl">
        <b>{ modelName }</b>
    </div>
    <form action="http://localhost:5000/predict/{id}" on:submit|preventDefault={predictClass}>
        <div class="grid gap-4 features-grid-columns">
            {#each features as fName }
                <div>
                    <label for="input_{ fName }" class="block font-semibold">
                        { fName }
                    </label>
                    <input class="w-full border-2 border-green-500 px-2 py-1" type="number" id="input_{ fName }" name={ fName } placeholder="0">
                </div>
            {/each}
        </div>
        <div class="text-center mt-4">
            <button class="bg-green-500 hover:bg-green-800 hover:text-white duration-300 px-10 py-1 rounded font-bold text-lg" type="submit">
                Recommend crop
            </button>
        </div>
        <div class="mt-4 text-center py-4 rounded hidden" bind:this={outputDiv}></div>
    </form>
</div>

<style>
    .features-grid-columns {
        grid-template-columns: repeat(auto-fit, minmax(125px, 3fr));
    }
</style>