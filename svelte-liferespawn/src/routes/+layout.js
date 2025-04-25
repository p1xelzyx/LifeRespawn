import { page } from "$app/state";
import { check_session } from "$utils";
import { redirect } from "@sveltejs/kit";

export async function load({ fetch }) {
    let data = await check_session(fetch);
    return data;

    

}