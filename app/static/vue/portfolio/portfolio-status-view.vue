<template>
  <div v-bind:class="{ 'loading': !portfolioData }" class="ui-block p-3 shadow-sm portfolio-status mb-4">
    <!-- <div class="row mb-3">
        <div class="col">
            <h4 class="text-secondary">{{$t('message.title')}}</h4>
        </div>
    </div> -->
    <div class="row">
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.day_change')}}
        </small><br>
        <h4 class="hide-when-loading" v-bind:class="{ 'text-danger': portfolioData.ch < 0, 'text-success': portfolioData.ch > 0, }">
          {{d3.format("+.3f")(portfolioData.ch)}}%
        </h4 >
      </div>
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.total_value')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{formatCurrency(portfolioData.tv)}}
        </h4>
      </div>
      <div class=" col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.dividend_value')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{formatCurrency(portfolioData.tv*portfolioData.y)}}
        </h4>
      </div>
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.returns')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{ (portfolioData.r*100).toFixed(1) }}
          <small class="text-secondary" style="font-size: 70%">
            ({{ (portfolioData.or*100).toFixed(1) }})
          </small><br>
        </h4>
        <!-- <small>
          1: {{ (portfolioData.rs[0]*100).toFixed(1) }},
          3: {{ (portfolioData.rs[1]*100).toFixed(1) }},
          5: {{ (portfolioData.rs[2]*100).toFixed(1) }}
        </small> -->
      </div>
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.volatility')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{ (portfolioData.d*100).toFixed(1) }}
          <small class="text-secondary">
            ({{ (portfolioData.od*100).toFixed(1) }})
          </small>
        </h4>
        <!-- <small>
          1: {{ (portfolioData.ds[0]*100).toFixed(1) }},
          3: {{ (portfolioData.ds[1]*100).toFixed(1) }},
          5: {{ (portfolioData.ds[2]*100).toFixed(1) }}
        </small> -->
      </div>
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.yield')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{ (portfolioData.y*100).toFixed(1) }}
          <small class="text-secondary">
            ({{ (portfolioData.oy*100).toFixed(1) }})
          </small>
        </h4>
        <!-- <small>
          1: {{ (portfolioData.ys[0]*100).toFixed(1) }},
          3: {{ (portfolioData.ys[1]*100).toFixed(1) }},
          5: {{ (portfolioData.ys[2]*100).toFixed(1) }},
        </small> -->
      </div>
      <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          {{$t('message.utility')}}
        </small><br>
        <h4 class="hide-when-loading">
          {{ (portfolioData.u*100).toFixed(1) }}
          <small class="text-secondary">
            ({{ (portfolioData.ou*100).toFixed(1) }})
          </small>
        </h4>
      </div>
      <!-- <div class="col">
        <small class="text-secondary" style="font-size: 70%">
          CURRENCY
        </small><br>
        <h4>₽ $ €</h4>
      </div> -->
    </div>
  </div>
</template>

<script>
  module.exports = {
    props: ['portfolioData'],
    i18n: {
        messages: {
            en: { message: {
                title: 'Portfolio stats',
                day_change: 'Δ LAST DAY', total_value: 'TOTAL VALUE',
                dividend_value: 'ANNUAL DIVIDEND', returns: 'RETURNS, %',
                volatility: 'VOLATILITY, %', yield: 'YIELD, %',
                utility: 'UTILITY',
            } },
            ru: { message: {
                title: 'Показатели портфеля',
                day_change: 'Δ ПОСЛЕДНИЙ ДЕНЬ', total_value: 'СОВОКУПНАЯ СТОИМОСТЬ',
                dividend_value: 'ГОДОВОЙ ДИВИДЕНД', returns: 'ДОХОДНОСТЬ, %',
                volatility: 'ВОЛАТИЛЬНОСТЬ, %', yield: 'ДИВ. ДОХОДНОСТЬ, %',
                utility: 'ПОЛЕЗНОСТЬ',
            } },
        }
    },
  }
</script>

<style>
  .portfolio-status small {
    white-space: nowrap;
  }

  .portfolio-status.loading {
    opacity: 0.5;
  }

  .portfolio-status.loading .hide-when-loading {
    opacity: 0;
  }
</style>
