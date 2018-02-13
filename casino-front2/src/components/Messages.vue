<template>
  <v-container text-xs-center >
  <v-layout row wrap>

   <v-dialog v-model="dialog" max-width="990">
    <v-toolbar color="pink">
      <v-toolbar-title class="white--text">From: {{msgDialogSender}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-icon>email</v-icon>
    </v-toolbar>
            <v-card>
            <v-card-title class="headline">{{msgDialogTitle}}</v-card-title>
            <v-card-text>{{msgDialog}}</v-card-text>
            <v-card-text class="grey--text">{{msgDialogDate}}</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" flat="flat" @click.native="dialog = false">close</v-btn>
            </v-card-actions>
            </v-card>
   </v-dialog>

  <v-flex xs12 sm6 offset-sm3>
    <div class="text-xs-center" v-if="pagesTotal">
      <v-pagination :length="pagesTotal" v-model="page" ></v-pagination>
    </div>
    <br>

      <v-card>
        <v-toolbar color="cyan" dark>
          <v-toolbar-title>Сообщения</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-progress-circular indeterminate v-bind:size="70" v-bind:width="7" color="purple" v-if="loadingState"></v-progress-circular>
        <v-list two-line v-if="!loadingState">
         <template v-for="(item, index) in items">
            <v-list-tile
              ripple
              @click="toggle(index)"
              :key="item.title"
            >
              <v-list-tile-action>
              <v-icon v-if="item.status === 1" color="pink">error</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>From: {{ item.sender }}</v-list-tile-title>
                <v-list-tile-sub-title class="grey--text text--darken-4">{{ item.title }}</v-list-tile-sub-title>
                <v-list-tile-sub-title>{{ item.message }}</v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-list-tile-action-text>{{ item.date }}</v-list-tile-action-text>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider v-if="index + 1 < items.length" v-bind:key="item.id"></v-divider>
          </template>
        </v-list>
      </v-card>

  
    </v-flex>

    <v-flex xs12 md6 offset-md3>
        <h2>  {{curData}} </h2>

                <v-alert type="success" dismissible v-model="alert">
                {{alertMessage}}
                </v-alert>

                <v-alert type="warning" dismissible v-model="warning">
                {{warningMessage}}
                </v-alert>

                <v-alert type="error" dismissible v-model="error">
                {{errorMessage}}
                </v-alert>

        </v-flex>


    </v-layout>
  </v-container>
</template>



<script>
import axios from 'axios'

export default {
  data () {
    return {
      error: '',
      errorMessage: '',
      warning: '',
      warningMessage: '',
      alert: '',
      alertMessage: '',
      items: [
      ],
      msgDialog: '',
      msgDialogTitle: '',
      msgDialogSender: '',
      msgDialogDate: '',
      dialog: false,
      loadingState: false,
      pagesTotal: 0,
      page: 1
    }
  },
  computed: {
    curData () {
      return this.getData()
    },
    isLogin: function () {
      return this.$store.state.isAuth
    }
  },
  methods: {
    getData () {
      var app = this
      app.loadingState = true
      axios.defaults.headers.common['x-access-token'] = app.$auth.getToken()
      axios.post(
      app.$store.state.api + 'messages',
        {
          data: { 'page': app.page }
        }
      ).then((response) => {
        if (response.data.status === 'success') {
          app.alert = response
          console.log(response.data.payload)
          app.items = response.data.payload
          app.pagesTotal = response.data.pages
          app.alertMessage = response.data.result
        } else if (response.data.status === 'warning') {
          app.warning = response
          app.warningMessage = response.data.message
        } else {
          app.error = true
          app.errorMessage = response.data.message | 'what'
        }
        app.loadingState = false
      }).catch((error) => {
        app.error = error
        app.errorMessage = 'Неизвестная ошибка'
        app.loadingState = false
      })
    },
    toggle (index) {
      this.dialog = true
      this.msgDialog = this.items[index].message
      this.msgDialogTitle = this.items[index].title
      this.msgDialogSender = this.items[index].sender
      this.msgDialogDate = this.items[index].date
    }
  }
}
</script>