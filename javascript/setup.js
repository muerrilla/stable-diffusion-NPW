function setupNPW() {
  fixAccordion();  
  fixInputs();
}

function fixInputs() {
  const npwSlider_t2i = document.querySelector("#tab_txt2img #npw-slider");
  const npwSlider_i2i = document.querySelector("#tab_img2img #npw-slider");

  npwSlider_t2i.querySelector('.head').remove(); 
  npwSlider_i2i.querySelector('.head').remove(); 

  const newSpan = document.createElement("span");
  newSpan.innerHTML = "Negative Prompt Weight";
  const ancestor_t2i = npwSlider_t2i.parentNode.parentNode.parentNode;
  ancestor_t2i.insertBefore(newSpan, ancestor_t2i.firstChild);
  const ancestor_i2i = npwSlider_i2i.parentNode.parentNode.parentNode;
  ancestor_i2i.insertBefore(newSpan.cloneNode(true), ancestor_i2i.firstChild);

  document.querySelector('#tab_txt2img #npw-number input[type="number"]').setAttribute("step", "0.01");
  document.querySelector('#tab_img2img #npw-number input[type="number"]').setAttribute("step", "0.01");
}

function fixAccordion() {
  document.querySelector('#tab_txt2img #npw .icon').remove();
  document.querySelector('#tab_img2img #npw .icon').remove();
  document.querySelector('#tab_txt2img #npw .open').remove();  
  document.querySelector('#tab_img2img #npw .open').remove();  
}

onUiLoaded(setupNPW);
