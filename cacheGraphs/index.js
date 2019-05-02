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
  promises.push(generateTrace('./output/cache_change_b2_a4_RND.txt', 'Cache Size', 'Block Offset 2'))
  promises.push(generateTrace('./output/cache_change_b8_a4_RND.txt', 'Cache Size', 'Block Offset 8'))
  promises.push(generateTrace('./output/cache_change_b32_a4_RND.txt', 'Cache Size', 'Block Offset 32'))
  promises.push(generateTrace('./output/cache_change_b64_a4_RND.txt', 'Cache Size', 'Block Offset 64'))

  Promise.all(promises).then(traces => {
    createGraph(traces, 'Miss Rate (%) VS. Cache Size B 2 8 32 64, A 4 RND', 'Cache Size')
  })
};

const plotBlockChange = () => {
  let promises = [];
  // Push all the generate traces files to the promises array (Don't forget to change the name)
  promises.push(generateTrace('./output/block_change_s8_a4_RND.txt', 'Block Size', 'Cache Size 8'))
  promises.push(generateTrace('./output/block_change_s64_a4_RND.txt', 'Block Size', 'Cache Size 64'))
  promises.push(generateTrace('./output/block_change_s256_a4_RND.txt', 'Block Size', 'Cache Size 256'))
  promises.push(generateTrace('./output/block_change_s1024_a4_RND.txt', 'Block Size', 'Cache Size 1024'))

  Promise.all(promises).then(traces => {
    createGraph(traces, 'Miss Rate (%) VS. Block Size S 8 64 256 1024, A 4, RND', 'Block Size')
  })
};

const plotAssocChange = () => {
  let promises = [];
  // Push all the generate traces files to the promises array (Don't forget to change the name)
  promises.push(generateTrace('./output/associativity_change_s64_b2_RND.txt', 'Associativity', 'Block Offset 2'))
  promises.push(generateTrace('./output/associativity_change_s64_b16_RND.txt', 'Associativity', 'Block Offset 16'))
  promises.push(generateTrace('./output/associativity_change_s64_b32_RND.txt', 'Associativity', 'Block Offset 32'))
  promises.push(generateTrace('./output/associativity_change_s64_b64_RND.txt', 'Associativity', 'Block Offset 64'))

  Promise.all(promises).then(traces => {
    createGraph(traces, 'Miss Rate (%) VS. Associativity S 64, B 2 16 32 64, RND', 'Associativity')
  })
};


// plotCacheChangeWithAssociativity()
plotBlockChange()
// plotAssocChange()

// plotCacheChange()
// plotBlockSizeChange()
// plotAssociativityChange()