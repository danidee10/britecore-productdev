<template>
  <div v-show="!this.loading" class="col-sm-6 offset-3">
    <h1>{{ risk.name }} Insurance</h1>

    <form>
      <Widgets :key="field.id" v-for="field in risk.fields" :field="field" />

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

import Widgets from './Widgets.vue'

export default {
  name: 'Risk',
  data () {
    return {
      loading: true,
      risk: {}
    }
  },

  components: {Widgets},

  created () {
    // Fetch a Risk from the api
    axios.get(`${process.env.API_URL}/risks/${this.$route.params.riskId}/`)
      .then((response) => {
        this.risk = response.data
        this.loading = false
      })
      .catch((error) => {
        console.error(error)
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
