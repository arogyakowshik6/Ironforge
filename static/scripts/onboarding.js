console.log('onboardingjs file is work')
let current = 1;
const total = 13;
const answers = {};

function showStep(n){
  document.querySelectorAll('.step').forEach(s=>s.classList.remove('active'));
  document.querySelector(`[data-step="${n}"]`).classList.add('active');
  document.getElementById('prog').style.width = ((n-1)/(total-1)*100)+'%';
  document.getElementById('back-btn').style.display = n>1?'':'none';
  document.getElementById('next-btn').style.display = n===total?'none':'';
  if(n===total) buildSummary();
}

function nextStep(){
  if(!validateStep()) return;
  current++;
  showStep(current);
}

document.getElementById('next-btn').addEventListener('click', nextStep)

function prevStep(){ if(current>1){ current--; showStep(current); } }

function validateStep(){
  const step = document.querySelector(`[data-step="${current}"]`);
  const inp = step.querySelector('input[type=number], input[type=text]');
  if(inp && !inp.value){ inp.focus(); inp.style.borderColor='var(--red)'; setTimeout(()=>inp.style.borderColor='',1500); return false; }
  const hidden = step.querySelector('input[type=hidden]');
  if(hidden && !hidden.value){ step.querySelectorAll('.opt-btn')[0].style.animation='shake .3s'; return false; }
  return true;
}

document.querySelectorAll('.opt-btn').forEach(btn=>{
  btn.addEventListener('click',function(){
    const field = this.dataset.field;
    document.querySelectorAll(`[data-field="${field}"]`).forEach(b=>b.classList.remove('selected'));
    this.classList.add('selected');
    document.getElementById(field).value = this.dataset.val;
    answers[field] = this.dataset.val;
    setTimeout(nextStep, 200);
  });
});

function setUnit(field, unit, el){
  el.parentElement.querySelectorAll('.unit-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
}

const labels = {name:'Name',age:'Age',gender:'Gender',height:'Height',weight:'Weight',target_weight:'Target Weight',body_type:'Body Type',experience:'Experience',goal:'Goal',days:'Days/Week',equipment:'Equipment',health:'Health'};
function buildSummary(){
  const form = document.getElementById('ob-form');
  const fd = new FormData(form);
  let html='';
  for(const [k,v] of fd.entries()) if(v) html+=`<div class="sum-item"><div class="sum-key">${labels[k]||k}</div><div class="sum-val">${v.replace(/_/g,' ')}</div></div>`;
  document.getElementById('summary-grid').innerHTML=html;
}