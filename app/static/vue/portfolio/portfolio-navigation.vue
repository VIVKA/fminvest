<template>
  <div class="mb-2 portfolio-navigation">
    <div class="btn-group shadow-sm mr-2 mb-2 rounded" :class="{ 'active': pd[0] == selectedPortfolioId }"
      v-for="pd in investmentsData.portfolio_data">
      <button type="button" class="btn text-left" @click="selectPortfolio(pd[0])" >
        <small v-if="!pd[1]">{{$t('message.portfolio')}}</small>
        <small v-if="pd[1]">{{pd[1]}}</small>
        <br><span>{{pd[2]}} {{$t('message.components')}}</span>
        <!-- <span>{{pd[1]}}</span><br>
        <small style="opacity: 0.6">{{pd[2]}} {{$t('message.components')}}</small> -->
      </button>

      <button type="button" class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
      <div class="dropdown-menu dropdown-menu-right">
        <a class="dropdown-item" v-on:click="selectPortfolio(pd[0])" href="#">{{$t('message.select')}}</a>
        <div class="dropdown-divider"></div>
        <a class="dropdown-item" v-on:click="duplicatePortfolio(pd[0])" href="#">{{$t('message.duplicate')}}</a>
        <a class="dropdown-item text-danger" v-on:click.prevent="deletePortfolio(pd[0])" href="#">{{$t('message.delete')}}</a>
      </div>
    </div>

    <a class="btn btn-new shadow-sm mr-2 mb-2" href="#" v-on:click.prevent="createPortfolio()">
      <strong>+</strong>
    </a>
  </div>
</template>

<script>
  module.exports = {
    i18n: {
        messages: {
            en: { message: {
                portfolio: 'portfolio', select: 'select',
                duplicate: 'duplicate', delete: 'delete',
                confirmDeletion: 'Confirm portfolio deletion?',
                components: 'components',
            } },
            ru: { message: {
                portfolio: 'портфель', select: 'выбрать',
                duplicate: 'дублировать', delete: 'удалить',
                confirmDeletion: 'Подтвердить удаление портфеля?',
                components: 'компонент',
            } },
        }
    },
    computed: {
      investmentsData: function() {
        return this.$store.state.investmentsData
      },
      selectedPortfolioId: function() {
        return this.$store.state.selectedPortfolioId
      },
    },
    methods: {
      selectPortfolio: async function(id) {
        this.$store.dispatch('selectPortfolio', id)
      },
      createPortfolio: async function() {
        this.$store.dispatch('createPortfolio')
      },
      duplicatePortfolio: async function(id) {
        this.$store.dispatch('duplicatePortfolio', id)
      },
      deletePortfolio: async function(id) {
        if(!confirm(this.$t('message.confirmDeletion'))){ return }
        this.$store.dispatch('deletePortfolio', id)
      },
    },
  }
</script>

<style>
  .portfolio-navigation .btn-group.active {
    background: white;
  }

  .portfolio-navigation .btn-group.active .btn {
    background: goldenrod !important;
    color: white !important;
  }

  .portfolio-navigation .btn-group.active .btn:hover {
    opacity: 0.8;
    color: white;
  }

  .portfolio-navigation .btn-group .btn:focus {
    outline: none;
    box-shadow: none;
  }

  .theme-light .portfolio-navigation .btn {
    background: white;
    color: inherit;
  }

  .theme-dark .portfolio-navigation .btn {
    background: #3c3836;
    color: inherit;
  }

  .portfolio-navigation .btn:hover {
    color: goldenrod;
  }

  .portfolio-navigation .btn-new:hover {
    color: goldenrod;
  }
</style>
