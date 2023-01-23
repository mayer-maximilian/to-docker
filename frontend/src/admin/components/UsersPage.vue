<template>
    <b-container fluid>
        <b-row>
            <b-col cols="8" style="text-align: center;">
                <div>
                    <h3>Users</h3>
                </div>
                <b-table :items="users" :fields="fields">
                    <template #cell(edit)="row">
                        <b-button variant="primary" @click="setEditingUser(row.item)" size="sm">Edit</b-button>
                    </template>
                </b-table>
                <b-button class="mt-5" style="float:left" variant="success" @click="setAddingUser()">Add user</b-button>
            </b-col>

            <!-- Add a user -->
            <b-col cols="4" v-if="adding_user">
                <div class="shadow p-3 mb-5 bg-white rounded">
                    <h3>Add user</h3>
                    <b-form @submit="submitNewUser" @reset="onReset" @submit.prevent>
                        <b-form-group id="username-inputgr" label="Username:" label-for="username-input">
                            <b-form-input
                                id="username-input"
                                v-model="adding_user.username"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <b-form-group id="pw-inputgr" label="New Password:" label-for="pw-input">
                            <b-form-input
                                id="pw-input"
                                type="password"
                                v-model="adding_user.password"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <b-form-group id="cpw-inputgr" label="Confirm password:" label-for="cpw-input">
                            <b-form-input
                                id="cpw-input"
                                type="password"
                                v-model="adding_user.confirm_password"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <div 
                            class="mb-2" 
                            style="color:red;" 
                            v-if="adding_user.confirm_password !== adding_user.password && adding_user.confirm_password"
                        >*Please confirm the password</div>
                        <b-button type="reset" variant="secondary">Cancel</b-button>
                        <b-button 
                            :disabled="adding_user.confirm_password !== adding_user.password" 
                            style="margin-left:1rem;" 
                            type="submit" 
                            variant="primary"
                        >Submit</b-button>
                    </b-form>
                </div>
            </b-col>

            <!-- Edit a user -->
            <b-col cols="4" v-else-if="editing_user">
                <div class="shadow p-3 mb-5 bg-white rounded">
                    <h3>Edit user</h3>
                    <b-form @submit="editItem" @reset="onReset" @submit.prevent>
                        <b-form-group id="username-inputgr" label="Username:" label-for="username-input">
                            <b-form-input
                                id="username-input"
                                v-model="editing_user.username"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <b-form-checkbox style=" margin-bottom: 2rem" v-model="editing_user.disabled" name="check-button" switch>
                            Disabled
                        </b-form-checkbox>
                        <b-button type="reset" variant="secondary">Cancel</b-button>
                        <b-button style="margin-left:1rem;" type="submit" variant="primary">Submit</b-button>
                    </b-form>
                    <hr />
                    <b-form class="mt-5" @submit="changePassword" @reset="onReset" @submit.prevent>
                        <b-form-group id="pw-inputgr" label="New Password:" label-for="pw-input">
                            <b-form-input
                                id="pw-input"
                                type="password"
                                v-model="editing_user.new_password"
                                required
                            ></b-form-input>
                        </b-form-group>
                        
                        <b-form-group id="cpw-inputgr" label="Confirm password:" label-for="cpw-input">
                            <b-form-input
                                id="cpw-input"
                                type="password"
                                v-model="editing_user.confirm_password"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <div 
                            class="mb-2" 
                            style="color:red;" 
                            v-if="editing_user.confirm_password !== editing_user.new_password && editing_user.confirm_password"
                        >*Please confirm the password</div>

                        <b-button type="reset" variant="secondary">Cancel</b-button>
                        <b-button 
                            :disabled="editing_user.confirm_password !== editing_user.new_password" 
                            style="margin-left:1rem;" 
                            type="submit" 
                            variant="primary"
                        >Submit</b-button>
                    </b-form>
                    <b-button class="mt-5" variant="danger" v-b-modal.modal-delete>Delete</b-button>
                    <b-modal id="modal-delete" title="Delete user" hide-footer>
                        Are you sure you want to delete user: <b>{{this.editing_user.username}}</b>?<br />
                        This action is permanent and cannot be undone.
                        <div style="text-align:right;margin-top:1rem;">
                            <b class="m-1">Confirm</b>
                            <b-button class="m-1" size="sm" variant="secondary" @click="onReset()">
                                Cancel
                            </b-button>
                            <b-button class="m-1S" size="sm" variant="danger" @click="deleteUser()">
                                Delete
                            </b-button>
                        </div>
                    </b-modal>
                </div>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import axios from 'axios'
import {getCookie} from '@/utils/cookies'
import {getUser, userLogOff} from '@/utils/user'
import getEnv from '@/utils/env'

export default {
    name: 'users-page',
    data () {
        return {
            editing_user: null,
            adding_user: null,
            users: null,
            fields: [
                {
                    key: "username",
                    label: "Username",
                    sortable: true
                },
                { key: "disabled", label: "Disabled" },
                { key: "edit" }
            ]
        }
    },
    methods: {
        getUsers () {
            let jwt_token = getCookie("jwt")
            if (jwt_token) {
                axios.get(`${!getEnv('ENV') ? 'http://20.31.14.128/api' : ''}/users/get-users`, {'headers': {'Authorization': `bearer ${jwt_token}`}})
                .then((response) => {
                    this.users = response.data.users
                })
            }
        },
        setEditingUser (item) {
            this.onReset()
            this.editing_user = JSON.parse(JSON.stringify(item));
        },
        setAddingUser () {
            this.onReset()
            this.adding_user = {
                username: "",
                password: "",
                confirm_password: ""
            }
        },
        editItem () {
            let jwt_token = getCookie("jwt")
            axios.post(`${!getEnv('ENV') ? 'http://20.31.14.128/api' : ''}/users/update-user`, this.editing_user, {'headers': {'Authorization': `bearer ${jwt_token}`}})
            .then(() => {
                this.getUsers()
                this.onReset()
            })
        },
        onReset () {
            this.editing_user = null;
            this.adding_user = null;
        },
        changePassword () {
            let jwt_token = getCookie("jwt")
            let current_user = getUser();
            let data = new FormData()
            data.append('username', this.editing_user.username)
            data.append('password', this.editing_user.new_password)
            axios.post(`${!getEnv('ENV') ? 'http://20.31.14.128/api' : ''}/users/change-password`, data, {'headers': {'Authorization': `bearer ${jwt_token}`}})
            .then(() => {
                if (current_user === this.editing_user.username) {
                    userLogOff()
                    this.$router.push({'name': 'login'})
                } else {
                    this.getUsers()
                    this.onReset()
                }
            })
        },
        submitNewUser () {
            let jwt_token = getCookie("jwt")
            axios.post(`${!getEnv('ENV') ? 'http://20.31.14.128/api' : ''}/users/add-user`, this.adding_user, {'headers': {'Authorization': `bearer ${jwt_token}`}})
            .then(() => {
                this.getUsers()
                this.onReset()
            })
        },
        deleteUser () {
            let jwt_token = getCookie("jwt")
            axios.post(`${!getEnv('ENV') ? 'http://20.31.14.128/api' : ''}/users/delete-user?username=${this.editing_user.username}`, {}, {'headers': {'Authorization': `bearer ${jwt_token}`}})
            .then(() => {
                this.getUsers()
                this.onReset()
            })
        }
    },
    created () {
        this.getUsers();
    },
}
</script>