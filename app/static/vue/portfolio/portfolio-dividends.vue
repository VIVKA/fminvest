<template>
    <div v-bind:class="{ 'loading': !dividendsData }" class="ui-block p-3 shadow-sm portfolio-dividends mb-4 rounded">
        <div class="row mb-3">
            <div class="col">
                <h4 class="text-secondary">{{$t('message.title')}}</h4>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col">
                <div class="chart-container hide-when-loading">
                    <svg class="chart dividends-chart"></svg>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col content scrolling-container hide-when-loading">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>{{$t('message.date')}}</th>
                            <th>{{$t('message.ticker')}}</th>
                            <th class="text-right">{{$t('message.amount')}}</th>
                            <th class="text-right">{{$t('message.dividend')}}</th>
                            <th class="text-right">{{$t('message.gross')}}</th>
                            <!-- <th class="text-right">after tax</th> -->
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="expense" v-for="trade in dividendsData">
                            <td>{{ simpleInterval(trade[0]) }}</td>
                            <td class="font-mono">{{ trade[1] }}</td>
                            <td class="text-right">{{ trade[2] }}</td>
                            <td class="text-right">{{ formatCurrency(trade[3], trade[5]) }}</td>
                            <td class="text-right">{{ formatCurrency(trade[4], trade[5]) }}</td>
                            <!-- <td class="text-right">{{ (trade[4] * 0.85).toFixed(2) }}</td> -->
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
                    date: 'date', ticker: 'ticker', dividend: 'dividend',
                    amount: 'amount', gross: 'gross', title: 'Dividend income',
                } },
                ru: { message: {
                    date: 'дата', ticker: 'тикер', dividend: 'дивиденд',
                    amount: 'кол-во', gross: 'брутто', title: 'Дивидендный доход',
                } },
            }
        },
        computed: {
            dividendsData: function() {
                return this.$store.state.dividendsData
            },
        },
        methods: {
            makeDividendsChart: function() {
                const container = d3.select('.portfolio-dividends .chart-container').node().getBoundingClientRect()

                const margin = {top: 0, right: 0, bottom: 30, left: 0};
                const width = 720 - margin.left - margin.right;
                const height = 260 - margin.top - margin.bottom;

                const today = new Date()
                const dateFrom = d3.timeMonth.offset(today, -13)
                const dateTo = d3.timeMonth.offset(today, 4)

                let plot_data = this.dividendsData
                plot_data = plot_data.filter(function(v) {
                    const c = new Date(d3.isoParse(v[0]))
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
                   .key(d => d3.timeMonth(d3.isoParse(d[0])))
                   .rollup(v => d3.sum(v, d => d[4]))
                   .entries(plot_data);

                const yMax = d3.max(nested, v => v.value)

                const y = d3.scaleLinear()
                    .domain([0, yMax*1.2])
                    .range([height, 0]);

                const yAxis = d3.axisLeft()
                    .ticks(5)
                    .scale(y)

                const target_svg = '.portfolio-dividends .dividends-chart'
                d3.select(target_svg).selectAll("*").remove()

                const chart = d3.select(target_svg)
                    .attr("preserveAspectRatio", "xMinYMin meet")
                    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
                    .append('g')
                    .attr('transform', `translate(${margin.left}, ${margin.top})`);

                const monthly_mean = d3.format(".3s")(d3.mean(nested, d => d.value))

                chart.append("g")
                    .attr("class", "axis-x")
                    .attr("transform", `translate(0, ${height})`)
                    .call(xAxis);

                bar = chart.append("g")
                    .selectAll('g')
                    .data(nested)
                    .enter()

                bar.append("rect")
                    .style("fill", "goldenrod")
                    .attr("width", width/100)
                    .attr("x", function(d) { return x(d3.isoParse(d.key)); })
                    .attr("y", function(d) { return y(d.value); })
                    .attr("height", function(d) { return height - y(d.value); });

                bar.append("text")
                    .attr("fill", "grey")
                    .attr("x", d => x(d3.isoParse(d.key)))
                    .attr("y", d => y(d.value))
                    .attr("dy", -10)
                    .style("text-anchor", "start")
                    .text(d => `${d3.format("d")(d.value)}`);

                chart.append("line")
                    .attr("x1", function(d) { return x(today); })
                    .attr("y1", "0")
                    .attr("x2", function(d) { return x(today); })
                    .attr("y2", height)
                    .attr("stroke-width", "2px")
                    .attr("stroke", "wheat")

                chart.append("text")
                    .attr("x", function(d) { return x(today); })
                    .attr("y", height/2+10)
                    .attr("fill", "wheat")
                    .style("text-anchor", "start")
                    .style("font-size", "1.4rem")
                    .text(`➡ ~${monthly_mean}/m`)
            },
        },
        watch: {
          dividendsData: async function() {
            if(this.dividendsData){
              this.makeDividendsChart()
            }
          },
        }
    }
</script>

<style>
    .dividends-chart text {
        font-size: 0.8rem;
    }

    .dividends-chart .axis-x {
        text-anchor: start;
    }

    .dividends-chart .axis-x line, .dividends-chart .axis-x path {
        opacity: 0.1;
    }

    .dividends-chart .axis-x text {
        opacity: 0.6;
    }

    .dividends-chart .axis-y line, .dividends-chart .axis-y path {
        opacity: 0.1;
    }

    .dividends-chart .axis-y text {
        opacity: 0.6;
    }

    .dividends-chart .axis-x .domain {
        opacity: 1;
        color: goldenrod;
        stroke-width: 2px;
    }

    .portfolio-dividends table thead th {
        border-top: 0;
    }

    .portfolio-dividends.loading {
        opacity: 0.5;
    }

    .portfolio-dividends.loading .hide-when-loading {
        opacity: 0;
    }
</style>
