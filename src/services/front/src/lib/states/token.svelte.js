let token = $state(null)


// @ts-ignore
export default {
    token: token,
    get() {return this.token},
    set(value) { this.token = value}
}