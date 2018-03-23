<template>
  <v-app @updateCountMsg="anus()" >
    <v-navigation-drawer
      value="False"
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
      <v-list>
        <v-list-tile
          value="true"
          v-for="(item, i) in items"
          :key="i"
          :to="item.path"
          v-if="!item.auth || isLogin"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      app
      :clipped-left="clipped"
    >
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title v-text="title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="isLogin" flat icon large to='/messages' >
       <v-badge overlay left color="red" overlap>
         <span slot="badge" v-if='newMsgCount > 0' >{{newMsgCount}}</span>
         <v-icon large>email</v-icon>
       </v-badge>
      </v-btn>
      <login></login>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
    <v-footer :fixed="fixed" app>
      <span>&copy; 2017 </span>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios'
import Login from '@/components/Login'
export default {
  computed: {
    isLogin: function () {
      return this.$store.state.isAuth
    },
    newMsgCount: function () {
      this.getCountMsg()
      return this.$store.state.newMsg
    }
  },
  data () {
    return {
      clipped: false,
      drawer: null,
      fixed: false,
      items: [{
        title: 'Home',
        path: '/',
        auth: false
      },
      {
        title: 'Registration',
        path: '/registration',
        auth: false
      },
      {
        title: 'Login',
        path: '/login',
        auth: false
      },
      {
        title: 'test',
        path: '/test',
        auth: true
      },
      {
        title: 'Messages',
        path: '/messages',
        auth: true
      }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'TestApp'
    }
  },
  methods: {
    getCountMsg () {
      var app = this
      axios.defaults.headers.common['x-access-token'] = app.$auth.getToken()
      axios.post(
      app.$store.state.api + 'new_messages_count',
        {
          data: {}
        }
      ).then((response) => {
        if (response.data.status === 'success') {
          console.log('payload:' + response.data.payload)
          this.$store.dispatch('setMsgIcon', response.data.payload)
        }
      }).catch((error) => {
        app.error = error
        app.errorMessage = 'Неизвестная ошибка'
      })
    },
    anus () {
      console.log('Anus')
    }
  },
  name: 'App',
  components: { Login }
}
</script>
