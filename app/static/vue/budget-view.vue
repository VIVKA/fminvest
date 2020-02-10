<template id="budget-view-template">
  <div class="budget-view-template">
    <div class="row">
      <main role="main">
        <div style="height: 2px; background: goldenrod; width: 100%;"></div>
        <div>
          <div class="row mb-4">
            <div class="col">
              <div class="bg-white shadow-sm p-3">
                <ul class="nav nav-tabs ">
                  <li class="nav-item">
                    <a class="nav-link" href="#"><b>&sum;</b></a>
                  </li>
                  <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle active" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">John Doe </a>
                    <div class="dropdown-menu">
                      <a class="dropdown-item" href="#">link</a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item text-danger" href="#">delete</a>
                    </div>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#"><b>+</b></a>
                  </li>
                </ul>
                <br>
                <br>
                <chart-view/>
              </div>
            </div>
          </div>
          <div class="row mb-4">
            <div class="col">
              <div class="bg-white shadow-sm">
                <stats-view :stats-data="stats_data"></stats-view>
              </div>
            </div>
          </div>
          <div class="row mb-4">
            <div class="col">
              <div class="bg-white shadow-sm">
                <rules-view :rules-data="rules_data" v-on:update-rules="reload"/></rules-view>
                <div class="row pl-4 pr-4 pt-4">
                  <div class="col-6"><income-form v-on:update-rules="reload"/></div>
                  <div class="col-6"><expense-form v-on:update-rules="reload"/></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
  module.exports = {
    data: function () {
      return {
        stacked_data: [],
        rules_data: {
          rules: [],
          income: 0,
          expense: 0,
        },
        stats_data: 1000,
      }
    },
    methods: {
      reload: async function() {
        await this.loadStacked()
        await this.loadStats()
        await this.loadRules()
      },
      loadStacked: async function() {
        try {
          const response = await axios.get('/stacked_data')
          this.stacked_data = response.data
        } catch(e) {
          this.stacked_data = []
        }
        plot_stacked('.chart-view-1', this.stacked_data)
      },
      loadStats: async function() {
        try {
          const response = await axios.get('/stats')
          this.stats_data = response.data
        } catch(e) {
          console.log(e)
        }
      },
      loadRules: async function() {
        try {
          const response = await axios.get('/components')
          this.rules_data = response.data
        } catch(e) {
          console.log(e)
        }
      }
    },
    mounted: async function () {
      show_chart('.chart-view-1');
      await this.loadStacked()
      await this.loadRules()
      await this.loadStats()
    }
  }
</script>
