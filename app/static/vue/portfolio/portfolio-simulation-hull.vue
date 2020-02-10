<template>
    <div :class="{ 'loading': !portfolioData }" class="ui-block p-3 shadow-sm portfolio-simulation-hull mb-4 rounded">
        <div class="row mb-3">
            <div class="col">
                <h4 class="text-secondary">{{$t("message.title")}}</h4>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div class="chart-container hide-when-loading">
                    <svg class="chart simulation-hull-chart"></svg>
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
                    title: 'Mean-variance analysis',
                    date: 'date', ticker: 'ticker', amount: 'amount',
                    price: 'price', value: 'value',
                } },
                ru: { message: {
                    title: 'Анализ средней дисперсии',
                    date: 'дата', ticker: 'тикер', amount: 'количество',
                    price: 'цена', value: 'стоимость',
                } },
            }
        },
        computed: {
            portfolioData: function() {
                return this.$store.state.portfolioData
            },
        },
        methods: {
            makeSimulationHullChart: function() {
                const container = d3.select('.portfolio-simulation-hull .chart-container').node().getBoundingClientRect()

                const margin = {top: 0, right: 0, bottom: 30, left: 50};
                const width = 720 - margin.left - margin.right;
                const height = 260 - margin.top - margin.bottom;

                const plot_data = this.portfolioData.simulation_hull

                const xMin = d3.min(plot_data, d => d[0])
                const xMax = d3.max(plot_data, d => d[0])
                const yMin = d3.min(plot_data, d => d[1])
                const yMax = d3.max(plot_data, d => d[1])

                const x = d3.scaleLinear()
                    .domain([0, xMax*1.5])
                    .range([0, width]);

                const y = d3.scaleLinear()
                    .domain([0, yMax*1.5])
                    .range([height, 0]);

                const xAxis = d3.axisBottom()
                    .ticks(5)
                    // .tickSizeInner(-height)
                    .scale(x)

                const yAxis = d3.axisLeft()
                    .ticks(3)
                    .tickSizeInner(-width)
                    .scale(y)

                const target_svg = '.portfolio-simulation-hull .simulation-hull-chart'
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

                chart.append("g")
                    .attr("class", "axis-y")
                    .call(yAxis);

                let line = d3.line()
                    .x(d => x(d[0]))
                    .y(d => y(d[1]))
                    .curve(d3.curveCatmullRom)

                const hulldata = d3.polygonHull(plot_data)

                if (hulldata) {
                    chart.append("path")
                        .datum(hulldata)
                        .attr("class", "hull")
                        .attr("d", line);

                    const min_d = hulldata.reduce((p, c) => p[0] < c[0] ? p : c)
                    const top_r = hulldata.reduce((p, c) => p[1] > c[1] ? p : c)
                    const li = hulldata.findIndex(v => v[0] == min_d[0] && v[1] == min_d[1])
                    const ti = hulldata.findIndex(v => v[0] == top_r[0] && v[1] == top_r[1])

                    let frontier = []
                    if (ti > li) {
                        frontier = hulldata.slice(li, ti+1)
                    } else {
                        frontier = frontier.concat(hulldata.slice(li))
                        frontier = frontier.concat(hulldata.slice(0, ti+1))
                    }

                    chart.append("path")
                        .datum(frontier)
                        .attr("class", "frontier")
                        .attr("d", line);

                    chart.append("circle")
                        .attr("fill", "green")
                        .attr("stroke-width", 0)
                        .attr("r", 3.5)
                        .attr("cx", x(this.portfolioData.d) )
                        .attr("cy", y(this.portfolioData.r) )

                    chart.append("circle")
                        .attr("fill", "goldenrod")
                        .attr("stroke-width", 0)
                        .attr("r", 3.5)
                        .attr("cx", x(this.portfolioData.od) )
                        .attr("cy", y(this.portfolioData.or) )
                }
            }
        },
        watch: {
            portfolioData: async function() {
                if(this.portfolioData){
                    this.makeSimulationHullChart()
                }
            }
        }
    }
</script>

<style>
    .theme-light .simulation-hull-chart .hull {
        fill: wheat;
        stroke: none;
        stroke-width: 0;
        opacity: 0.3;
        stroke-linejoin: round;
    }

    .theme-dark .simulation-hull-chart .hull {
        fill: wheat;
        stroke: none;
        stroke-width: 0;
        opacity: 0.1;
        stroke-linejoin: round;
    }

    .simulation-hull-chart .frontier {
        fill: none;
        stroke: goldenrod;
        stroke-width: 2px;
        stroke-dasharray: 10;
        stroke-linejoin: round;
    }

    .simulation-hull-chart text {
        font-size: 1rem;
    }

    .simulation-hull-chart .axis-x line, .simulation-hull-chart .axis-x path {
        opacity: 0.1;
    }

    .simulation-hull-chart .axis-x text {
        opacity: 0.6;
    }

    .simulation-hull-chart .axis-x .domain {
        opacity: 1;
        color: goldenrod;
        stroke-width: 2px;
    }

    .simulation-hull-chart .axis-x {
        text-anchor: start;
    }

    .simulation-hull-chart .axis-y text {
        opacity: 0.6;
    }

    .simulation-hull-chart .axis-y line, .simulation-hull-chart .axis-y path {
        opacity: 0.1;
    }

    .portfolio-simulation-hull.loading {
        opacity: 0.5;
    }

    .portfolio-simulation-hull.loading .hide-when-loading {
        opacity: 0;
    }
</style>
