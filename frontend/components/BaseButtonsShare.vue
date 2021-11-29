<template>
  <header>
    <h2 class="title is-1">{{ title }} <slot></slot></h2>
    <div class="is-pulled-right buttonsShare">

      <!-- Dowload data -->
      <button v-if="data" class="button" @click="downloadData">
        Descargar datos
      </button>

      <!-- API -->
      <button class="button" @click="openApiDialog">
        API
      </button>

      <!-- Embeber -->
      <button class="button" @click="openEmbeberDialog">
        Embeber
      </button>

      <button v-if="plotName" class="button" @click="downloadAsPNG">
        Descargar grafico
      </button>

    </div><!--/buttonsShare -->
  </header>
</template>

<script>
import * as d3 from 'd3'
import { saveAs } from 'file-saver'
import { apiUrl } from '@/assets/utils'

import { downloadEntityBio, downloadEntityCases, downloadCasesResolution,
  downloadCasesInvolved, downloadStats, downloadStatsOral,
  downloadStatsOld, downloadGraph } from '~/assets/js/downloadData'

export default {
  name: 'ShareButtons',
  props: {
    section: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    data: {
      type: Array
    },
    plotName: {
      type: String
    }
  },
  methods: {
    downloadData: function () {
      if (this.section === 'biografia') {
        downloadEntityBio(this.data, this.$route.query.nombre)
      } else if (this.section === 'causas') {
        downloadEntityCases(this.data, this.$route.query.nombre)
      } else if (this.section === 'resoluciones') {
        downloadCasesResolution(this.data, this.$route.query.nombre)
      } else if (this.section === 'involucrados') {
        downloadCasesInvolved(this.data, this.$route.query.nombre)
      } else if (this.section === 'topRelacion') {
        downloadStats(this.data, 'relaciones')
      } else if (this.section === 'casosPorAnio') {
        downloadStats(this.data, 'casos por anio')
      } else if (this.section === 'jueces') {
        downloadStats(this.data, 'jueces')
      } else if (this.section === 'juiciosOral') {
        downloadStatsOral(this.data, 'juicio oral')
      } else if (this.section === 'crimenes') {
        downloadStats(this.data, 'crimenes')
      } else if (this.section === 'casosViejos') {
        downloadStatsOld(this.data, 'casos viejos')
      } else if (this.section === 'conexiones') {
        downloadGraph(this.data, this.$route.query.nombre)
      }

    },
    openApiDialog () {
      this.$buefy.dialog.prompt({
        title: 'API',
        message: 'Link a nuestra API sobre Causas de Corrucion',
        confirmText: 'Copiar',
        cancelText: 'Cancelar',
        inputAttrs: {
          readonly: 'readonly',
          placeholder: 'URL',
          type: 'text',
          id: 'copy-api-' + this.section,
          value: apiUrl + 'nodo/nodos_entidades/' + this.$route.query.nombre
        },
        onConfirm: (value) => {
          this.$buefy.toast.open({
            message: 'Link copiado al portapapeles.',
            type: 'is-success'
          })
          this.copyLink()
        }
      })
    },
    openEmbeberDialog () {
      this.$buefy.dialog.prompt({
        title: 'Embeber',
        message: 'Url para embeber',
        confirmText: 'Copiar',
        cancelText: 'Cancelar',
        inputAttrs: {
          readonly: 'readonly',
          placeholder: 'URL',
          type: 'text',
          id: 'copy-api-' + this.section,
          value: this.generateLink()
        },
        onConfirm: (value) => {
          this.$buefy.toast.open({
            message: 'Link copiado al portapapeles.',
            type: 'is-success'
          })
          this.copyLink()
        }
      })
    },
    copyLink () {
      var copyTextarea = document.getElementById('copy-api-' + this.section)
      copyTextarea.select()
      document.execCommand('copy')
    },
    generateLink: function () {
      // Generate link to embeber
      let area = this.$route.name
      let node = this.$route.query.nombre

      if (area === 'estadisticas') {
        return `${window.location.origin}/embeber?area=${area}&section=${this.section}`
      }

      return `${window.location.origin}/embeber?area=${area}&section=${this.section}&nombre=${node}`
    },
    downloadAsPNG: function () {
      /*
      Download the svg to a png file
      */
      let that = this
      let width = +document.getElementById(this.plotName).getAttribute('width')
      let height = +document.getElementById(this.plotName).getAttribute('height')
      let svg = d3.select('#' + this.plotName)

      var svgString = this.getSVGString(svg.node())

      function save (dataBlob, filesize) {
        const pngName = (`${that.title} ${that.$route.query.nombre}.png`)
          .replace(/ /, '_')
          .replace(/-/, '_')
          .toLowerCase()
        saveAs(dataBlob, pngName) // FileSaver.js function
      }

      // passes Blob and filesize String to the callback
      this.svgString2Image(svgString, 2 * width, 2 * height, 'png', save)
    },
    getSVGString: function (svgNode) {
      svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink')
      var cssStyleText = getCSSStyles(svgNode)
      appendCSS(cssStyleText, svgNode)

      var serializer = new XMLSerializer()
      var svgString = serializer.serializeToString(svgNode)
      svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink=') // Fix root xlink without namespace
      svgString = svgString.replace(/NS\d+:href/g, 'xlink:href') // Safari NS namespace fix

      return svgString

      function getCSSStyles (parentElement) {
        var selectorTextArr = []

        // Add Parent element Id and Classes to the list
        selectorTextArr.push('#' + parentElement.id)
        for (let c = 0; c < parentElement.classList.length; c++) {
          if (!contains('.' + parentElement.classList[c], selectorTextArr)) {
            selectorTextArr.push('.' + parentElement.classList[c])
          }
        }

        // Add Children element Ids and Classes to the list
        var nodes = parentElement.getElementsByTagName('*')
        for (let i = 0; i < nodes.length; i++) {
          var id = nodes[i].id
          if (!contains('#' + id, selectorTextArr)) {
            selectorTextArr.push('#' + id)
          }

          var classes = nodes[i].classList
          for (let c = 0; c < classes.length; c++) {
            if (!contains('.' + classes[c], selectorTextArr)) {
              selectorTextArr.push('.' + classes[c])
            }
          }
        }

        // Extract CSS Rules
        var extractedCSSText = ''
        for (var i = 0; i < document.styleSheets.length; i++) {
          var s = document.styleSheets[i]

          try {
            if (!s.cssRules) continue
          } catch (e) {
            if (e.name !== 'SecurityError') throw e // for Firefox
            continue
          }

          var cssRules = s.cssRules
          for (var r = 0; r < cssRules.length; r++) {
            if (contains(cssRules[r].selectorText, selectorTextArr)) {
              extractedCSSText += cssRules[r].cssText
            }
          }
        }

        return extractedCSSText

        function contains (str, arr) {
          // eslint-disable-next-line
          return arr.indexOf(str) === -1 ? false : true
        }
      }

      function appendCSS (cssText, element) {
        var styleElement = document.createElement('style')
        styleElement.setAttribute('type', 'text/css')
        styleElement.innerHTML = cssText
        var refNode = element.hasChildNodes() ? element.children[0] : null
        element.insertBefore(styleElement, refNode)
      }
    },
    svgString2Image: function (svgString, width, height, format, callback) {
      // eslint-disable-next-line
      format = format ? format : 'png'
      var imgsrc = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString))) // Convert SVG string to data URL
      var canvas = document.createElement('canvas')
      var context = canvas.getContext('2d')

      canvas.width = width
      canvas.height = height

      var image = new Image()
      image.onload = function () {
        context.clearRect(0, 0, width, height)
        context.drawImage(image, 0, 0, width, height)

        canvas.toBlob(function (blob) {
          var filesize = Math.round(blob.length / 1024) + ' KB'
          if (callback) callback(blob, filesize)
        })
      }

      image.src = imgsrc
    }
  }
}
</script>

