import { error } from '@sveltejs/kit';

export const load = async ({ params }) => {
    const DATASET_NAME = params.slug;
    
    const res = await fetch("http://localhost:5000/datasets");
    const apiDatasets = (await res.json()).datasets;

    if (apiDatasets.includes(DATASET_NAME)) {
        return {
            page_dataset: DATASET_NAME
        };
    }

	error(404, "Not found");
};