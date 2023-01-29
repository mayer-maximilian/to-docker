<template>
    <div>
        <b-row class="justify-content-md-center">
            <b-col md="4" class="shadow p-3 mb-5 bg-white rounded">

                <div v-if="this.user">
                    <h3>Hello World!</h3> 
                    <h3>Life is Good!</h3>
                </div>

                <b-container v-else>
                    <b-row>
                        <h1 style="text-align:center">Basic Todo App</h1>
                    </b-row>

                    <b-row>
                        <h3 style="text-align:center">This is a simple Todo app. Please create an account or log in.</h3>
                    </b-row>

                    <b-row align-h="center">
                        <b-col>
                            <b-button variant="success" style="margin-top: 2em" @click="toPage('register')">Register</b-button>
                        </b-col>
                        <b-col>
                            <b-button variant="secondary" style="margin-top: 2em" @click="toPage('login')">Login</b-button>
                        </b-col>
                    </b-row>
                </b-container>

            </b-col>
        </b-row>
    </div>
</template>

<script>
    import './assets/styles/style.css';
    import {getUser} from '@/utils/user';
    import {eventBus} from '@/main';

    export default {
        name: 'home',
        data () {
            return {
                user: null
            }
        },
        created: function () {
            this.user = getUser()
            eventBus.$on('user-change', () => {
                this.user = getUser()
            });
        },
        methods: {
            toPage (pagename) {
                if (this.$route.name !== pagename) {
                    this.$router.push({name: pagename})
                }
            }
        }
    };
</script>
