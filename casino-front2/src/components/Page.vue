/* eslint-disable */

<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <img src="@/assets/logo.png" alt="Vuetify.js" class="mb-5">
        <blockquote>
          &#8220;{{ userName }} - ANUS PINUS - {{ userCash }} : ({{ cur_time }})&#8221;
          <footer>
          </footer>
        </blockquote>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      userCash: '1',
      userName: '2'
    }
  },
  computed: {
    cur_time: function () {
      var app = this
      console.log(Date.now())
      axios.get('http://localhost:5000/user').then(function (response) {
        app.userName = response.data.name
        app.userCash = response.data.cash
      })
      return Date.now()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
