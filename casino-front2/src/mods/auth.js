export default function (Vue) {
  Vue.auth = {
        // set token
    setToken: (token, expire) => {
      localStorage.setItem('token', token)
      localStorage.setItem('expire', expire)
    },
        // get token
    getToken: () => {
      if (localStorage.getItem('expire') && localStorage.getItem('token')) {
        if (localStorage.getItem('expire') > Math.round(Date.now() / 1000)) {
          return localStorage.getItem('token')
        } else {
          console.log(Math.round(Date.now() / 1000))
          console.log(localStorage.getItem('expire'))
          localStorage.removeItem('token')
          localStorage.removeItem('expire')
          return false
        }
      } else {
        return false
      }
    },
        // destroy token
    destroyToken: () => {
      localStorage.removeItem('token')
      localStorage.removeItem('expire')
    },
        // isAuthenticated
    isAuthenticated: () => {
      if (this.getToken()) {
        return true
      } else {
        return false
      }
    }

  }

  Object.defineProperties(Vue.prototype, {
    $auth: {
      get: () => { return Vue.auth }
    }
  })
}
