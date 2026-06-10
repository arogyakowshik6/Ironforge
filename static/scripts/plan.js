function toggleDay(i){
  const el=document.getElementById('day-'+i);
  const pills=document.querySelectorAll('.day-pill');
  const wasOpen=el.classList.contains('open');
  document.querySelectorAll('.day-detail').forEach(d=>d.classList.remove('open'));
  document.querySelectorAll('.day-pill').forEach(p=>p.classList.remove('active'));
  if(!wasOpen){el.classList.add('open');pills[i].classList.add('active');el.scrollIntoView({behavior:'smooth',block:'nearest'});}
}
// Open Monday by default
toggleDay(0);