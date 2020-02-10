<!--
<template>
  <div class="ui-block p-3 shadow-sm market-clock mb-4 rounded">
    <div class="row">
        <div class="col">
            <h5 class="text-secondary">{{currentTime}}</h5>
            <div class="text-secondary">{{ruExchangeStatus}}</div>
            <div class="text-secondary">{{usExchangeStatus}}</div>
        </div>
    </div>
  </div>
</template>
 -->

<template>
  <div class="">
    <div class="row">
        <div class="col mb-2" style="opacity: 0.6">
            <span class="mr-3 text-nowrap">{{currentTime}}</span>
            <span class="mr-3 text-nowrap">{{ruExchangeStatus}}</span>
            <span class="mr-3 text-nowrap">{{usExchangeStatus}}</span>
        </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    props: ['portfolioId'],
    i18n: {
        messages: {
            en: { message: {
              willOpen: '{country} will open in {hours}h {minutes}m',
              willClose: '{country} will close in {hours}h {minutes}m',
              hasClosed: '{country} closed {hours}h {minutes}m ago',
              isHoliday: '{country} holiday 😴',
              isWeekend: '{country} weekend 😴',
            } },
            ru: { message: {
              willOpen: '{country} откроется через {hours}ч {minutes}м',
              willClose: '{country} закроется через {hours}ч {minutes}м',
              hasClosed: '{country} закрылась {hours}ч {minutes}м назад',
              isHoliday: '{country} праздник 😴',
              isWeekend: '{country} выходной 😴',
            } },
        }
    },
    data: function () {
      return {
        time: null,
      }
    },
    computed: {
      usExchangeStatus: function() {
        if(!this.time){ return }

        exchange_data = {
          country: '🇺🇸',
          tz: 'America/New_York',
          start: [9, 30],
          end: [16, 0],
          holidays: [ // 2019
            '2019-01-01', '2019-01-21', '2019-02-18',
            '2019-04-19', '2019-05-27', '2019-07-04',
            '2019-09-02', '2019-11-28', '2019-12-25',
            // '2019-11-29', '2019-12-24', '2019-07-03', half-days
          ]
        }
        return this.getCurrentClockMessage(this.time, exchange_data)
      },
      ruExchangeStatus: function() {
        if(!this.time){ return }

        exchange_data = {
          country: '🇷🇺',
          tz: 'Europe/Moscow',
          start: [9, 30],
          end: [19, 0],
          holidays: [ // 2019
            '2019-01-01', '2019-01-02', '2019-01-05',
            '2019-01-06', '2019-01-07', '2019-02-23',
            '2019-02-24', '2019-03-08', '2019-03-09',
            '2019-03-10', '2019-05-01', '2019-05-09',
            '2019-06-12', '2019-11-04',
          ]
        }
        return this.getCurrentClockMessage(this.time, exchange_data)
      },
      currentTime: function() {
        return this.time && this.time.toLocaleString()
      }
    },
    methods: {
      isHoliday: function(moment_date, holidays) {
        if (holidays.includes(moment_date.format('YYYY-MM-DD'))) {
          return true
        }
        return false
      },
      isWeekend: function(moment_date) {
        if ([6,0].includes(moment_date.day())) {
          return true
        }
        return false
      },
      isOffDay: function(moment_date, holidays) {
        return this.isHoliday(moment_date, holidays) || this.isWeekend(moment_date)
      },
      getCurrentClockMessage: function(today, exchange_data) {
        const moment_today = moment(today).tz(exchange_data.tz)
        const start = moment.tz(exchange_data.tz)
          .hours(exchange_data.start[0])
          .minutes(exchange_data.start[1])
          .seconds(0)

        const end = moment.tz(exchange_data.tz)
          .hours(exchange_data.end[0])
          .minutes(exchange_data.end[1])
          .seconds(0)

        const yesterday = moment_today.clone().subtract(1, "days")
        const tomorrow = moment_today.clone().add(1, "days")
        const closedYesterday = this.isOffDay(yesterday, exchange_data.holidays)
        const closedTomorrow = this.isOffDay(tomorrow, exchange_data.holidays)

        // holiday
        if (this.isHoliday(moment_today, exchange_data.holidays)){
          return this.$t('message.isHoliday', {
            country: exchange_data.country
          })
        }

        // weekend
        if (this.isWeekend(moment_today)) {
          return this.$t('message.isWeekend', {
            country: exchange_data.country
          })
        }

        // will close
        if (moment_today >= start && moment_today <= end) {
          const msec = end - moment_today
          const mins = Math.floor(msec / 60000)
          const hrs = Math.floor(mins / 60)
          return this.$t('message.willClose', {
             country: exchange_data.country,
             hours: hrs,
             minutes: d3.format("0>2")(mins % 60)
          })
        }

        // will open
        if (moment_today < start) {
          const msec = start - moment_today
          const mins = Math.floor(msec / 60000)
          const hrs = Math.floor(mins / 60)
          return this.$t('message.willOpen', {
             country: exchange_data.country,
             hours: hrs,
             minutes: d3.format("0>2")(mins % 60)
          })
        }

        // has closed
        if (moment_today > end) {
          const msec = moment_today - end
          const mins = Math.floor(msec / 60000)
          const hrs = Math.floor(mins / 60)
          return this.$t('message.hasClosed', {
             country: exchange_data.country,
             hours: hrs,
             minutes: d3.format("0>2")(mins % 60)
          })
        }
      },
      update: function() {
        this.time = new Date()
      }
    },
    mounted: function() {
      this.update()
      this.interval = setInterval(this.update, 1000)
    }
  }
</script>
