<template id="add-asset-form-template">
  <div :class="{ 'loading': !selectedPortfolioId }" class="ui-block p-3 shadow-sm portfolio-add-asset mb-4 rounded">
    <div class="row mb-3">
        <div class="col">
            <h4 class="text-secondary">{{$t('message.title')}}</h4>
        </div>
    </div>
    <div class="row">
      <div class="col">
        <form action="/add_asset" class="form-group" method="POST" v-on:submit.prevent="ajaxSubmit">
            <div class="form-row">
              <div class="col mb-3">
                <label class="text-secondary">{{$t('message.ticker')}}</label>
                <input class="form-control" type="text" name="description" v-model="form.asset" v-bind:class="{ 'is-valid': assetValid === true, 'is-invalid': assetValid === false }">
              </div>

              <div class="col-6 mb-3">
                <label class="text-secondary">{{$t('message.action_at')}}</label>
                <datepicker name="action_at" v-model="form.action_at" bootstrap-styling></datepicker>
              </div>

              <div class="col-6 mb-3">
                <label class="text-secondary">{{$t('message.action_type')}}</label>
                <select v-model="form.action_type" class="custom-select">
                  <option value="BUY">{{$t('message.action_type_buy')}}</option>
                  <option value="SELL">{{$t('message.action_type_sell')}}</option>
                </select>
              </div>

              <div class="col mb-3">
                <label class="text-secondary">{{$t('message.amount')}}</label>
                <input class="form-control" type="number" min="0" name="amount" v-model="form.amount">
              </div>

              <div class="col mb-3">
                <label class="text-secondary">{{$t('message.price')}}<sup>*</sup></label>
                <input class="form-control" type="number" min="0" step="0.0001" name="price" v-model="form.price">
              </div>
            </div>
            <div class="form-row">
              <div class="col mb-3">
                <input class="btn btn-primary" v-bind:class="{ 'disabled': !formValid }" type="submit" :value="$t('message.commit')">
              </div>
            </div>
        </form>
        <small class="text-secondary"><sup>*</sup> {{$t('message.disclamer')}}</small>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    components: {
      datepicker: vuejsDatepicker
    },
    i18n: {
        messages: {
            en: { message: {
                action_at: 'trade date', ticker: 'ticker', dividend: 'dividend',
                amount: 'amount', price: 'price', commit: 'commit',
                title: 'Add to portfolio', action_type: 'order type',
                action_type_buy: 'buy', action_type_sell: 'sell',
                disclamer: 'If price is not defined, a closing price for the specified trade date will be used.',
            } },
            ru: { message: {
                action_at: 'дата сделки', ticker: 'тикер', dividend: 'дивиденд',
                amount: 'количество', price: 'цена', commit: 'совершить',
                title: 'Добавить в портфель', action_type: 'тип сделки',
                action_type_buy: 'покупка', action_type_sell: 'продажа', disclamer: 'Если цена не указана, будет использована цена закрытия указанного торгового дня.',
            } },
        }
    },
    computed: {
        selectedPortfolioId: function() {
          return this.$store.state.selectedPortfolioId
        },
        formValid: function () {
          return this.assetValid && this.form.action_at && this.form.amount
        }
    },
    data: function () {
      return {
        assetValid: undefined,
        form: {
          action_type: 'BUY',
        },
      }
    },
    watch: {
      form: {
        handler: function (form) {
          const that = this
          that.assetValid = undefined

          if(!form.asset || form.asset.length == 0 ) {
            clearTimeout(this.t)
            return
          }

          const q = '/asset/'+form.asset

          const f = () => {
            return axios.get(q)
              .then(function (response) {
                that.form.asset_id = response.data.id
                that.assetValid = true
              })
              .catch(function (error) {
                that.assetValid = false
              })
          }

          clearTimeout(this.t)
          this.t = setTimeout(f, 1000)
        },
        deep: true
      }
    },
    methods: {
      ajaxSubmit: async function () {
        if(!(this.assetValid)) {
          return
        }

        const post_data = {
          'asset_id': this.form.asset_id,
          'asset_ticker': this.form.asset,
          'amount': this.form.amount,
          'price': this.form.price,
          'action_at': this.form.action_at,
          'action_type': this.form.action_type,
        }

        try {
          await axios.post(`/portfolios/${this.selectedPortfolioId}/actions`, post_data)
          this.$store.dispatch('reloadCurrentPortfolio')
        } catch (e) {
          console.log(e)
        }
      }
    },
  }
</script>

<style>
  .portfolio-add-asset .vdp-datepicker__calendar {
    color: #333;
    width: 100%;
  }
</style>
