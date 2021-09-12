/* global getNodesByXPath, parse */

import ClusterModule from 'puppeteer-cluster'

import writer from './src/writer.js'

const { Cluster } = ClusterModule
const baseUrl = 'https://www.cij.gob.ar/causas-de-corrupcion.html'

async function main() {
  const cluster = await Cluster.launch({
    concurrency: Cluster.CONCURRENCY_CONTEXT,
    maxConcurrency: 5,
    // monitor: true,
    puppeteerOptions: {
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
  })

  // Event handler to be called in case of problems
  cluster.on('taskerror', (err, data) => {
    console.log(`Error crawling ${data}: ${err.message}`)
  })

  await cluster.task(async ({ page, data: { total, paged, section } }) => {
    console.log(`Scrapeando página ${paged}/${total} de la sección ${section}`)

    await page.goto(baseUrl)
    await page.evaluate(`irPaginaS${section}(${paged})`)
    await page.waitForNavigation()
    await page.addScriptTag({ path: 'src/utils.js' })

    const rows = await page.evaluate(() =>
      getNodesByXPath('//*[@id="solapa-1"]/div/ul[@class="info"]')
        .map((ul) => getNodesByXPath('li', ul))
        .map((lis) => parse(lis))
    )

    // Save to csv
    rows.forEach((row) => {
      writer({ terminado: section === 1, ...row })
    })
  })

  // Get the number of cases completed and pending
  const [section1, section2] = await cluster.execute(
    baseUrl,
    async ({ page, data: url }) => {
      await page.goto(url)
      await page.addScriptTag({ path: 'src/utils.js' })
      return await page.evaluate(() =>
        getNodesByXPath('//*[@id="paginado-sup-s2"]/div[1]/span').map(
          (r) => +r.textContent
        )
      )
    }
  )
  console.log(`Hay ${section1} casusas de la sección 1 y ${section2} de la 2`)

  const section1Pages = parseInt(section1 / 6)
  const section2Pages = parseInt(section2 / 6)
  for (let i = 0; i < section1Pages; i++) {
    cluster.queue({ total: section1Pages, paged: i, section: 1 })
  }
  for (let i = 0; i < section2Pages; i++) {
    cluster.queue({ total: section2Pages, paged: i, section: 2 })
  }

  await cluster.idle()
  await cluster.close()
}

main()
