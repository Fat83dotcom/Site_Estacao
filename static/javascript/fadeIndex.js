window.addEventListener('load', () =>{
    let contentA = document.getElementById('fade-info-A')
    let contentB = document.getElementById('fade-info-B')
    let contentC = document.getElementById('fade-graph-A')
    let contentD = document.getElementById('fade-graph-B')
    let flex = 'flex'
    let value = '1'
    contentA.style.display = flex
    contentB.style.display = flex
    contentC.style.display = flex
    contentD.style.display = flex
    setTimeout(() =>{
      contentA.style.opacity = value
      contentB.style.opacity = value
      contentC.style.opacity = value
      contentD.style.opacity = value
    }, 500)
  })