function setupNPW() {
  fixAccordion();  
  fixInputs(); 
}

function fixInputs() {
  const npwSlider = document.getElementById("npw-slider");
  const npwSliderHead = npwSlider.querySelector('.head');
  npwSliderHead.remove(); 

  let npwNumber = document.getElementById('npw-number');
  npwNumber = npwNumber.querySelector('input[type="number"]');
  npwNumber.setAttribute("step", "0.01");
  npwNumber.value = (1).toFixed(2);

  const newSpan = document.createElement("span");
  newSpan.innerHTML = "Negative Prompt Weight";
  const ancestor = npwSlider.parentNode.parentNode.parentNode;
  ancestor.insertBefore(newSpan, ancestor.firstChild);
}

function fixAccordion() {
  const arrow = document.querySelector('#npw .icon');
  arrow.remove(); 
  const label = document.querySelector('.open');
  label.remove(); 
}

onUiLoaded(setupNPW);
