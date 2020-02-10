<template id="stats-view-template">
  <div class="row p-4">
    <div class="col-6">
      <h4>Statistics</h4>
      You spend about <b class="text-info">{{statsData.monthly}} ₽$€</b>/month.
      You may want to save aside <b class="text-info">{{statsData.halfYear}} ₽$€</b> in cash.
    </div>
  </div>
</template>

<script>
  module.exports = {
    props: ['statsData'],
  }
</script>