<style scoped>
header {
  padding-top: 50px;
  padding-bottom: 50px;
}

header h2, .buttonsShare {
  display: inline;
}

.buttonsShare {
  padding-left: 20px;
}

button {
  border-radius: 0;
  margin-left: 10px;
  font-weight: bold;
  font-size: 1.5rem;
  font-family: BisionBold;
  text-transform: uppercase;
}

/* Day Button */
body.day button {
  color: white;
  background-color: #0a121b;
  border: solid 3px black;
  box-shadow: 5px 5px 2px 1px rgba(0, 0, 255, .2);
}

body.day button:hover {
  background-color: #ffffff;
  color: #000000;
  border-color: #000000;
}

body.day .buttonsShare button:first-child {
  background-color: #ffffff;
  color: #000000;
}

body.day .buttonsShare button:first-child:hover {
  background-color: #0a121b;
  color: #ffffff;
}

/* Night button */
body.night button {
  color: black;
  background-color: #ffffff;
  border: solid 3px white;
  box-shadow: 5px 5px 2px 1px rgba(255, 255, 255, .4);
}

body.night button:hover {
  background-color: black;
  color: #ffffff;
  border-color: #ffffff;
}

body.night .buttonsShare button:first-child {
  background-color: #000000;
  color: #ffffff;
}

body.night .buttonsShare button:first-child:hover {
  background-color: #ffffff;
  color: #0a121b;
}
</style>
