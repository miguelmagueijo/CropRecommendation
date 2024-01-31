import { dev  } from "$app/environment";

export interface FeaturesMetadataJSON {
    [feature_name: string]: {
        type: string,
        min: number, 
        max: number,
        full_name: string,
        help: string,
        unit: string,
    }
}

export const API_BASE_URL = dev ? "http://localhost:5000" : "https://api.cr.miguelmagueijo.pt/est/p1"