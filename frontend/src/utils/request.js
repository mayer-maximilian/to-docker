import axios from 'axios'
import getEnv from '@/utils/env';

let HOST = !getEnv('ENV') ? 'http://localhost:5008' : '';

export function get(path, headers) {
    return axios.get(`${HOST}/${path}`, headers);
}

export async function post(path, data, headers) {
    return axios.post(`${HOST}/${path}`, data, headers);
}