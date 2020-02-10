<template>
  <tr class="portfolio-asset-template">
    <td style="font-family: Roboto Mono; white-space: nowrap">
      <span class="h5">{{flagFromCountry(assetData.country)}}</span>
      <span v-if="assetData.asset_type == 'stock'">{{ assetData.ticker }}</span>
      <small v-if="assetData.asset_type == 'bond'">{{ assetData.ticker }}</small>
      <small class="text-secondary">
        <!-- {{ gicsNameFromCode(assetData.sector) }} -->
      </small>
    </td>
    <!-- <td>
    </td> -->
    <td class="text-right">
      <span v-bind:class="{ 'text-danger': assetData.ch < 0, 'text-success': assetData.ch > 0, }">
        {{ d3.format("+.2f")(assetData.ch) }}<!-- <small style="opacity: 0.5">%</small> -->
      </span>
    </td>
    <td class="text-right">
      <span v-bind:class="{ 'text-danger': assetData.ch < 0, 'text-success': assetData.ch > 0, }">
        {{ formatCurrency(assetData.p, assetData.country) }}
      </span>
    </td>
    <td class="text-right">
      {{ assetData.amount }}
    </td>
    <td class="text-right">
      <span class="text-secondary">{{ formatCurrency(assetData.tv, assetData.country) }}</span>
    </td>
    <td><!-- distribution --></td>

    <td class="text-right d-none d-sm-table-cell">
      {{ (assetData.weight*100).toFixed(1) }}
    </td>
    <td class="text-right d-none d-sm-table-cell">
      <small style="opacity: 0.5">{{(assetData.recommended_weight*100).toFixed(1)}}</small>
    </td>
    <td class="text-right d-none d-sm-table-cell">{{ (assetData.ry[1]*100).toFixed(1) }}<!-- <small style="opacity: 0.5">%</small> --></td>
    <td class="text-right d-none d-sm-table-cell">{{ (assetData.dy[1]*100).toFixed(1) }}<!-- <small style="opacity: 0.5">%</small> --></td>
    <td class="text-right d-none d-sm-table-cell">{{ (assetData.yy*100).toFixed(1) }}<!-- <small style="opacity: 0.5">%</small> --></td>
    <!-- <td class="text-right d-none d-sm-table-cell"><span class="text-secondary">{{ simpleInterval(assetData.updated_at) }}</span></td> -->
    <td class="text-right d-none d-sm-table-cell">
      <span v-bind:class="{ 'text-danger': assetData.cg < 0, 'text-success': assetData.cg > 0, }">
        {{assetData.cg.toFixed(2)}}
      </span>
    </td>
    <td class="text-right d-none d-sm-table-cell">
      {{assetData.divs.toFixed(2)}}
    </td>
    <td class="text-right d-none d-sm-table-cell">
      <span v-bind:class="{ 'text-danger': assetData.tr < 0, 'text-success': assetData.tr > 0, }">
        {{assetData.tr.toFixed(2)}}
      </span>
    </td>
    <td class="d-none d-sm-table-cell"><a href="" class="trash" v-on:click.enter.prevent="ajaxDelete">❌</a></td>
  </tr>
</template>

<script>
  module.exports = {
    props: ['assetData', 'portfolioId'],
    data: function () {
      return {
        isBusy: undefined
      }
    },
    methods: {
      flagFromCountry: function(country)  {
        if(country == 'RU') {
          return '🇷🇺'
        }

        if(country == 'US') {
          return '🇺🇸'
        }
      },
      ajaxDelete: async function () {
        try {
          await axios.delete('/portfolios/'+this.portfolioId+'/assets', { data: {
            asset_id: this.assetData.asset_id,
          }})
          this.$store.dispatch('reloadCurrentPortfolio')
        } catch(e) {
          console.log(e)
        }
      }
    }
  }
</script>

<style>
  .portfolio-asset-template input {
    border: 0;
    border-top: 1px solid #ddd;
    border-left: 1px solid #ddd;
    width: 50%;
    min-width: 5em;
    background: #f9f9f9;
  }

  .portfolio-asset-template .trash {
    font-size: 0.5rem;
    vertical-align: middle;
    visibility: hidden;
    text-decoration: none;
  }

  .theme-light .portfolio-asset-template:hover {
    background: #fff9e6;
  }

  .theme-dark .portfolio-asset-template:hover {
    background: #504945;
  }

  .portfolio-asset-template:hover .trash {
    visibility: visible;
    text-decoration: none;
    opacity: 0.5;
  }

  .portfolio-asset-template td {
    vertical-align: middle;
  }
</style>
