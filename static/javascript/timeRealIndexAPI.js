const urlRealTime = 'https://www.brainstormtecnologia.tech/api/tempo_real/'
const urlLocalTime = 'http://127.0.0.1:8000/api/tempo_real/'
const date = document.getElementById('dateNow')
const umi = document.getElementById('umi')
const press = document.getElementById('press')
const temp1 = document.getElementById('tmp1')
const temp2 = document.getElementById('tmp2')
const updateData = data => {
    date.textContent = JSON.stringify(data.data_hora).replace(/"/g, '')
    umi.textContent = JSON.stringify(data.umidade)
    press.textContent = JSON.stringify(data.pressao)
    temp1.textContent = JSON.stringify(data.temp_int)
    temp2.textContent = JSON.stringify(data.temp_ext)
}
setInterval(() => {
    fetch(urlRealTime)
    .then(response => {
        if (response.status !== 200) throw new Error('Dados não encontrados')
        return response.json()
    })
    .then(data => {
        updateData(data)
    })
    .catch(e => console.log(e))
}, 1000);