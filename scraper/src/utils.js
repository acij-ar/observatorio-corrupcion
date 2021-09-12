const getNodesByXPath = (xpath, contextNode = document) => {
  const nodes = []
  const results = document.evaluate(
    xpath,
    contextNode,
    null,
    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
    null
  )
  for (let i = 0; i < results.snapshotLength; i++) {
    nodes.push(results.snapshotItem(i))
  }
  return nodes
}

const mapKeys = {
  Expediente: 'expediente',
  Carátula: 'caratula',
  Delitos: 'delitos',
  'Radicación del expediente': 'radicacioon_del_expediente',
  Estado: 'estado',
  'Resolución/es': 'resoluciones',
  'Última actualización': 'ultima_actualizacion',
}

// eslint-disable-next-line no-unused-vars
const parse = (lis) => {
  const row = {}
  lis.forEach((li) => {
    let [key, text] = li.textContent
      .replace(/\s+/g, ' ')
      // eslint-disable-next-line no-undef
      .split(':', (limit = 2))
    key = mapKeys[key.trim()]

    if (['expediente', 'estado', 'ultima_actualizacion'].includes(key)) {
      text = text.trim()
    } else if (key === 'delitos') {
      text = text.split(',').map((d) => ({ delito: d.trim() }))
    } else if (key === 'resoluciones') {
      text = getNodesByXPath('div/div/a', li).map((a) => {
        const text = a.textContent
        // eslint-disable-next-line no-undef
        const [date, rest] = text.split(':', (limit = 2))
        let camara = rest
        let room = ''
        if (rest.includes('-')) {
          // eslint-disable-next-line no-undef
          ;[camara, room] = rest.split('-', (limit = 2))
        }
        return {
          fecha: date,
          camara: camara.trim(),
          sala: room.trim(),
          link: a.href,
        }
      })
    } else if (key === 'radicacioon_del_expediente') {
      text = [
        ...getNodesByXPath('div[contains(@class, "item-especial-largo")]', li),
        ...getNodesByXPath('div/div/div[@class="item-especial-largo"]', li),
      ]
        .map((node) => [...node.children].map((div) => div.textContent))
        .map((node) => [
          ...node,
          // eslint-disable-next-line no-unused-vars
          ...Array.from({ length: 4 - node.length }, (_) => ''),
        ])
        .map((row) => ({
          fecha: row[0],
          camara: row[1],
          fiscal: row[2],
          fiscalia: row[3],
        }))
    } else if (key === 'caratula') {
      text = li.innerText.replace('Carátula: ', '')

      const relations = getNodesByXPath('div/div/div/div[@class="resalta"]', li)
        .map((div) => div.textContent)
        .map((relation) => relation.replace(/S:(\s+)?$/gm, ''))

      const involved = getNodesByXPath('div/div/div/ul', li)
        .map((ul, i) => {
          const lis = getNodesByXPath('li', ul)
          return lis.map((li) => [relations[i], li])
        })
        .flat()
        .map((row) => {
          const [relation, li] = row
          // eslint-disable-next-line no-unused-vars
          const [involved, _] = li.innerText.split('VER LETRADOS')
          const layers = getNodesByXPath('div/div[@class="item"]', li).map(
            (div) => div.textContent
          )

          if (layers.length) {
            return layers.map((layer) => [
              relation,
              involved.trim(),
              layer.trim(),
            ])
          }
          return [[relation, involved.trim(), '']]
        })
        .flat()
        .filter((row) => row[1].toLowerCase() !== 'ver todos')
        .map((row) => ({
          relacion: row[0],
          nombre: row[1],
          abogado: row[2],
        }))

      row.implicados = involved
    }

    row[key] = text
  })

  return row
}
