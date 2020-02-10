<template id="income-form-template">
  <form action="/income" method="POST" v-on:submit.prevent="ajaxSubmit" v-bind:class="{ 'border border-danger': isError }">
    <div class="row p-4">
      <div class="col">
        <input class="form-control form-control-sm" placeholder="description" type="text" name="description" v-model="formData.description">
      </div>
      <div class="col">
        <select class="custom-select-sm" name="frequency" v-model="formData.frequency">
          <option value="weekly">weekly</option>
          <option value="monthly">monthly</option>
          <option value="quarterly">quarterly</option>
        </select>
      </div>

      <div class="col">
        <input class="form-control form-control-sm" placeholder="sum" type="text" name="quantity" v-model="formData.quantity">
      </div>
      <div class="col">
        <input class="btn btn-sm btn-outline-primary" type="submit" >
      </div>
    </div>
  </form>
</template>

<script>
  module.exports = {
    data: function () {
      return {
        isError: false,
        formData: {
          frequency: '',
          description: '',
          quantity: '',
        },
      }
    },
    methods: {
      ajaxSubmit: async function () {
        try {
          await axios.post('/income', this.formData)
          this.isError = false
          this.$emit('update-rules')
        } catch(e) {
          console.log(e)
          this.isError = true
        }
      }
    }
  }
</script>
