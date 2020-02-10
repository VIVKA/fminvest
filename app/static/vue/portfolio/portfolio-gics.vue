<template>
  <div v-bind:class="{ 'loading': !portfolioData }" class="ui-block p-3 shadow-sm portfolio-gics mb-4 rounded">
    <div class="row mb-3">
        <div class="col">
            <h4 class="text-secondary">{{$t("message.title")}}</h4>
        </div>
    </div>
    <div class="row mb-3">
        <div class="col">
            <div class="chart-container hide-when-loading">
                <svg class="chart gics-chart"></svg>
            </div>
        </div>
    </div>
    <div class="row">
      <div class="col content scrolling-container hide-when-loading">
        <table class="table table-sm">
          <thead>
            <tr>
              <th colspan="2">{{$t(`message.gicsname`)}}</th>
              <th class="text-right">w %</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(gics, i) in portfolioData.gics_data">
              <td>{{gics[0]}}</td>
              <td>{{$t(`message.gics.${gics[0]}`)}}</td>
              <td class="text-right">{{((gics[1])*100).toFixed(1)+"%"}}</td>
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
                title: "Diversification",
                gics: {
                  "10": "Energy",
                  "15": "Materials",
                  "20": "Industrials",
                  "25": "Consumer Discretionary",
                  "30": "Consumer Staples",
                  "35": "Health Care",
                  "40": "Financials",
                  "45": "Information Technology",
                  "50": "Communication Services",
                  "55": "Utilities",
                  "60": "Real Estate",
                },
                gicsname: 'GICS'
            } },
            ru: { message: {
                title: "Диверсификация",
                gics: {
                  "10": "Энергетика",
                  "15": "Материалы",
                  "20": "Промышленность",
                  "25": "Товары выборочного спроса",
                  "30": "Товары повседневного спроса",
                  "35": "Здравоохранение",
                  "40": "Финансы",
                  "45": "Информационные технологии",
                  "50": "Услуги связи",
                  "55": "Коммунальные услуги",
                  "60": "Недвижимость",
                },
                gicsname: 'GICS'
            } },
        }
    },
    computed: {
        portfolioData: function() {
            return this.$store.state.portfolioData
        },
    },
    methods: {
      makeGicsChart: function() {
        const container = d3.select(".portfolio-gics .chart-container").node().getBoundingClientRect()

        const margin = {top: 0, right: 0, bottom: 30, left: 0};
        const width = 720 - margin.left - margin.right;
        const height = 260 - margin.top - margin.bottom;

        const data = this.portfolioData.gics_data
        const domain_keys = data.map(function(k) { return k[0] })
        const x = d3.scaleBand()
            // .domain([
            //   "10", "15", "20", "25", "30", "35",
            //   "40", "45", "50", "55", "60"
            // ])
            .domain(domain_keys)
            .padding([0.05])
            .range([0, width])

        const yMax = d3.max(data, function(d) { return d[1]; })

        const y = d3.scaleLinear()
            .domain([0, yMax*1.2])
            .range([height, 0]);

        const xAxis = d3.axisBottom()
            .tickSizeOuter(0)
            .tickSizeInner(0)
            .tickPadding(10)
            .scale(x);

        const target_svg = '.portfolio-gics .gics-chart'
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

        bar = chart.append("g")
          .attr('class', 'bar')
          .selectAll('g')
          .data(data)
          .enter()

        bar.append('rect')
          .attr("fill", "goldenrod")
          .attr('x', function(d, i) {
            return x(d[0]);
          })
          .attr('y', function(d){
            return y(d[1])
          })
          .attr('height', function(d) {
            return height-y(d[1]);
          })
          .attr('width', x.bandwidth());

        bar.append('text')
          .attr('x', function(d, i) {
            return x(d[0])+x.bandwidth()/2;
          })
          .attr('y', function(d){
            return y(d[1])
          })
          .attr("dy", -10)
          .attr("fill", "grey")
          .text(function(d){ return `${(d[1]*100).toFixed(1)}%` })

        chart.append("g")
          .append("line")
          .attr("x1", 0)
          .attr("x2", width)
          .attr("y1", y(1/11))
          .attr("y2", y(1/11))
          .attr("stroke-width", "2px")
          .attr("stroke-dasharray", "5")
          .attr("opacity", 0.5)
          .attr("stroke", "grey")


      }
      // gicsNameFromCode: (c) => {
      //   const SECTOR_DATA = {
      //       "10": "Energy",
      //       "15": "Materials",
      //       "20": "Industrials",
      //       "25": "Consumer Discretionary",
      //       "30": "Consumer Staples",
      //       "35": "Health Care",
      //       "40": "Financials",
      //       "45": "Information Technology",
      //       "50": "Telecommunication",
      //       "55": "Utilities",
      //       "60": "Real Estate",
      //       ": "Undefined"
      //   }

      //   return SECTOR_DATA[c]
      // },
    },
    watch: {
      portfolioData: async function() {
        if(this.portfolioData) {
          this.makeGicsChart()
        }
      },
    },
  }
</script>

<style>
  .scrolling-container {
    overflow-x: scroll;
    overflow-y: hidden;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
  }

  .portfolio-gics.loading {
    opacity: 0.5;
  }

  .portfolio-gics.loading .hide-when-loading {
    opacity: 0;
  }

  .portfolio-gics .axis-x .domain {
      opacity: 1;
      color: goldenrod;
      stroke-width: 2px;
  }

  .portfolio-gics table thead th {
      border-top: 0;
  }

  .portfolio-gics .axis-x text {
      opacity: 0.6;
      /*font-weight: bold;*/
  }

  .portfolio-gics .bar text {
      text-anchor: middle;
  }

  .portfolio-gics text {
      font-size: 0.8rem;
  }

</style>
