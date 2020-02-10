<template>
  <div class="investments-view-template">
    <div class="row">
      <div class="col">
        <market-clock></market-clock>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <portfolio-navigation></portfolio-navigation>
      </div>
    </div>

    <!-- <div class="row">
      <div class="col">
        <portfolio-contents-view></portfolio-contents-view>
      </div>
    </div>  -->

    <div class="row">
      <div class="col-xl-8">
        <portfolio-contents-view></portfolio-contents-view>
      </div>
      <div class="col-xl-4">
        <div class="row">
          <div class="col-md-6 col-xl-12">
            <portfolio-simulation-hull></portfolio-simulation-hull>
          </div>
          <div class="col-md-6 col-xl-12">
            <add-asset-form></add-asset-form>
          </div>
          <div class="col-md-6 col-xl-12">
            <get-recommendation-form></get-recommendation-form>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 col-xl-4">
        <portfolio-gics></portfolio-gics>
      </div>
      <div class="col-md-6 col-xl-4">
        <portfolio-dividends></portfolio-dividends>
      </div>
      <div class="col-md-6 col-xl-4">
        <portfolio-trades></portfolio-trades>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    mounted: async function () {
      this.$store.dispatch('loadInvestments')
    }
  }
</script>
