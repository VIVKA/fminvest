<template>
  <div v-bind:class="{ 'loading': !portfolioData }" class="ui-block p-3 shadow-sm portfolio-contents mb-4 rounded">
    <div v-if="settings">
      <div class="row">
        <div class="col">
          <div v-if="false && portfolioName" class="row">
            <div class="col">
              <h4>{{portfolioName}}</h4>
            </div>
          </div>
          <div class="row mb-3 portfolio-status">
            <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_day_change_tooltip')">
                {{$t('message.portfolio_day_change')}}
              </small><br>
              <h5 class="hide-when-loading" v-bind:class="{ 'text-danger': portfolioData.ch < 0, 'text-success': portfolioData.ch > 0, }">
                {{d3.format("+.2f")(portfolioData.ch)}}%
              </h5>
            </div>
           <!--  <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_value_tooltip')">
                {{$t('message.portfolio_value')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{formatCurrency(portfolioData.tv)}}
              </h5>
            </div> -->
            <div class="col">
              <small class="text-secondary" style="font-size: 60%">
                {{$t('message.portfolio_capital_gain')}}
              </small><br>
              <h5 class="hide-when-loading" v-bind:class="{ 'text-danger': portfolioData.tcg < 0, 'text-success': portfolioData.tcg > 0, }">
                {{d3.format(".2f")(portfolioData.tcg)}}
              </h5>
            </div>
            <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_expected_dividend_tooltip')">
                {{$t('message.portfolio_expected_dividend')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{formatCurrency(portfolioData.tv*portfolioData.y)}}
              </h5>
            </div>
           <!--  <div class="col">
              <small class="text-secondary" style="font-size: 60%">
                {{$t('message.portfolio_dividends')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{d3.format(".2f")(portfolioData.td)}}
              </h5>
            </div> -->
            <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_return_tooltip')">
                {{$t('message.portfolio_return')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{ (portfolioData.r*100).toFixed(1) }}
                <small class="text-secondary" style="font-size: 50%">
                  ({{ (portfolioData.or*100).toFixed(1) }})
                </small>
              </h5>
              <!-- <small>
                1: {{ (portfolioData.rs[0]*100).toFixed(1) }},
                3: {{ (portfolioData.rs[1]*100).toFixed(1) }},
                5: {{ (portfolioData.rs[2]*100).toFixed(1) }}
              </small> -->
            </div>
            <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_volatility_tooltip')">
                {{$t('message.portfolio_volatility')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{ (portfolioData.d*100).toFixed(1) }}
                <small class="text-secondary" style="font-size: 50%">
                  ({{ (portfolioData.od*100).toFixed(1) }})
                </small>
              </h5>
              <!-- <small>
                1: {{ (portfolioData.ds[0]*100).toFixed(1) }},
                3: {{ (portfolioData.ds[1]*100).toFixed(1) }},
                5: {{ (portfolioData.ds[2]*100).toFixed(1) }}
              </small> -->
            </div>
            <div class="col">
              <small class="text-secondary" style="font-size: 60%" data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.portfolio_expected_yield_tooltip')">
                {{$t('message.portfolio_expected_yield')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{ (portfolioData.y*100).toFixed(1) }}
                <small class="text-secondary" style="font-size: 50%">
                  ({{ (portfolioData.oy*100).toFixed(1) }})
                </small>
              </h5>
              <!-- <small>
                1: {{ (portfolioData.ys[0]*100).toFixed(1) }},
                3: {{ (portfolioData.ys[1]*100).toFixed(1) }},
                5: {{ (portfolioData.ys[2]*100).toFixed(1) }},
              </small> -->
            </div>
            <div class="col">
              <small class="text-secondary" style="font-size: 60%">
                {{$t('message.portfolio_utility')}}
              </small><br>
              <h5 class="hide-when-loading">
                {{ (portfolioData.u*100).toFixed(1) }}
                <small class="text-secondary" style="font-size: 50%">
                  ({{ (portfolioData.ou*100).toFixed(1) }})
                </small>
              </h5>
            </div>
            <!-- <div class="col">
              <small class="text-secondary" style="font-size: 70%">
                CURRENCY
              </small><br>
              <h4>₽ $ €</h4>
            </div> -->
          </div>
        </div>
        <div class="col-auto">
          <a href="#" @click="toggleSettings">
            <svg class="settings-gear" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"><path d="M12 18c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3zm0-9c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3zm0-9c1.657 0 3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 1.343-3 3-3z"/></svg>
          </a>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col">
          <ul class="nav nav-tabs mb-2 portfolio-tabs">
            <li class="nav-item">
              <a class="nav-link" v-bind:class="{ 'active': selectedPortfolioPeriod == 'ALL' }" v-on:click.prevent="selectPeriod('ALL')" href="#">{{$t('message.period_ALL')}}</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" v-bind:class="{ 'active': selectedPortfolioPeriod == 'YTD' }" v-on:click.prevent="selectPeriod('YTD')" href="#">{{$t('message.period_YTD')}}</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col">
          <div class="chart-container hide-when-loading">
            <svg class="chart red portfolio-chart"></svg>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col hide-when-loading scrolling-container">
          <table class="table table-sm">
            <thead>
              <tr>
                <th scope="col">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.name_tooltip')">{{$t('message.name')}}</span>
                </th>
                <th scope="col" class="text-right">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.change_tooltip')">{{$t('message.change')}}</span>
                </th>
                <th scope="col" class="text-right">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.price_tooltip')">{{$t('message.price')}}</span>
                </th>
                <th scope="col" class="text-right">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.amount_tooltip')">{{$t('message.amount')}}</span>
                </th>
                <th scope="col" class="text-right">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.value_tooltip')">{{$t('message.value')}}</span>
                </th>
                <th scope="col" class="text-right"></th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.weight_tooltip')">w %</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell"><!-- wΔ % --></th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.return_tooltip')">r %</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.sigma_tooltip')">σ %</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.yield_tooltip')">y %</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.capital_gain_tooltip')">{{$t('message.capital_gain')}}</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.dividends_tooltip')">{{$t('message.dividends')}}</span>
                </th>
                <th scope="col" class="text-right d-none d-sm-table-cell">
                  <span data-toggle="tooltip" data-placement="top" :data-original-title="$t('message.real_return_tooltip')">{{$t('message.real_return')}}</span>
                </th>

                <!-- <th scope="col" class="text-right d-none d-sm-table-cell">{{$t('message.updated')}}</th> -->
                <th scope="col" class="d-none d-sm-table-cell"></th>
              </tr>
            </thead>
            <tbody >
              <tr class="portfolio-totals">
                <td class="text-left">
                  <span style="opacity: 0.5">&sum;</span>
                </td>
                <td class="text-right">
                  <span v-bind:class="{ 'text-danger': portfolioData.ch < 0, 'text-success': portfolioData.ch > 0 }">
                    {{d3.format("+.2f")(portfolioData.ch)}}
                  </span>
                </td>
                <td colspan="2"></td>
                <td class="text-right">
                  {{formatCurrency(portfolioData.tv)}}
                </td>
                <td colspan="3"></td>
                <td class="text-right">
                  {{ (portfolioData.r*100).toFixed(1) }}<br>
                </td>
                <td class="text-right">
                  {{ (portfolioData.d*100).toFixed(1) }}<br>
                </td>
                <td class="text-right">
                  {{ (portfolioData.y*100).toFixed(1) }}<br>
                </td>
                <td class="text-right">
                  <span v-bind:class="{ 'text-danger': portfolioData.tcg < 0, 'text-success': portfolioData.tcg > 0 }">
                    {{d3.format(".2f")(portfolioData.tcg)}}
                  </span>
                </td>
                <td class="text-right">
                  {{d3.format(".2f")(portfolioData.td)}}
                </td>
                <td class="text-right">
                  <span v-bind:class="{ 'text-danger': (portfolioData.tcg+portfolioData.td) < 0, 'text-success': (portfolioData.tcg+portfolioData.td) > 0 }">
                    {{d3.format(".2f")(portfolioData.tcg+portfolioData.td)}}
                  </span>
                </td>
                <td></td>
              </tr>
           <!--  </tbody>
            <tbody> -->
              <tr is="portfolio-asset" v-for="asset_data in assetData" :asset-data="asset_data" :portfolio-id="selectedPortfolioId" :key="asset_data.asset_id"></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  module.exports = {
    i18n: {
        messages: {
            en: { message: {
                title: 'Portfolio',

                period_YTD: 'YTD',
                period_ALL: 'All time',

                portfolio_capital_gain: 'TOTAL CAPITAL GAIN',
                portfolio_dividends: 'TOTAL DIVIDENDS RECEIVED',
                portfolio_day_change: 'Δ LAST DAY',
                portfolio_value: 'TOTAL VALUE',
                portfolio_expected_dividend: 'ANNUAL DIVIDEND',
                portfolio_return: 'RETURN, %',
                portfolio_volatility: 'VOLATILITY, %',
                portfolio_expected_yield: 'DIVIDEND YIELD, %',
                portfolio_utility: 'UTILITY',

                portfolio_day_change_tooltip: 'Portfolio value change % since the last trading day',
                portfolio_value_tooltip: 'Current portfolio market value',
                portfolio_expected_dividend_tooltip: 'Projected dividend income',
                portfolio_return_tooltip: 'Portfolio expected yearly return %, calculated over 36-month moving window',
                portfolio_volatility_tooltip: 'Portfolio expected volatility %, calculated over 36-month moving window',
                portfolio_expected_yield_tooltip: 'Portfolio expected dividend yield %, calculated over past 3 full years',
                portfolio_utility_tooltip: '',

                name: 'name', change: 'Δ %',
                price: 'price', amount: 'amount', value: 'value',
                updated: 'updated',
                capital_gain: 'capital gain',
                dividends: 'dividends',
                real_return: 'return',

                name_tooltip: 'Country, ticker name',
                change_tooltip: 'Price change % since the last trading day',
                price_tooltip: 'Current price in original currency',
                amount_tooltip: 'Amount held in portfolio',
                value_tooltip: 'Total current market value in original currency',
                weight_tooltip: 'Position weight, % of total portfolio value',
                return_tooltip: 'Average annual return %, calculated over 36-month moving window',
                sigma_tooltip: 'Average annual volatility %, calculated over 36-month moving window',
                yield_tooltip: 'Average annual dividend yield %, calculated over past 3 full years',
                capital_gain_tooltip: 'Capital gain',
                dividends_tooltip: 'Dividends',
                real_return_tooltip: 'Return',
            } },
            ru: { message: {
                title: 'Портфель',

                period_YTD: 'C 1 янв',
                period_ALL: 'C начала',

                portfolio_capital_gain: 'ПРИРОСТ КАПИТАЛА',
                portfolio_dividends: 'СОВОКУПНЫЕ ДИВИДЕНДЫ',
                portfolio_day_change: 'Δ ПОСЛЕДНИЙ ДЕНЬ',
                portfolio_value: 'СОВОКУПНАЯ СТОИМОСТЬ',
                portfolio_expected_dividend: 'ГОДОВОЙ ДИВИДЕНД',
                portfolio_return: 'ДОХОДНОСТЬ, %',
                portfolio_volatility: 'ВОЛАТИЛЬНОСТЬ, %',
                portfolio_expected_yield: 'ДИВ. ДОХОДНОСТЬ, %',
                portfolio_utility: 'ПОЛЕЗНОСТЬ',

                portfolio_day_change_tooltip: 'Изменение стоимости портфелся с момента закрытия последнего торгового дня',
                portfolio_value_tooltip: 'Совокупная рыночная стоимость портфеля',
                portfolio_expected_dividend_tooltip: 'Ожидаемый годовой объем дивидендных поступлений',
                portfolio_return_tooltip: 'Ожидаемая годовая доходность в %, рассчитанная за последние 36 месяцев',
                portfolio_volatility_tooltip: 'Ожидаемая волатильность в %, рассчитанная за последние 36 месяцев',
                portfolio_expected_yield_tooltip: 'Ожидаемая дивидендная доходность в %, рассчитанная за 3 последних полных года',
                portfolio_utility_tooltip: '',

                name: 'название', change: 'Δ %',
                price: 'цена', amount: 'кол-во', value: 'стоимость',
                updated: 'обновлено',
                capital_gain: 'прирост капитала',
                dividends: 'дивиденды',
                real_return: 'доходность',

                name_tooltip: 'Страна, тикер',
                change_tooltip: '% изменения цены с момента закрытия последнего торгового дня',
                price_tooltip: 'Текущая рыночная цена в оригинальной валюте',
                amount_tooltip: 'Количество в портфеле',
                value_tooltip: 'Совокупная рыночная стоимость позиции в оригинальной волюте',
                weight_tooltip: 'Вес позиции в портфеле, % от совокупной рыночной стоимости всего портфеля',
                return_tooltip: 'Среднегодовая доходность в %, рассчитанная за последние 36 месяцев',
                sigma_tooltip: 'Среднегодовая волатильнось в %, рассчитанная за последние 36 месяцев',
                yield_tooltip: 'Среднегодовая дивидендная доходность в %, рассчитанная за 3 последних полных года',
                capital_gain_tooltip: 'Прирост капитала',
                dividends_tooltip: 'Дивиденды',
                real_return_tooltip: 'Доходность',
            } },
        }
    },
    computed: {
        selectedPortfolioPeriod: function() {
            return this.$store.state.selectedPortfolioPeriod
        },
        selectedPortfolioId: function() {
            return this.$store.state.selectedPortfolioId
        },
        portfolioData: function() {
            return this.$store.state.portfolioData
        },
        assetData: function() {
            return this.$store.state.assetData
        },
        benchmarkData: function() {
            return this.$store.state.benchmarkData
        },
        portfolioName: function() {
          if(this.$store.state.portfolioData && this.$store.state.portfolioData.name) {
            return this.$store.state.portfolioData.name
          }

          return false
        },
    },
    data: function() {
      return {
        settings: true,
      }
    },
    methods: {
      toggleSettings: function() {
        console.log('12312312')
      },
      selectPeriod: async function(period) {
        await this.$store.dispatch('selectPortfolioPeriod', period)
      },
      showPortfolioChart: function() {
        const container = d3.select('.portfolio-contents .chart-container').node().getBoundingClientRect()

        const margin = {top: 10, right: 0, bottom: 30, left: 30};
        const width = container.width - margin.left - margin.right;
        const height = 260 - margin.top - margin.bottom;

        const today = new Date()
        const dateFrom = d3.timeMonth.offset(today, -13)
        const dateTo = d3.timeMonth.offset(today, 4)

        let plot_data = this.benchmarkData

        // const _width = 1000
        // let nan = 0;
        // let yyy = d3.scaleLog().domain([1, 3000]).range([1,400]);
        // let margin = {top: 20, right: 30, bottom: 30, left: 40},
        //     width = _width, // - margin.left - margin.right,
        //     height = yyy(_width)+100; // - margin.top - margin.bottom;

        let first_date
        if (plot_data.portfolio.length > 0){
          first_date = d3.isoParse(plot_data.portfolio[0][0])
        } else {
          first_date = d3.isoParse(plot_data.voo[0][0])
        }

        const x = d3.scaleTime()
            .domain([
                d3.isoParse(d3.timeMonth.offset(first_date, 0)),
                d3.isoParse(d3.timeMonth.offset(today, 4)),
            ])
            .range([0, width]);

        // let bw = width / d3.scaleTime()
        //     .domain([
        //         d3.isoParse('2018-01-01'),
        //         d3.isoParse('2020-01-01'),
        //     ])
        //     .ticks(d3.timeDay.every(1))
        //     .length;

        let xAxis = d3.axisBottom()
            // .ticks(d3.timeMonth.every(1))
            .tickSizeOuter(0)
            .tickSizeInner(6)
            .tickPadding(10)
            .tickFormat(function(date){
              if (d3.timeYear(date) < date) {
                return d3.timeFormat('%b')(date);
              } else {
                return d3.timeFormat('%Y')(date);
              }
            })
            .scale(x);

        const target_svg = '.portfolio-contents .portfolio-chart'
        d3.select(target_svg).selectAll("*").remove()

        const svg = d3.select(target_svg)
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)

        svg.append("defs")
          .append("clipPath")
          .attr("id", "portfolio-chart-clip")
          .append("rect")
          .attr("x", 0)
          .attr("y", 0)
          .attr("width", width)
          .attr("height", height)

        // NB OFFSETTED
        // const bisectDate = d3.bisector(function(d, v) {
        //   // console.log('-',d[0], d3.isoParse(d[0]))
        //   // console.log(d3.isoParse(d[0]))
        //   return d3.isoParse(d[0]) < d3.isoParse(v);
        // })
        const bisectDate = d3.bisector(function(d) {
          return d3.isoParse(d[0])
        })

        const that = this
        svg.on("touchmove mousemove", function() {
            const __date = x.invert(d3.mouse(this)[0]-margin.left)
            const p = bisectDate.left(plot_data.portfolio, __date)
            const vo = bisectDate.left(plot_data.voo, __date)
            const im = bisectDate.left(plot_data.imoex, __date)
            const vt = bisectDate.left(plot_data.vt, __date)

            // console.log(
            //   plot_data.portfolio[p][1],
            //   plot_data.voo[vo][1],
            //   plot_data.imoex[im][1],
            //   plot_data.vt[vt][1],
            // )

            chart.selectAll("line.chart-tooltip, circle.chart-marker").remove()

            chart.append("line")
              .attr("class", "chart-tooltip")
              .attr("x1", function(d) { return x(__date) })
              .attr("y1", "0")
              .attr("x2", function(d) { return x(__date) })
              .attr("y2", height)
              .attr("stroke-width", "1px")
              .attr("stroke-dasharray", "5 2")
              .attr("stroke", "wheat")

            chart.append("circle")
              .attr("class", "chart-marker")
              .attr("cx", function (d) { return x(__date) })
              .attr("cy", "0" )
              .attr("r", "5px")
              .style("fill", "wheat")
          })

        const chart = svg.append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        chart.append("g")
            .attr("class", "axis axis-x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        let abMax = d3.max([
          d3.max(plot_data.voo, function(d) { return d[1]; }),
          d3.max(plot_data.imoex, function(d) { return d[1]; }),
          d3.max(plot_data.portfolio, function(d) { return d[1]; }),
          // d3.max(plot_data.target, function(d) { return d[1]; }),
        ])
        let abMin = d3.min([
          d3.min(plot_data.voo, function(d) { return d[1]; }),
          d3.min(plot_data.imoex, function(d) { return d[1]; }),
          d3.min(plot_data.portfolio, function(d) { return d[1]; }),
          // d3.min(plot_data.target, function(d) { return d[1]; }),
        ])

        abMax = (Math.round(abMax * 20.0) / 20.0).toFixed(2)
        abMin = (Math.round(abMin * 20.0) / 20.0).toFixed(2)

        let y = d3.scaleLinear()
            .domain([
              abMin-(1.0+0.1),
              abMax-(1.0-0.1),
            ])
            .range([height, 0]);

        let yAxis = d3.axisLeft()
            .ticks(5)
            .tickSizeOuter(0)
            .tickSizeInner(0)
            .tickPadding(5)
            .tickFormat(d3.format(".0%"))
            // .tickValues([-0.1,0,0.1,0.2])
            .scale(y);

        let yAxisH = d3.axisLeft()
            .ticks(5)
            .tickSizeOuter(0)
            .tickSizeInner(-width)
            // .tickValues([-0.1,0,0.1,0.2])
            .scale(y)

        chart.append("g")
            .attr("class", "axis axis-y")
            .call(yAxis);

        chart.append("g")
            .attr("class", "axis axis-y2")
            .call(yAxisH);

        let line = d3.line()
           .x(function(d) { return x(d3.isoParse(d[0])); })
           .y(function(d) { return y(d[1]-1); })

        chart.selectAll("g.benchmark").remove()

        const last_voo = plot_data.voo[plot_data.voo.length-1].slice()
        const last_vt = plot_data.vt[plot_data.vt.length-1].slice()
        const last_imoex = plot_data.imoex[plot_data.imoex.length-1].slice()

        last_voo[0] = last_vt[0] = last_imoex[0] = today

        const draw_area = chart.append("g").attr('clip-path', 'url(#portfolio-chart-clip)')

        draw_area.append("g").attr("class", "benchmark")
          .append('path')
          .datum(plot_data.voo.concat([last_voo]))
          .attr("d", line);

        draw_area.append("g").attr("class", "benchmark world-index")
          .append('path')
          .datum(plot_data.vt.concat([last_vt]))
          .attr("d", line);

        draw_area.append("g").attr("class", "benchmark")
          .append('path')
          .datum(plot_data.imoex.concat([last_imoex]))
          .attr("d", line);

        draw_area.append("text")
          .datum(last_voo)
          .attr("class", "world-index-label")
          .attr("text-anchor", "start")
          .attr("x", function(d) { return 5+x(today); })
          .attr("y", function(d) { return 3+y(d[1]-1); })
          .text(function(d) {return 's&p500 '+((d[1]-1)*100).toFixed(2)+'%'});

        draw_area.append("text")
          .datum(last_vt)
          .attr("fill", "goldenrod")
          .attr("text-anchor", "start")
          .attr("x", function(d) { return 5+x(today); })
          .attr("y", function(d) { return 3+y(d[1]-1); })
          .text(function(d) {return 'world '+((d[1]-1)*100).toFixed(2)+'%'});

        draw_area.append("text")
          .datum(last_imoex)
          .attr("class", "world-index-label")
          .attr("text-anchor", "start")
          .attr("x", function(d) { return 5+x(today); })
          .attr("y", function(d) { return 3+y(d[1]-1); })
          .text(function(d) {return 'imoex '+((d[1]-1)*100).toFixed(2)+'%'});

        if (plot_data.portfolio.length > 0) {
          const last_portfolio = plot_data.portfolio[plot_data.portfolio.length-1].slice()
          // const last_target = plot_data.target[plot_data.target.length-1].slice()
          last_portfolio[0] = today
          draw_area.append("g").attr("class", "benchmark portfolio-index")
            .append('path')
            .datum(plot_data.portfolio.concat([last_portfolio]))
            .attr("d", line);


          const capMin = d3.min(plot_data.portfolio, function(d) { return d[2]; })
          const capMax = d3.max(plot_data.portfolio, function(d) { return d[2]; })

          const yCap = d3.scaleLinear()
            .domain([capMin, capMax])
            .range([height, 0]);

          draw_area.append("g")
            .append("path")
            .attr("class", "capital-index")
            .datum(plot_data.portfolio)
            .attr("d", d3.area()
              .x(function(d) { return x(d3.isoParse(d[0])); })
              .y0(yCap(0))
              .y1(function(d) { return yCap(d[2]) })
              )

          // draw_area.append("g").attr("class", "benchmark")
          //   .append('path')
          //   .datum(plot_data.target.concat([last_target]))
          //   .attr("fill", "none")
          //   .attr("stroke", "green")
          //   .attr("stroke-dasharray", 3)
          //   .attr("stroke-linejoin", "round")
          //   .attr("d", line);

          draw_area.append("text")
            .datum(last_portfolio)
            .attr("fill", "green")
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .attr("x", function(d) { return 5+x(today); })
            .attr("y", function(d) { return 3+y(d[1]-1); })
            .text(function(d) {return 'portfolio '+((d[1]-1)*100).toFixed(2)+'%'});
        }

        // const that = this
        // const bisectDate = d3.bisector(function(d, v) {
        //     // console.log('-',d[0], d3.isoParse(d[0]))
        //     // console.log(d3.isoParse(d[0]))
        //     return d3.isoParse(d[0]) < d3.isoParse(v);
        //   })

        // const focus = chart.append("text")
        //   .attr("x", function(d) { return 5+x(today); })
        //   .attr("y", function(d) { return height / 2; })
        //   .text('12123123')

        // const mouseMove = function() {
        //   const v = x.invert(d3.mouse(this)[0]-margin.left)
        //   const c = bisectDate.right(that.dividendsData, v)
        //   const k = c

        //   // chart.append("text")
        //   //   .datum(last_portfolio)
        //   //   .attr("fill", "green")
        //   //   .attr("text-anchor", "start")
        //   //   .attr("font-weight", "bold")
        //   //   .attr("x", function(d) { return 5+x(today); })
        //   //   .attr("y", function(d) { return height / 2; })
        //   //   .text(function(d) {return c});
        //   // focus.text(that.dividendsData[k][4]);
        // }

        // d3.select(target_svg).on("mousemove", mouseMove)

        // dividends
        // bar = draw_area.append("g")
        //   .selectAll('g')
        //   .data(this.dividendsData)
        //   .enter()

        // bar.append("line")
        //   .attr("x1", function(d) { return x(d3.isoParse(d[0])); })
        //   .attr("y1", function(d) {
        //     return height-3-Math.abs(Math.log(d[4])*2)
        //   })
        //   .attr("x2", function(d) { return x(d3.isoParse(d[0])); })
        //   .attr("y2", function(d) { return height } )
        //   .attr("stroke-width", "1px")
        //   .attr("opacity", 0.8)
        //   .attr("stroke", "goldenrod")
      },
    },
    watch: {
      benchmarkData: async function() {
        if(this.benchmarkData){
          this.showPortfolioChart()
        }
      },
    },
    mounted: function() {
      $('.portfolio-contents [data-toggle="tooltip"]').tooltip()
      window.addEventListener('resize', this.showPortfolioChart )
    },
  }
</script>

<style>
    .portfolio-contents .portfolio-totals {
      background: #daa52020;
    }

    .portfolio-contents [data-toggle="tooltip"]  {
      border-bottom: 1px dashed grey;
    }

    .portfolio-contents table thead th {
        border-top: 0;
    }

    .portfolio-contents.loading {
        opacity: 0.5;
    }

    .portfolio-contents.loading .hide-when-loading {
        opacity: 0;
    }

    .scrolling-container {
        overflow-x: scroll;
        overflow-y: hidden;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
    }

    .portfolio-chart text {
        font-size: 0.8rem;
    }

    .portfolio-chart .axis-x line, .portfolio-chart .axis-x path {
        /*opacity: 0.1;*/
        opacity: 1;
        color: goldenrod;
        stroke-width: 2px;
    }

    .portfolio-chart .axis-x text {
        opacity: 0.6;
        /*font-weight: bold;*/
    }

    .portfolio-chart .axis-x .domain {
        opacity: 1;
        color: goldenrod;
        stroke-width: 2px;
    }

    .portfolio-chart .axis-x {
        text-anchor: start;
    }

    .portfolio-chart .axis-y text {
        opacity: 0.6;
    }

    .portfolio-chart .axis-y line, .portfolio-chart .axis-y path {
        opacity: 0.1;
    }

    .portfolio-chart .axis-y .domain {
        visibility: hidden;
    }

    .portfolio-chart .axis-y2 text {
        opacity: 0.0;
    }

    .portfolio-chart .axis-y2 .domain {
        visibility: hidden;
    }

    .portfolio-chart .axis-y2 .tick line {
        opacity: 0.1;
        stroke-dasharray: 3;
    }

    .portfolio-chart .benchmark path {
      opacity: 0.4;
      fill: none;
      stroke: goldenrod;
      stroke-linejoin: round;
    }

    .portfolio-chart .world-index-label {
      opacity: 0.4;
      fill: goldenrod;
    }

    .portfolio-chart .benchmark.world-index path {
      opacity: 1;
      fill: none;
      stroke: goldenrod;
      stroke-linejoin: round;
    }

    .portfolio-chart .benchmark.portfolio-index path {
      opacity: 1;
      fill: none;
      stroke: limegreen;
      stroke: green;
      stroke-linejoin: round;
    }

    .portfolio-chart .capital-index {
      opacity: 0.1;
      fill: goldenrod;
    }

    .portfolio-status small, .portfolio-status h5  {
      white-space: nowrap;
    }

    .theme-dark .portfolio-tabs .nav-link.active {
      background: #3c3836;
      color: #d5c4a1;
      border-color: #665c54 #665c54 transparent !important;
    }

    .theme-dark .portfolio-tabs .nav-link {
      background: #3c3836;
      color: #a89984;
      border-bottom: 1px solid #665c54;
    }

    .theme-dark .portfolio-tabs .nav-link:hover {
      background: #3c3836;
      color: #d5c4a1;
      border-color: transparent;
      border-bottom: 1px solid #665c54;
    }

    .theme-dark .nav-tabs {
      border-bottom: 1px solid #665c54;
    }
</style>
