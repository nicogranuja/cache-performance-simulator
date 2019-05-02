const fs = require('fs')
const path = require('path')
const plotly = require('plotly')("NicolasAlvarezMondragon", "LltwGONZoZ77Uq8CpJUq")

const missRateStr = 'Miss Rate ='

// Trace sample
// let trace1 = {
//   x: [1, 2, 3, 4],
//   y: [10, 15, 13, 17],
//   type: 'scatter'
// };
// Sample data
// data = [trace1]
const createGraph = (data, graphTitle, xAxisTitle) => {
  let graphOptions = {
    layout: {
      title: graphTitle,
      yaxis: {
        title: 'Miss Rate %'
      },
      xaxis: {
        title: xAxisTitle
      },
    },
    fileopt: "overwrite",
    filename: graphTitle
  }

  plotly.plot(data, graphOptions, function (err, msg) {
    if (err) {
      return console.log(err)
    };
    console.log(msg)
  })
}

const readFileResults = (filePath) => {
  return new Promise((resolve, reject) => {
    fs.readFile(path.normalize(filePath), 'utf-8', (err, data) => {
      if (err) {
        return reject(console.log(err))
      }

      let lines = data.split('BATCH END')
      let results = []

      for (let i = 0; i < lines.length; i++) {
        if (lines[i].length > 0) {
          results.push(lines[i])
        }
      }

      resolve(results);
    })
  })
}

const getValueFromString = (line, str) => {
  let num = 0;
  try {
    let regex = new RegExp(`${str}\\s+(.*)\\s`, 'gi');
    let match = regex.exec(line);
    num = parseFloat(match[1])
  } catch (e) {
    console.log(e);
  }

  return num
}

const generateTrace = (filePath, valueFromCache, name) => {
  let trace = {
    x: [],
    y: [],
    name: name,
    type: 'scatter'
  }
  return new Promise((resolve, reject) => {
    readFileResults(filePath).then((results) => {
      for (let i = 0; i < results.length; i++) {
        if (results[i].length <= 1) continue

        let traceValue = getValueFromString(results[i], valueFromCache + ':')
        let missRate = getValueFromString(results[i], missRateStr)
        trace.x.push(traceValue)
        trace.y.push(missRate)
      }

      resolve(trace)
    })
  })
}

// Plot Single Traces sample
const plotCacheChange = () => {
  generateTrace('./output/cache_change.txt', 'Cache Size').then(trace => {
    createGraph([trace], 'Miss Rate (%) VS. Cache Size', 'Cache Size KB')
  })
}

const plotBlockSizeChange = () => {
  generateTrace('./output/block_change.txt', 'Block Size').then(trace => {
    createGraph([trace], 'Miss Rate (%) VS. Block Size', 'Block Size Bytes')
  })
}

const plotAssociativityChange = () => {
  generateTrace('./output/associativity_change.txt', 'Associativity').then(trace => {
    createGraph([trace], 'Miss Rate (%) VS. Associativity', 'Associativity')
  })
}

const plotCacheChangeWithAssociativity = () => {
  let promises = [];
  // Push all the generate traces files to the promises array (Don't forget to change the name)
  promises.push(generateTrace('./output/cache_change_a2.txt', 'Cache Size', 'Associativity 2'))
  promises.push(generateTrace('./output/cache_change_a4.txt', 'Cache Size', 'Associativity 4'))
  promises.push(generateTrace('./output/cache_change_a8.txt', 'Cache Size', 'Associativity 8'))

  Promise.all(promises).then(traces => {
    createGraph(traces, 'Miss Rate (%) VS. Cache Size A 2, 4, 8', 'Cache Size')
  })
};

plotCacheChangeWithAssociativity()

// plotCacheChange()
// plotBlockSizeChange()
// plotAssociativityChange()