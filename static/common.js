const $=(s,root=document)=>root.querySelector(s); const $$=(s,root=document)=>[...root.querySelectorAll(s)];
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2800)}
function setHand(mode){document.body.dataset.hand=mode;localStorage.setItem('easyHand',mode);const el=$('#handMode');if(el)el.value=mode}
function initHand(){setHand(localStorage.getItem('easyHand')||'right')}
function fmtDate(v){if(!v)return '—';const d=new Date(v);return isNaN(d)?v:d.toLocaleString()}
function esc(s){return String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
function activateView(id){$$('.view').forEach(v=>v.classList.toggle('active',v.id===id));$$('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===id));window.scrollTo({top:0,behavior:'smooth'})}
async function api(path,opts={}){const r=await fetch(path,{headers:{'Content-Type':'application/json',...(opts.headers||{})},...opts});if(!r.ok)throw new Error((await r.text())||r.statusText);return r.status===204?null:r.json()}
window.addEventListener('load',()=>{initHand();if('serviceWorker' in navigator)navigator.serviceWorker.register('/static/sw.js').catch(()=>{});$$('[data-view]').forEach(b=>b.addEventListener('click',()=>activateView(b.dataset.view)));const h=$('#handMode');if(h)h.addEventListener('change',e=>setHand(e.target.value));});
