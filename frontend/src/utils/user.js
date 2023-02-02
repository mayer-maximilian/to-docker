import {post} from '@/utils/request'
import jwt_decode from "jwt-decode";

import {eventBus} from '@/main';
import {getCookie, setCookie, deleteCookie} from '@/utils/cookies';

export function print(obj) {
    console.log(obj)
}

export function getUser() {
    let jwt_token = getCookie("jwt")
    if (jwt_token) {
        let decoded_token = jwt_decode(jwt_token)
        return decoded_token.sub
    }
    return false;
}

export async function userLogIn(username, password) {
    let data = new FormData()
    data.append('username', username)
    data.append('password', password)
    let headers = {
        'headers': { "Content-Type": "multipart/form-data" }
    }
    let successful = true
    await post(`authenticate`, data, headers)
        .then((response) => {
            console.log('yay')
            setCookie("jwt", response.data.access_token)
            eventBus.$emit('user-change')
        }).catch((error) => {
            console.log('nay', error)
            successful = false
        })
    return successful
}

export function userLogOff() {
    if (getCookie("jwt")) {
        deleteCookie("jwt")
    }
    eventBus.$emit('user-change')
}
