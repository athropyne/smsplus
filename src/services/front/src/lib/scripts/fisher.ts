import {API_URI} from "../../config.js";

export const METHODS = {
    GET: "GET",
    POST: "POST",
    PUT: "PUT",
    PATCH: "PATCH",
    DELETE: "DELETE"
}

export class Fisher {
    API_URI = API_URI

    async dhrow(path: string,
                params: object = {},
                method: string,
                body: any,
                json: boolean,
                token: boolean,
                headers: object) {
        let _params: URLSearchParams;
        let params_str: string = ''
        if (params) {
            _params = new URLSearchParams({...params})
            params_str = _params.toString()
        }
        let _headers: object = {...headers}
        if (json) {
            _headers = {...headers, "Content-Type": "application/json"}
            _headers = {...headers, "Authorization": `Bearer ${API_URI}`}
        }
        let result = await fetch(`${API_URI}/${path}/${params_str}`, {
            body: method === METHODS.GET ? null : body,
            method: method,
            headers: {..._headers}
        })
        if (result.ok) return result
    }

    async get() {

    }

    async post() {

    }

    async put() {

    }


    async delete() {

    }

    async patch() {

    }
}