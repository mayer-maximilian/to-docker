<template>
    <b-container fluid>
        <b-row>
            <b-col cols="9">
                <div v-if="page === 'users'">
                    <users-page></users-page>
                </div>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import axios from 'axios'
import {getCookie} from '@/utils/cookies'
import getEnv from '@/utils/env'

import UsersPage from './components/UsersPage.vue'

export default {
  components: { UsersPage },
    name: 'admin-page',
    created () {
        let jwt_token = getCookie("jwt")
        if (!jwt_token) {
            this.$router.push({'name': 'login'})
            return
        }
        console.log(`${!getEnv('ENV') ? 'http://localhost:5008' : ''}/check-login`);
        axios.get(
            `${!getEnv('ENV') ? 'http://localhost:5008' : ''}/check-login`,
            {'headers': {'Authorization': `bearer ${jwt_token}`}}
        )
        .then((response) => {
            if (response.status === 401) {
                this.$router.push({'name': 'login'})
            }
        })
    },
    data () {
        return {
            page: 'users'
        }
    },
    methods: {
        setPage (page) {
            this.page = page;
        }
    }
}
</script>

<style scoped>
.menu-item {
    margin-bottom: 2rem;
    cursor:pointer;
    text-align: left;
}
</style>