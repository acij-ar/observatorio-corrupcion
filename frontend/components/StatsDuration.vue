<template>
  <section id="duration">
    <div class="container">
      <base-buttons-share section="duracionCausas" title="Cantidad de causas por duracion"></base-buttons-share>

      <b-tabs>
        <!-- Tab 1 -->
        <b-tab-item label="Instruccion abierta">
          <div class="columns">

            <div class="column is-6">
              <b-table :data="casesEnd">
                <b-table-column field="bin" label="Duracion" v-slot="props">
                  <div class="box" :style="{'background-color': colors[props.index]}"></div>
                  {{ props.row.bin }}
                </b-table-column>

                <b-table-column field="value" label="Cantidad" v-slot="props">
                  {{ props.row.value }}
                </b-table-column>

                <b-table-column field="percent" label="Porcentaje" v-slot="props">
                  {{ props.row.p }}
                </b-table-column>
              </b-table>
            </div>

            <div class="column is-6">
              <donut id="durationEndPlot" :data="casesEnd"></donut>
            </div>

          </div><!--/columns -->
        </b-tab-item>

        <!-- Tab 2 -->
        <b-tab-item label="Instruccion cerrada">
          <div class="columns">

            <div class="column is-6">
              <b-table :data="casesOpen">
                <b-table-column field="bin" label="Duracion" v-slot="props">
                  <div class="box" :style="{'background-color': colors[props.index]}"></div>
                  {{ props.row.bin }}
                </b-table-column>

                <b-table-column field="value" label="Cantidad" v-slot="props">
                  {{ props.row.value }}
                </b-table-column>

                <b-table-column field="percent" label="Porcentaje" v-slot="props">
                  {{ props.row.p }}
                </b-table-column>
              </b-table>
            </div>

            <div class="column is-6">
              <donut id="durationOpenPlot" :data="casesOpen"></donut>
            </div>

          </div><!--/columns -->
        </b-tab-item>
      </b-tabs>

    </div>
  </section>
</template>

<script>
import * as d3 from 'd3'
import { apiUrl } from '@/assets/utils'
import Donut from '~/components/PlotDonut'
import BaseButtonsShare from '~/components/BaseButtonsShare'

export default {
  data () {
    return {
      casesEnd: [],
      casesOpen: [],
      colors: d3.schemeCategory10
    }
  },
  components: {
    Donut,
    BaseButtonsShare
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData: function () {
      d3.json(apiUrl + 'estadisticas/duracion')
        .then(dataJson => {
          console.log(dataJson)
          let f = d3.format('.1f')

          this.casesEnd = dataJson.resultado.terminadas.map(d => {
            d.p = f(d.p)
            return d
          })

          this.casesOpen = dataJson.resultado.abiertas.map(d => {
            d.p = f(d.p)
            return d
          })
        })
    }
  }
}
</script>

<style scoped>
.box {
  padding: 0;
  width: 50px;
  height: 30px;
  display: table-cell;
  vertical-align: middle;
}
</style>
