<template>
    <b-container fluid>

        <!-- <b-alert show variant="danger" >Default Alert</b-alert> -->

        <b-row class="justify-content-md-center">
            <b-col md="4" class="shadow p-3 mb-5 bg-white rounded">
                <h3>Register</h3>
                <add-user-form @on-response="onResponse"/>
            </b-col>
        </b-row>

        <b-alert 
            :show="failed_registration" 
            dismissible 
            variant="danger"
            @dismissed="failed_registration=0"
            @dismiss-count-down="failedRegistrationUpdate"
        >
            Registration Failed
        </b-alert>
        
    </b-container>
</template>

<script>
import AddUserForm from './components/AddUserForm.vue'
import {userLogIn} from '@/utils/user';

export default {
    components: {AddUserForm},
    name: 'register',
    data() {
        return {
            form: {
                username: null,
                password: null
            },
            failed_registration: 0,
            failed_registration_max: 3
        }
    },
    computed: {
        validInput () {
            return !!(this.form.username && this.form.password);
        }
    },
    methods: {
        async onResponse(response, userForm) {
            if (response.status_code !== 202) {
                this.failed_registration = this.failed_registration_max
            }

            let successful = await userLogIn(userForm.username, userForm.form.password)
            console.log('successful', successful)
            if (successful) {
                await this.$router.push({name: 'home'})
            } else {
                this.failed_registration = this.failed_registration_max
            }
        },
        failedRegistrationUpdate(failed_registration) {
            this.failed_registration = failed_registration
        }
    }
}
</script>