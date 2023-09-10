const ctx1 = document.getElementById('graphLineUmidade');
    let config1 = {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: "Umidade",
          data: [],
          borderWidth: 0.5,
          fill: 'origin',
          pointRadius: 1,
          cubicInterpolationMode: 'monotone',
          backgroundColor: 'rgba(153, 102, 255, 0.6)',
        }]
      },

      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `${value} %`
            }
          }
        }
      }
    };
    let chartHumi = new Chart(ctx1, config1);

    const ctx2 = document.getElementById('graphLinePressao');
    let config2 = {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: "Pressão Atmosférica",
          data: [],
          borderWidth: 0.5,
          fill: 'origin',
          pointRadius: 1,
          cubicInterpolationMode: 'monotone',
          backgroundColor: 'rgba(12, 90, 232, 0.6)',
        }]
      },

      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `${value} hPa`
            }
          }
        }
      }
    };
    let chartPress = new Chart(ctx2, config2);

    const ctx3 = document.getElementById('graphLineTempInt');
    let config3 = {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: "Temperatura Interna",
          data: [],
          borderWidth: 0.5,
          fill: 'origin',
          pointRadius: 1,
          cubicInterpolationMode: 'monotone',
          backgroundColor: 'rgba(31, 81, 65, 0.6)',
        }]
      },

      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `${value} °C`
            }
          }
        }
      }
    };
    let chartTemp1 = new Chart(ctx3, config3);

    const ctx4 = document.getElementById('graphLineTempExt');
    let config4 = {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: "Temperatura Externa",
          data: [],
          borderWidth: 0.5,
          fill: 'origin',
          pointRadius: 1,
          cubicInterpolationMode: 'monotone',
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
        }]
      },

      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => `${value} °C`
            }
          }
        }
      }
    };
    let chartTemp2 = new Chart(ctx4, config4);

    const max = array => {
      if (array.length === 0) {
        max.dateIndex = undefined
        max.value = undefined
        return max
      }
      let max = new Object()
      max.value = 0
      for (let index = 0; index < array.length; index++) {
        if (max.value === 0) {
          max.dateIndex = index
          max.value = array[index]
        }
        if (array[index] > max.value) {
          max.dateIndex = index
          max.value = array[index]
        }
      }
      return max
    }

    const min = array => {
      if (array.length === 0) {
        min.dateIndex = undefined
        min.value = undefined
        return min
      }
      let min = new Object()
      min.value = 0
      for (let index = 0; index < array.length; index++) {
        if (min.value === 0) {
          min.dateIndex = index
          min.value = array[index]
        }
        if (array[index] < min.value) {
          min.dateIndex = index
          min.value = array[index]
        }
      }
      return min
    }

    const mean = array => {
      if (array.length === 0) {
        return undefined
      }
      let sum = 0
      for (let index = 0; index < array.length; index++) {
        sum += array[index]
      }
      return (sum / array.length).toFixed(2)
    }

    const maxUmi = document.getElementById('max-umi')
    const meanUmi = document.getElementById('mean-umi')
    const minUmi = document.getElementById('min-umi')
    const maxPress = document.getElementById('press-max')
    const meanPress = document.getElementById('press-mean')
    const minPress = document.getElementById('press-min')
    const maxTempInt = document.getElementById('max-temp-int')
    const meanTempInt = document.getElementById('mean-temp-int')
    const minTempInt = document.getElementById('min-temp-int')
    const maxTempExt = document.getElementById('max-temp-ext')
    const meanTempExt = document.getElementById('mean-temp-ext')
    const minTempExt = document.getElementById('min-temp-ext')

    const updateMax = (label, humi, press, temp1, temp2) => {
      let maxObj = new Object()

      maxObj.umiMax = max(humi)
      maxObj.umiDateMax = label[maxObj.umiMax.dateIndex]
      maxUmi.innerHTML = `${maxObj.umiDateMax}<br>${maxObj.umiMax.value} %`

      maxObj.presMax = max(press)
      maxObj.presDateMax = label[maxObj.presMax.dateIndex]
      maxPress.innerHTML = `${maxObj.presDateMax}<br>${maxObj.presMax.value} hPa`

      maxObj.tempIntMax = max(temp1)
      maxObj.tempIntDateMax = label[maxObj.tempIntMax.dateIndex]
      maxTempInt.innerHTML = `${maxObj.tempIntDateMax}<br>${maxObj.tempIntMax.value} °C`

      maxObj.tempExtMax = max(temp2)
      maxObj.tempExtDateMax = label[maxObj.tempExtMax.dateIndex]
      maxTempExt.innerHTML = `${maxObj.tempExtDateMax}<br>${maxObj.tempExtMax.value} °C`
    }

    const updateMin = (label, humi, press, temp1, temp2) => {
      let minObj = new Object()

      minObj.umiMin = min(humi)
      minObj.umiDateMin = label[minObj.umiMin.dateIndex]
      minUmi.innerHTML = `${minObj.umiDateMin}<br>${minObj.umiMin.value} %`

      minObj.presMin = min(press)
      minObj.presDateMin = label[minObj.presMin.dateIndex]
      minPress.innerHTML = `${minObj.presDateMin}<br>${minObj.presMin.value} hPa`

      minObj.tempIntMin = min(temp1)
      minObj.tempIntDateMin = label[minObj.tempIntMin.dateIndex]
      minTempInt.innerHTML = `${minObj.tempIntDateMin}<br>${minObj.tempIntMin.value} °C`

      minObj.tempExtMin = min(temp2)
      minObj.tempExtDateMin = label[minObj.tempExtMin.dateIndex]
      minTempExt.innerHTML = `${minObj.tempExtDateMin}<br>${minObj.tempExtMin.value} °C`
    }

    const updateMean = (label, humi, press, temp1, temp2) => {
      meanUmi.innerHTML = `- <br>${mean(humi)} %`
      meanPress.innerHTML = `- <br>${mean(press)} hPa`
      meanTempInt.innerHTML = `- <br>${mean(temp1)} °C`
      meanTempExt.innerHTML = `- <br>${mean(temp2)} °C`
    }

    const updateCharts = (label, humi, press, temp1, temp2) => {
      chartHumi.data.labels = label
      chartHumi.data.datasets.forEach(element => {
        element.data = humi
      });
      chartHumi.update()

      chartPress.data.labels = label
      chartPress.data.datasets.forEach(element => {
        element.data = press
      });
      chartPress.update()

      chartTemp1.data.labels = label
      chartTemp1.data.datasets.forEach(element => {
        element.data = temp1
      });
      chartTemp1.update()

      chartTemp2.data.labels = label
      chartTemp2.data.datasets.forEach(element => {
        element.data = temp2
      });
      chartTemp2.update()
    }

    const fetchEngineCharts = (url) => {
      fetch(url)
        .then(response => {
          if (response.status !== 200) throw new Error(
            'Dados não encontrados: ' + response.statusText
          )
          return response.json()
        })
        .then(data => {
          let labelss = []
          let humidity = []
          let pressure = []
          let tempIn = []
          let tempEx = []
          data.forEach(element => {
            labelss.push(element.data_hora)
            humidity.push(element.umidade)
            pressure.push(element.pressao)
            tempIn.push(element.temp_int)
            tempEx.push(element.temp_ext)
          })
          updateCharts(labelss, humidity, pressure, tempIn, tempEx)
          updateMax(labelss, humidity, pressure, tempIn, tempEx)
          updateMin(labelss, humidity, pressure, tempIn, tempEx)
          updateMean(labelss, humidity, pressure, tempIn, tempEx)
        })
        .catch(e => console.log(e))
    }

    const urlGraf = 'https://www.brainstormtecnologia.tech/api/graficosIndex/'
    const urlLocal = 'http://127.0.0.1:8000/api/graficosIndex/'
    fetchEngineCharts(urlGraf)
    setInterval(() => {
      fetchEngineCharts(urlGraf)
    }, 300000);