function setupNPW() {
  fixAccordion('tab_txt2img');  
  fixAccordion('tab_img2img');  
  fixInputs('tab_txt2img');
  fixInputs('tab_img2img');
}

function fixInputs(tab) {
  const npwSlider = document.querySelector(`#${tab} #npw-slider`);

  npwSlider.querySelector('.head').remove(); 

  const newSpan = document.createElement("span");
  newSpan.innerHTML = "Negative Prompt Weight";
  const ancestor = npwSlider.parentNode.parentNode.parentNode;
  ancestor.insertBefore(newSpan, ancestor.firstChild);

  document.querySelector(`#${tab} #npw-number input[type="number"]`).setAttribute("step", "0.01");
}

function fixAccordion(tab) {
  document.querySelector(`#${tab} #npw .icon`).remove();
  document.querySelector(`#${tab} #npw .open`).remove();  
}

onUiLoaded(setupNPW);
