<template id="rules-view-template">
  <div class="rules-view-template">
    <div class="row pl-4 pr-4 pt-4">
      <div class="col-6">
        <h4>Income</h4>
        <table class="table table-sm">
          <tr class="income" v-for="rule in rulesData['income']">
            <td>{{ rule[2] }}</td>
            <td>{{ rule[3] }}</td>
            <td>{{ rule[4] }}</td>
            <td>
              <button v-on:click="deleteComponent(rule[0])">x</button>
            </td>
          </tr>
        </table>
      </div>
      <div class="col-6 ">
        <h4>Expenses</h4>
        <table class="table table-sm">
          <tr class="expense" v-for="rule in rulesData['expense']">
            <td>{{ rule[2] }}</td>
            <td>{{ rule[3] }}</td>
            <td>{{ rule[4] }}</td>
            <td>
              <button v-on:click="deleteComponent(rule[0])">x</button>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    template: '#rules-view-template',
    props: ['rulesData'],
    methods: {
      deleteComponent: async function(id) {
        try {
          await axios.delete('/components/'+id)
          this.$emit('update-rules')
        } catch(e) {
          console.log(e)
        }
      }
    }
  }
</script>
