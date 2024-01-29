import { error } from '@sveltejs/kit';
import { API_BASE_URL } from '$lib';

export const load = async ({ params }) => {
    const DATASET_NAME = params.slug;
    
    const res = await fetch(`${API_BASE_URL}/datasets`);
    const apiDatasets = (await res.json()).datasets;

    if (apiDatasets.includes(DATASET_NAME)) {
        return {
            page_dataset: DATASET_NAME
        };
    }

	error(404, "Not found");
};