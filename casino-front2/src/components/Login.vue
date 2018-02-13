<template>
      <div v-if="ifLogin"><v-btn @click="logout" color="warning">LOGOUT</v-btn></div>
      <div v-else><v-btn color="info" dark to='/login'>PLEASE LOGIN</v-btn></div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  computed: {
    ifLogin: function () {
      var log = this.checkLogin()
      console.log('iflogin: ' + this.$store.state.isAuth + '|' + log)
      return this.$store.state.isAuth
      //  return this.$store.getters.ifLogin
    }
  },
  methods: {
    logout: function () {
      this.$auth.destroyToken()
      this.$store.dispatch('setLogout')
    },
    checkLogin: function () {
      if (this.$auth.getToken()) {
        this.$store.dispatch('setLogin')
        console.log('setLogin')
        return this.$store.getters.ifLogin
      } else {
        this.$store.dispatch('setLogout')
        console.log('setLogout')
        return this.$store.getters.ifLogin
      }
    }
  }
}
</script>

<style scoped>

</style>
