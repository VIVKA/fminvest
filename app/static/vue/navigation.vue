<template>
  <div class="row mb-2">
    <div class="col my-auto">
      <strong class="font-mono" style="white-space: nowrap">{{$store.state.token}}</strong>
    </div>
    <div class="col my-auto text-right dropleft">
      <a class="z-top" href="#" role="button" id="dropdownMenuLink" data-offset="-5,-20" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        <svg class="settings-gear" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path d="M12 18c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3zm0-9c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3zm0-9c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3z"/></svg>
      </a>
      <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
        <span class="dropdown-header">{{$t('message.settings')}}</span>
        <div class="dropdown-item">
          <select @click.stop @change="$store.dispatch('selectTheme', t_)" v-model="t_">
            <option v-for="(v, i) in $store.state.availableThemes" :value="v">{{ v }}</option>
          </select>
        </div>
        <div class="dropdown-item">
          <select @click.stop @change="$store.dispatch('selectLocale', l_)" v-model="l_">
            <option v-for="(v, i) in $store.state.availableLocales" :value="v">{{ v }}</option>
          </select>
        </div>
        <div class="dropdown-divider"></div>
        <a class="dropdown-item" href="#"><img style="fill: red;" src="static/sign-out.svg"/> {{$t('message.sign_out')}}</a>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    props: ['token'],
    i18n: {
      messages: {
        en: {
          message: {
            budget: 'Budget', investments: 'Investments',
            settings: 'SETTINGS', sign_out: 'Sign out',
          }
        },
        ru: {
          message: {
            budget: 'Бюджет', investments: 'Инвестиции',
            settings: 'НАСТРОЙКИ', sign_out: 'Выйти',
          }
        }
      }
    },
    data: function () {
      return {
        l_: this.$store.state.locale,
        t_: this.$store.state.theme,
      }
    },
  }
</script>

<style>
  .z-top {
    z-index: 2000;
    position: relative
  }
</style>
