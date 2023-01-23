<template>
    <b-container fluid>

        <!-- <b-alert show variant="danger" >Default Alert</b-alert> -->

        <b-row class="justify-content-md-center">
            <b-col md="4" class="shadow p-3 mb-5 bg-white rounded">
                <h3>Login</h3>
                <b-form-group id="username" label="Username"  label-for="username-input" required>
                    <b-form-input id="username-input" v-model="form.username" trim></b-form-input>
                </b-form-group>
                <b-form-group id="password" label="Password" label-for="password-input" required>
                    <b-form-input id="password-input" v-model="form.password" type="password"></b-form-input>
                </b-form-group>
                <b-button variant="primary" @click="onSubmit" :disabled="!validInput">Log In</b-button>
            </b-col>
        </b-row>

        <b-alert 
            :show="failed_login" 
            dismissible 
            variant="danger"
            @dismissed="failed_login=0"
            @dismiss-count-down="failedLoginUpdate"
        >
            Wrong Credentials
        </b-alert>

    </b-container>
</template>

<script>
import {userLogIn} from '@/utils/user';

export default {
    name: 'Login',
    data() {
        return {
            form: {
                username: null,
                password: null
            },
            failed_login: 0,
            failed_login_max: 3
        }
    },
    computed: {
        validInput () {
            return !!(this.form.username && this.form.password);
        }
    },
    methods: {
        async onSubmit() {
            let successful = await userLogIn(this.form.username, this.form.password)
            console.log('successful', successful)
            if (successful) {
                await this.$router.push({name: 'home'})
            } else {
                this.failed_login = this.failed_login_max
            }
        },
        failedLoginUpdate(failed_login) {
            this.failed_login = failed_login
        }
    }
}
</script>
