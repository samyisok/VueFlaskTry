<template>
  <v-container text-xs-center >
  <v-layout row wrap>
    <v-flex xs12 md6 offset-md3>
        <h2> TEST {{curData}} </h2>

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
      alertMessage: ''
    }
  },
  computed: {
    curData () {
      return this.getData()
    }
  },
  methods: {
    getData () {
      var app = this
      axios.defaults.headers.common['x-access-token'] = app.$auth.getToken()
      axios.post(
      app.$store.state.api + 'test',
        {
          data: {}
        }
      ).then((response) => {
        if (response.data.status === 'success') {
          app.alert = response
          app.alertMessage = response.data.message
        } else if (response.data.status === 'warning') {
          app.warning = response
          app.warningMessage = response.data.message
        } else {
          app.error = true
          app.errorMessage = response.data.message | 'what'
        }
      }).catch((error) => {
        app.error = error
        app.errorMessage = 'Неизвестная ошибка'
      })
      console.log('login')
      return 2
    }
  }
}
</script>