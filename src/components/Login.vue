<template lang="html">
  <div>
    <b-link @click="toggleModal()">Login</b-link>
    <b-modal :visible="isModalOpen" hide-footer @hide="toggleModal">
      <div>
        <b-form @submit.prevent="onSubmit()">
          <b-form-group
            id="input-group-1"
            label="Username:"
            label-for="input-1"
            label-cols="3"
          >
            <b-form-input
              id="input-1"
              v-model="username"
              autofocus
              placeholder="Enter username"
              required></b-form-input>
          </b-form-group>
          <b-form-group
            id="input-group-2"
            label="Password:"
            label-for="input-2"
            label-cols="3"
          >
            <b-form-input
              id="input-2"
              v-model="password"
              type="password"
              placeholder="Enter password"
              required></b-form-input>
          </b-form-group>
          <b-button block type="submit" variant="primary">Login</b-button>
          <b-alert class="text-center" :show="error!==null" variant="danger">{{ error }}</b-alert>
        </b-form>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
/* eslint-disable */
export default {
  name: 'LoginModal',
  data () {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  computed: {
    ...mapGetters('auth', [
      'isModalOpen'
    ])
  },
  methods: {
    ...mapActions('auth', [
      'authenticate', 'toggleModal'
    ]),
    onSubmit() {
      this.authenticate({args:[this.username, this.password]})
      .then(() => {
        this.toggleModal()
        // this.$router.push({name: 'home'})
      }).catch((e) => {
        // eslint-disable-next-line
        console.warn(e)
        this.error = 'Invalid username/password'
      })
    }
  }
}
</script>

<style lang="css">
</style>
