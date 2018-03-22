<template>
  <v-container text-xs-center >
  <v-layout row wrap>
    <v-flex xs12 md6 offset-md3>
        <h2>Sign in form</h2>
        <v-form ref="form" >

            <v-text-field
            label="email"
            id="email"
            v-model="email"
            :error-messages="errors.collect('email')"
            v-validate="'required|email'"
            type="email"
            data-vv-name="email"
            ></v-text-field>

            <v-text-field
            label="password"
            id="password"
            v-model="password"
            type="password"
            ></v-text-field>

            <v-btn
            type="submit"
            @click.stop.prevent="submit"
            > SIGN IN </v-btn>

                <v-alert type="success" dismissible v-model="alert">
                {{alertMessage}}
                </v-alert>

                <v-alert type="warning" dismissible v-model="warning">
                {{warningMessage}}
                </v-alert>

                <v-alert type="error" dismissible v-model="error">
                {{errorMessage}}
                </v-alert>

        </v-form>
        </v-flex>
    </v-layout>
  </v-container>
</template>



<script>
import axios from 'axios'

export default {
  $_veeValidate: {
    validator: 'new'
  },
  data () {
    return {
      password: '',
      email: '',
      error: '',
      errorMessage: '',
      warning: '',
      warningMessage: '',
      alert: '',
      alertMessage: ''
    }
  },
  methods: {
    submit () {
      this.$validator.validateAll()
      var app = this
      var regInfo = {
        'password': this.password,
        'email': this.email
      }
      axios.post(
      app.$store.state.api + 'login',
      {data: regInfo}
      ).then((response) => {
        if (response.data.status === 'success') {
          app.alert = response
          var token = response.data.token
          var expire = JSON.parse(atob(token.split('.')[1]))
          console.log(token)
          console.log(expire)
          console.log(expire.exp)
          app.$auth.setToken(token, expire.exp)
          if (this.$auth.getToken()) {
            this.$store.dispatch('setLogin')
          }
          app.alertMessage = 'Успех!'
        } else if (response.data.status === 'warning') {
          app.warning = response
          app.warningMessage = response.data.message
        } else {
          app.error = true
          app.errorMessage = 'Ошибка'
        }
      }).catch((error) => {
        app.error = error
        app.errorMessage = 'Неизвестная ошибка'
      })
      console.log('login')
    }
  }
}
</script>