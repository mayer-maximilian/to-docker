<template>
    <b-form @submit="submitNewUser" @reset="onReset" @submit.prevent>
        <b-form-group id="username-inputgr" label="Username:" label-for="username-input">
            <b-form-input
                id="username-input"
                v-model="user.username"
                required
            ></b-form-input>
        </b-form-group>
        <b-form-group id="pw-inputgr" label="New Password:" label-for="pw-input">
            <b-form-input
                id="pw-input"
                type="password"
                v-model="user.password"
                required
            ></b-form-input>
        </b-form-group>
        <b-form-group id="cpw-inputgr" label="Confirm password:" label-for="cpw-input">
            <b-form-input
                id="cpw-input"
                type="password"
                v-model="user.confirm_password"
                required
            ></b-form-input>
        </b-form-group>
        <div 
            class="mb-2" 
            style="color:red;" 
            v-if="user.confirm_password !== user.password && user.confirm_password"
        >*Please confirm the password</div>
        <b-button 
            :disabled="user.confirm_password !== user.password" 
            style="margin-left:1rem;" 
            type="submit" 
            variant="primary"
        >Submit</b-button>
        <b-button type="reset" variant="secondary">Cancel</b-button>
    </b-form>
</template>

<script>
import {post} from '@/utils/request'

export default {
    name: 'add-user-form',
    data () {
        return {
            user: {
                username: "",
                password: "",
                confirm_password: ""
            }
        }
    },
    methods: {
        onReset () {
            this.user = {
                username: "",
                password: "",
                confirm_password: ""
            }
        },
        submitNewUser () {
            post(`api/users/register`, this.user)
            .then((response) => {
                this.$emit('on-response', { response: response, 
                                            username: this.user.username, 
                                            password: this.user.password,
                                            error: null })
                this.onReset()
            }).catch((error) => {
                this.$emit('on-response', { response: null, 
                                            username: this.user.username, 
                                            password: this.user.password,
                                            error: error })
                this.onReset()
            })
        }
    }
}
</script>
  