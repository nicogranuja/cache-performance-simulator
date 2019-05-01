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
const createGraph = (data, title, yTitle) => {
  let graphOptions = {
    layout: {
      title: title,
      yaxis: {
        title: 'Miss Rate %'
      },
      xaxis: {
        title: yTitle
      },
    },
    fileopt: "overwrite",
    filename: yTitle
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

const generateTrace = (filePath, traceName) => {
  let trace = {
    x: [],
    y: [],
    name: traceName,
    type: 'scatter'
  }
  return new Promise((resolve, reject) => {
    readFileResults(filePath).then((results) => {
      for (let i = 0; i < results.length; i++) {
        if (results[i].length <= 1) continue

        let traceValue = getValueFromString(results[i], traceName + ':')
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

// plotCacheChange()
// plotBlockSizeChange()
// plotAssociativityChange()