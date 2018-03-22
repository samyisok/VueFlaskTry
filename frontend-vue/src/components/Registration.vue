<template>
  <v-container text-xs-center >
  <v-layout row wrap>
    <v-flex xs12 md6 offset-md3>
        <h2>Registration form</h2>
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

            <v-text-field
            label="confirmPassword"
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            :rules="[comparePasswords]"
            ></v-text-field>



            <v-btn
            type="submit"
            @click.stop.prevent="submit"
            v-if="!loadingState"
            > SIGN UP </v-btn>

            <v-progress-circular indeterminate v-bind:size="70" v-bind:width="7" color="purple" v-if="loadingState"></v-progress-circular>

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
      confirmPassword: '',
      email: '',
      error: '',
      errorMessage: '',
      warning: '',
      warningMessage: '',
      alert: '',
      alertMessage: '',
      loadingState: false

    }
  },
  computed: {
    comparePasswords () {
      return this.password !== this.confirmPassword ? 'Passwords do not match' : true
    }
  },
  methods: {
    submit () {
      this.$validator.validateAll()
      var app = this
      app.loadingState = true
      var regInfo = {
        'password': this.password,
        'email': this.email
      }
      axios.post(
      app.$store.state.api + 'reg',
      {data: regInfo}
      ).then((response) => {
        if (response.data.status === 'success') {
          app.alert = response
          app.alertMessage = 'Ваш ID: ' + response.data.id
        } else if (response.data.status === 'warning') {
          app.warning = response
          app.warningMessage = response.data.message
        } else {
          app.error = true
          app.errorMessage = 'Ошибка Регистрации'
        }
        app.loadingState = false
      }).catch((error) => {
        app.error = error
        app.errorMessage = 'Неизвестная ошибка'
        app.loadingState = false
      })
    }
  }
}
</script>

<style scoped>

</style>
