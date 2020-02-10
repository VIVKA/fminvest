<template>
  <div :class="{ 'loading': !selectedPortfolioId }" class="ui-block p-3 shadow-sm portfolio-gics mb-4 rounded">
    <div class="row mb-3">
      <div class="col">
        <h4 class="text-secondary">{{$t('message.title')}}</h4>
      </div>
    </div>
    <div class="row mb-3">
      <div class="col">
        <form action="/recommendation" method="GET" v-on:submit.prevent="ajaxSubmit">
          <div class="form-row">
            <div class="col mb-3">
              <label class="text-secondary">{{$t('message.allocation')}}</label>
              <input class="form-control" type="number" min="0" name="amount" v-model="form.amountAllocate">
            </div>
          </div>
          <div class="form-row">
            <div class="col">
              <input class="btn btn-primary" type="submit" :value="$t('message.allocate')">
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="row" v-if="suggestions.length > 0">
      <div class="col">
        <div class="mb-2"><strong>{{$t('message.suggestion')}}</strong></div>
        <table class="table table-sm">
          <tr v-for="s in suggestions">
            <td class="font-mono">{{s[0]}}</td>
            <td>{{s[1]}}</td>
            <td>{{s[2].toFixed(2)}}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    i18n: {
        messages: {
            en: { message: {
                title: 'Advisor', allocation: 'Amount to allocate',
                allocate: 'allocate', suggestion: 'Suggested trades'
            } },
            ru: { message: {
                title: 'Советчик', allocation: 'Сколько разместить',
                allocate: 'разместить', suggestion: 'Советуем приобрести'
            } },
        }
    },
    computed: {
        selectedPortfolioId: function() {
            return this.$store.state.selectedPortfolioId
        },
    },
    data: function () {
      return {
        suggestions: [],
        form: {
          amountAllocate: 0,
        },
      }
    },
    methods: {
      ajaxSubmit: async function () {
        try {
          const response = await axios.get(`/portfolios/${this.selectedPortfolioId}/recommendation/${this.form.amountAllocate}`)
          this.suggestions = response.data.suggestions
        } catch(e) {
          console.log(e)
          this.isError = true
        }
      }
    }
  }
</script>
