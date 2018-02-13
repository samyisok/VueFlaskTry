import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  api: 'http://localhost:5000/',
  isAuth: 0,
  newMsg: 0
}

export default new Vuex.Store({
  state,
  getters: {
    isLogin: function (state) {
      return state.isAuth
    }
  },
  mutations: {
    login: function (state) { state.isAuth = 1 },
    logout: function (state) { state.isAuth = 0 },
    MsgIcon: function (state, index) { state.newMsg = index }
  },
  actions: {
    setLogin: function (context) { context.commit('login') },
    setLogout: function (context) { context.commit('logout') },
    setMsgIcon: function (context, index) { context.commit('MsgIcon', index) }
  }
})
