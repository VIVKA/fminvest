<template>
    <div v-bind:class="{ 'loading': !(tradesData && benchmarkData) }" class="ui-block p-3 shadow-sm portfolio-trades mb-4 rounded">
        <div class="row mb-3">
            <div class="col">
                <h4 class="text-secondary">{{$t('message.title')}}</h4>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col">
                <div class="chart-container hide-when-loading">
                    <svg class="chart trades-chart"></svg>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col content scrolling-container hide-when-loading">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>{{$t('message.date')}}</th>
                            <th>{{$t('message.action_type')}}</th>
                            <th>{{$t('message.ticker')}}</th>
                            <th class="text-right">{{$t('message.amount')}}</th>
                            <th class="text-right">{{$t('message.price')}}</th>
                            <!-- <th class="text-right">brokerage</th>
                            <th class="text-right">exch. rate</th> -->
                            <th class="text-right">{{$t('message.value')}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="expense" v-for="trade in tradesData">
                            <!-- <td>{{ trade['asset_id'] }}</td> -->
                            <td>{{ simpleInterval(trade['traded_at']) }}</td>
                            <td>{{ trade['action_type'] }}</td>
                            <td class="font-mono">{{ trade['ticker'] }}</td>
                            <td class="text-right">{{ trade['amount'] }}</td>
                            <td class="text-right">{{ formatCurrency(trade['price'], trade.country) }}</td>
                            <!-- <td class="text-right">-</td>
                            <td class="text-right">-</td> -->
                            <td class="text-right">{{ formatCurrency(trade['value'], trade.country) }}</td>
                        </tr>
                    </tbody>
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
                    date: 'date', ticker: 'ticker', amount: 'amount',
                    action_type: 'type', price: 'price', value: 'value',
                    title: 'Trade history',
                } },
                ru: { message: {
                    date: 'дата', ticker: 'тикер', amount: 'кол-во',
                    action_type: 'тип', price: 'цена', value: 'стоимость',
                    title: 'Торговая история',
                } },
            }
        },
        computed: {
            tradesData: function() {
                return this.$store.state.tradesData
            },
            benchmarkData: function() {
                return this.$store.state.benchmarkData
            },
        },
        methods: {
            makeTradesChart: function() {
                const container = d3.select('.portfolio-trades .chart-container').node().getBoundingClientRect()

                const margin = {top: 0, right: 0, bottom: 30, left: 0};
                const width = 720 - margin.left - margin.right;
                const height = 260 - margin.top - margin.bottom;

                const today = new Date()
                const dateFrom = d3.timeMonth.offset(today, -12)

                const dateTo = d3.timeMonth.offset(today, 4)

                let plot_data = this.tradesData
                plot_data = plot_data.filter(function(v) {
                    const c = new Date(d3.isoParse(v.traded_at))
                    return c > d3.timeMonth.offset(today, -13)
                })

                const x = d3.scaleTime()
                    .domain([dateFrom, dateTo])
                    .range([0, width]);

                const xAxis = d3.axisBottom()
                    .ticks(d3.timeMonth.every(1))
                    .tickSizeOuter(0)
                    .tickSizeInner(-height)
                    .tickPadding(10)
                    .tickFormat(function(date){
                      if (d3.timeYear(date) < date) {
                        return d3.timeFormat('%b')(date);
                      } else {
                        return d3.timeFormat('%Y')(date);
                      }
                    })
                    .scale(x);

                const nested = d3.nest()
                   .key(d => d3.timeWeek(d3.isoParse(d.traded_at)))
                   .rollup(v => d3.sum(v, d => d.value))
                   .entries(plot_data);

                const target_svg = '.portfolio-trades .trades-chart'
                d3.select(target_svg).selectAll("*").remove()

                const chart = d3.select(target_svg)
                    .attr("preserveAspectRatio", "xMinYMin meet")
                    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                    .append('g')
                    .attr('transform', `translate(${margin.left}, ${margin.top})`);

                chart.append("g")
                    .attr("class", "axis-x")
                    .attr("transform", `translate(0, ${height})`)
                    .call(xAxis);

                const benchmark_world = this.benchmarkData.vt
                const benchmark_us = this.benchmarkData.voo
                const benchmark_ru = this.benchmarkData.imoex

                const last_world = benchmark_world[benchmark_world.length-1]
                const last_us = benchmark_us[benchmark_us.length-1]
                const last_ru = benchmark_ru[benchmark_ru.length-1]

                let abMax = d3.max([
                  d3.max(benchmark_world, function(d) { return d[1]; }),
                  d3.max(benchmark_us, function(d) { return d[1]; }),
                  d3.max(benchmark_ru, function(d) { return d[1]; }),
                ])
                let abMin = d3.min([
                  d3.min(benchmark_world, function(d) { return d[1]; }),
                  d3.min(benchmark_us, function(d) { return d[1]; }),
                  d3.min(benchmark_ru, function(d) { return d[1]; }),
                ])

                abMax = (Math.round(abMax * 20.0) / 20.0).toFixed(2)
                abMin = (Math.round(abMin * 20.0) / 20.0).toFixed(2)

                let y = d3.scaleLinear()
                    .domain([
                      abMin-(1.0+0.15),
                      abMax-(1.0-0.15),
                    ])
                    .range([height, 0]);

                let line = d3.line()
                   .x(function(d) { return x(d3.isoParse(d[0])); })
                   .y(function(d) { return y(d[1]-1); })

                let yAxisH = d3.axisLeft()
                    .tickSizeOuter(0)
                    .tickSizeInner(-width)
                    .tickValues([-0.1,0.0,0.1])
                    .scale(y)

                chart.append("g")
                    .attr("class", "axis axis-y")
                    .call(yAxisH);

                bar = chart.append("g")
                    .selectAll('g')
                    .data(nested)
                    .enter()

                bar.append("line")
                    .attr("x1", function(d) { return x(d3.isoParse(d.key)); })
                    .attr("y1", function(d) { return height })
                    .attr("x2", function(d) { return x(d3.isoParse(d.key)); })
                    .attr("y2", function(d) { return 0 } )
                    .attr("stroke-width", "1px")
                    .attr("opacity", 0.5)
                    .attr("stroke", "green")

                chart.append("line")
                    .attr("x1", function(d) { return x(today); })
                    .attr("y1", "0")
                    .attr("x2", function(d) { return x(today); })
                    .attr("y2", height)
                    .attr("stroke-width", "2px")
                    .attr("stroke", "wheat")

                chart.append("g")
                    .attr("class", "benchmark")
                    .append('path')
                    .datum(benchmark_us)
                    .attr("d", line);

                chart.append("g")
                    .attr("class", "benchmark")
                    .append('path')
                    .datum(benchmark_ru)
                    .attr("d", line);

                chart.append("g")
                    .attr("class", "benchmark")
                    .append('path')
                    .datum(benchmark_world)
                    .attr("d", line);

                chart.append("text")
                    .datum(last_world)
                    .attr("fill", "goldenrod")
                    .attr("opacity", 0.6)
                    .attr("text-anchor", "start")
                    .attr("x", function(d) { return 5+x(today); })
                    .attr("y", function(d) { return 3+y(d[1]-1); })
                    .text(function(d) {return 'world '+((d[1]-1)*100).toFixed(2)+'%'});

                chart.append("text")
                    .datum(last_us)
                    .attr("fill", "goldenrod")
                    .attr("opacity", 0.6)
                    .attr("text-anchor", "start")
                    .attr("x", function(d) { return 5+x(today); })
                    .attr("y", function(d) { return 3+y(d[1]-1); })
                    .text(function(d) {return 's&p500 '+((d[1]-1)*100).toFixed(2)+'%'});

                chart.append("text")
                    .datum(last_ru)
                    .attr("fill", "goldenrod")
                    .attr("opacity", 0.6)
                    .attr("text-anchor", "start")
                    .attr("x", function(d) { return 5+x(today); })
                    .attr("y", function(d) { return 3+y(d[1]-1); })
                    .text(function(d) {return 'imoex '+((d[1]-1)*100).toFixed(2)+'%'});

                chart.append("text")
                    .attr("x", function(d) { return x(today); })
                    .attr("y", height/2+10)
                    .attr("fill", "wheat")
                    .style("text-anchor", "start")
                    .style("font-size", "1.4rem")
                    .text(`➡`)
            }
        },
        watch: {
          tradesData: async function() {
            if(this.tradesData && this.benchmarkData){
              // this.makeTradesChart()
            }
          },
          benchmarkData: async function() {
            if(this.tradesData && this.benchmarkData){
              // this.makeTradesChart()
            }
          },
        },
    }
</script>

<style>
    .trades-chart text {
        font-size: 0.8rem;
    }

    .trades-chart .axis-x {
        text-anchor: start;
    }

    .trades-chart .axis-x line, .trades-chart .axis-x path {
        opacity: 0.1;
    }

    .trades-chart .axis-x text {
        opacity: 0.6;
    }

    .trades-chart .axis-x .domain {
        opacity: 1;
        color: goldenrod;
        stroke-width: 2px;
    }

    .trades-chart .benchmark path {
        fill: none;
        stroke: goldenrod;
        stroke-width: 2px;
        stroke-linejoin: round;
    }

    .trades-chart .axis-y line, .trades-chart .axis-y path {
        opacity: 0.1;
    }

    .trades-chart .axis-y .domain {
        visibility: hidden;
    }

    .portfolio-trades table thead th {
        border-top: 0;
    }

    .portfolio-trades.loading {
        opacity: 0.5;
    }

    .portfolio-trades.loading .hide-when-loading {
        opacity: 0;
    }

    .portfolio-trades .axis.no-labels text, .portfolio-trades .axis.no-labels .domain {
      opacity: 0;
    }

    .portfolio-trades .axis.no-labels line {
      stroke: #333;
      opacity: 0.05;
    }
</style>
