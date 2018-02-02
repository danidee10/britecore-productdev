<template>
  <div class="col-sm-6 offset-3">
    <h2 :key="risk.id" v-for="risk in risks" class="text-center">
      <router-link :to="`/${risk.id}`">
        {{ risk.name }} Insurance
      </router-link>
    </h2>
  </div>
</template>

<script>
// Component to fetch all Risks from the api

import axios from 'axios'

export default {
  data () {
    return {
      risks: []
    }
  },

  created () {
    axios.get('http://localhost:5000/risks/')
      .then((response) => {
        this.risks = response.data
      })
      .catch((error) => {
        console.error(error)
      })
  }
}
</script>
