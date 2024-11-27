import {API_URI} from "../../config.js";

export const enum METHODS {
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    PATCH = "PATCH",
    DELETE = "DELETE"
}

class BaseOptions {
    path: string;
    params: object;
    token: boolean;
    headers: object;
    json: boolean;

    constructor(
        path: string = "/",
        params: object = {},
        token: boolean = true,
        headers: object = {},
        json: boolean = true
    ) {
        this.path = path
        this.params = params
        this.token = token
        this.headers = headers
        this.json = json
    }


}

class Options extends BaseOptions {
    body: any;
    constructor(
        path: string = "/",
        params: object = {},
        token: boolean = true,
        headers: object = {},
        json: boolean = true,
        body: any = null
    ) {
        super(path,
            params,
            token,
            headers,
            json);
        this.body = body
    }

}

export class GetOptions extends BaseOptions {
}

export class PostOptions extends Options {
}

export class PutOptions extends Options {
}

export class PatchOptions extends Options {
}

export class DeleteOptions extends BaseOptions {
}

export class Fisher {
    async fishing(options: Options, method: METHODS) {
        let params: URLSearchParams;
        let params_str: string = ''
        if (options.params) {
            params = new URLSearchParams({...options.params})
            params_str = params.toString()
        }
        let headers: object = {...options.headers}
        if (options.json) {
            headers = {...options.headers, "Content-Type": "application/json"}
        }
        if (options.token) {
            headers = {...options.headers, "Authorization": `Bearer ${API_URI}`}
        }
        let result = await fetch(`${API_URI}${options.path}/${params_str}`, {
            body: method === METHODS.GET ? null : options.body,
            method: method,
            headers: {...headers}
        })
        if (result.ok) return result
        else console.log(result)
    }

    async get(
        options: GetOptions
    ) {
        return await this.fishing(
            new Options(
                options.path,
                options.params,
                options.token,
                options.headers,
                options.json
            ),
            METHODS.GET
        )
    }

    async post(options: PostOptions) {
        return await this.fishing(options, METHODS.POST)
    }

    async put(options: PutOptions) {
        return await this.fishing(options, METHODS.PUT)
    }


    async delete(options: DeleteOptions) {
        return await this.fishing(
            new Options(
                options.path,
                options.params,
                options.token,
                options.headers,
                options.json,
                false
            ),
            METHODS.DELETE
        )
    }

    async patch(options: PatchOptions) {
        return await this.fishing(options, METHODS.PATCH)
    }
}