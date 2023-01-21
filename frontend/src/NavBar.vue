<template>
    <b-container fluid style="background-color:#2E86C1; margin-bottom:1rem; ">
        <b-row class="pb-1 pt-1">
            <b-col cols=6>
                <b-button style="float:left" variant="light" @click="toPage('home')">Home</b-button>
            </b-col>
            <b-col cols=6>
                <b-button v-if=!this.user style="float:right" variant="light" @click="toPage('login')">Login</b-button>
                <b-button v-else style="float:right" variant="light" @click="logOff()">Logout</b-button>
                <b-button v-if=this.user style="float:right; margin-right: 1rem" variant="light" @click="$router.push({name: 'admin'})">Admin</b-button>
            </b-col>

        </b-row>
                
    </b-container>
</template>

<script>
import {getUser, userLogOff} from '@/utils/user';
import {eventBus} from '@/main';

export default {
    name: 'navbar',
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
        logOff () {
            userLogOff();
            this.$router.push({name: 'login'})
        },
        toPage (pagename) {
            if (this.$route.name !== pagename) {
                this.$router.push({name: pagename})
            }
        }
    }
}
</script>
