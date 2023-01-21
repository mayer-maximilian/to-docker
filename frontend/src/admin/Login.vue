<template>
    <b-container fluid>
        <b-alert :show="failed_login" >Default Alert</b-alert>
        <b-alert show variant="danger" >Default Alert</b-alert>
        <b-row class="justify-content-md-center">
            <b-col md="4" class="shadow p-3 mb-5 bg-white rounded">
                <b-form-group id="username" label="Username"  label-for="username-input" required>
                    <b-form-input id="username-input" v-model="form.username" trim></b-form-input>
                </b-form-group>
                <b-form-group id="password" label="Password" label-for="password-input" required>
                    <b-form-input id="password-input" v-model="form.password" type="password"></b-form-input>
                </b-form-group>
                <b-button variant="primary" @click="onSubmit" :disabled="!validInput">log in</b-button>
                <div style="color:red; margin-top:1rem;">
                    *Invalid credentials
                </div>
            </b-col>
        </b-row>
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
            failed_login: false
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
                this.failed_login = true
            }
        }
    }
}
</script>
