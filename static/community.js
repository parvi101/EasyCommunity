let saved=[];
try{saved=JSON.parse(localStorage.getItem('ecSaved')||'[]');if(!Array.isArray(saved))saved=[]}catch{saved=[]}
let latestNotices=[];
let latestEvents=[];
function persistSaved(){try{localStorage.setItem('ecSaved',JSON.stringify(saved));return true}catch{return false}}
function saveItem(id){if(!saved.includes(id))saved.push(id);else saved=saved.filter(x=>x!==id);const persisted=persistSaved();loadSaved();loadListings();toast(persisted?'Saved items updated':'Saved for this session only; browser storage is unavailable')}
function friendlyTime(value){if(!value)return 'Unavailable';const d=new Date(value);return Number.isNaN(d.getTime())?String(value):d.toLocaleString([], {dateStyle:'medium',timeStyle:'short'})}
function shortDate(value){if(!value)return 'Timing unverified';const d=new Date(value);return Number.isNaN(d.getTime())?String(value):d.toLocaleDateString([], {day:'numeric',month:'short'})}
function noticeVisual(row){const text=`${row.title} ${row.body}`.toLowerCase();if(text.includes('rain')||text.includes('weather'))return {icon:'☂',klass:'warning',status:'ALERT',statusClass:'alert',action:'Plan accordingly.'};if(text.includes('security')||text.includes('visitor'))return {icon:'◇',klass:'safety',status:'ADVISORY',statusClass:'advisory',action:'Verify before acting.'};if(text.includes('restored')||text.includes('resolved'))return {icon:'●',klass:'',status:'RESOLVED',statusClass:'resolved',action:'No action required.'};return {icon:'i',klass:'',status:'NOTICE',statusClass:'advisory',action:'Review the notice.'}}
async function loadHealth(){
  try{const h=await api('/api/health');$('#lastUpdated').textContent=h.data_refreshed_at?friendlyTime(h.data_refreshed_at):'Refresh time unavailable';document.body.dataset.dataState=h.data_state||'unknown'}
  catch{$('#lastUpdated').textContent='Data status unavailable';document.body.dataset.dataState='unavailable'}
}
async function loadListings(){
  const q=encodeURIComponent($('#q')?.value||'');
  try{
    const rows=await api('/api/listings?q='+q);
    $('#searchContext').textContent=$('#q').value.trim()?`Results for “${$('#q').value.trim()}”.`:'Showing available verified and pending listings.';
    $('#listings').innerHTML=rows.map(r=>`<article class="listing-card"><header><div><h3>${esc(r.name)}</h3><div class="listing-meta">${esc(r.category)} · ${esc(r.area)}</div></div><span class="chip ${r.verified?'ok':'warn'}">${r.verified?'Verified':'Pending'}</span></header><p>${esc(r.description)}</p><div class="listing-meta">Accessibility: ${esc(r.accessibility)}${r.parkeasy_supported?' · ParkEasy supported':''}</div><button type="button" data-save="${r.id}">${saved.includes(r.id)?'★ Saved':'☆ Save'}</button></article>`).join('')||'<div class="loading-card">No matching community information found. Try a broader service, place or area.</div>';
    $$('[data-save]').forEach(b=>b.onclick=()=>saveItem(Number(b.dataset.save)));
  }catch(e){$('#listings').innerHTML=`<div class="loading-card">Listings unavailable: ${esc(e.message)}</div>`}
}
function renderCurrentNotices(rows){
  $('#noticesList').innerHTML=rows.map(r=>{const v=noticeVisual(r);return `<article class="notice-card"><div class="notice-symbol ${v.klass}" aria-hidden="true">${v.icon}</div><div class="notice-copy"><h3>${esc(r.title)} <span class="status-pill ${v.statusClass}">${v.status}</span></h3><p>${esc(r.body)}</p></div><div class="notice-meta"><span>◷ ${esc(shortDate(r.effective_from))}</span><span>● ${esc(r.source)}</span><span class="notice-action">${esc(v.action)}</span></div><button class="notice-chevron" type="button" data-notice-source="${esc(r.source)}" aria-label="Review notice source">›</button></article>`}).join('')||'<div class="loading-card">No immediate community notices are active right now.</div>';
  $$('[data-notice-source]').forEach(b=>b.onclick=()=>toast(`Source: ${b.dataset.noticeSource}. Full source-link integration is not available in this build.`));
}
function renderPlanning(){
  const upcomingNotices=latestNotices.filter(r=>r.temporal_state==='upcoming').map(r=>({kind:'notice',title:r.title,summary:r.body,source:r.source,from:r.effective_from,to:r.effective_to,confidence:r.confidence,timing:r.temporal_state}));
  const events=latestEvents.map(r=>({kind:'event',title:r.title,summary:r.summary,source:r.source,from:r.effective_from,to:r.effective_to,confidence:r.confidence,timing:r.temporal_state,event_type:r.event_type}));
  const rows=[...upcomingNotices,...events];
  $('#planningList').innerHTML=rows.map((r,index)=>`<article class="planning-item"><div class="planning-date">${esc(shortDate(r.from))}${r.to?`<br>to ${esc(shortDate(r.to))}`:''}</div><div class="planning-icon" aria-hidden="true">${r.kind==='event'?'▣':'!'}</div><div class="planning-copy"><h3>${esc(r.title)}</h3><p>${esc(r.summary)}</p></div><div class="planning-source"><span>Source</span><strong>${esc(r.source)}</strong><span class="${r.timing==='timing-unverified'?'':'source-verified'}">${esc(r.timing||'timing-unverified')} · ${esc(r.confidence||'confidence unavailable')}</span></div><button class="plan-button" type="button" data-plan-index="${index}">Plan⌄</button></article>`).join('')||'<div class="loading-card">No upcoming planning signals are available from the current governed data.</div>';
  $$('[data-plan-index]').forEach(b=>b.onclick=()=>toast('Calendar/reminder integration is not enabled yet. The planning signal remains available on this page.'));
}
async function loadNotices(){
  try{latestNotices=await api('/api/notices');renderCurrentNotices(latestNotices.filter(r=>r.temporal_state!=='upcoming'));renderPlanning()}
  catch(e){$('#noticesList').innerHTML=`<div class="loading-card">Notices unavailable: ${esc(e.message)}</div>`}
}
async function loadEvents(){
  try{latestEvents=await api('/api/events');renderPlanning()}
  catch(e){$('#planningList').innerHTML=`<div class="loading-card">Planning signals unavailable: ${esc(e.message)}</div>`}
}
async function loadSaved(){
  $('#savedCount').textContent=String(saved.length);
  try{const rows=await api('/api/listings');const f=rows.filter(r=>saved.includes(r.id));$('#savedList').innerHTML=f.map(r=>`<article class="saved-item"><div><h4>${esc(r.name)}</h4><small>${esc(r.category)} · ${esc(r.area)}</small></div><button type="button" data-remove="${r.id}" aria-label="Remove ${esc(r.name)} from saved">Remove</button></article>`).join('')||'<div class="loading-card">Nothing saved yet.</div>';$$('[data-remove]').forEach(b=>b.onclick=()=>saveItem(Number(b.dataset.remove)))}catch(e){$('#savedList').innerHTML=`<div class="loading-card">Saved items unavailable: ${esc(e.message)}</div>`}
}
function applySearch(term){$('#q').value=term;loadListings();$('#discovery').scrollIntoView({behavior:'smooth'});}
function setupPrototypeActions(){
  $('#btnMenu').onclick=()=>toast('The primary resident journeys are already available on this home screen; secondary menu options will be added only when needed.');
  $('#communityLocation').onclick=()=>toast('Green Meadows is the current demonstration community context. Multi-community switching is not enabled yet.');
  $('#notificationButton').onclick=()=>toast('No unread notification count is being claimed in this development build.');
  $('#voiceSearch').onclick=()=>toast('Voice search is not enabled in this development build.');
  $$('.service-shortcut[data-search],.discovery-shortcuts [data-search]').forEach(b=>b.onclick=()=>applySearch(b.dataset.search));
  $('#moreServices').onclick=()=>{$('#discovery').scrollIntoView({behavior:'smooth'});toast('Use community discovery to search the full available service directory.');};
  $('#viewAllNotices').onclick=()=>toast('All currently active notices returned by the governed API are shown here.');
  $('#viewCalendar').onclick=$('#addCalendar').onclick=()=>toast('Calendar integration is not enabled yet; EasyCommunity is not storing a personal calendar entry.');
  $('#createReminder').onclick=()=>toast('Reminder integration is not enabled yet; no personal reminder has been stored.');
  $('#sharePlanning').onclick=()=>toast('Share integration is not enabled in this development build.');
  $('#editDiscovery').onclick=()=>toast('Discovery shortcuts remain configurable by governance; resident customization is not enabled yet.');
  $('#enquireNow').onclick=()=>toast('The current listing schema does not yet expose a verified contact link. EasyCommunity will not invent one.');
  $('#clearSearch').onclick=()=>applySearch('');
  $('#q').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();loadListings();$('#discovery').scrollIntoView({behavior:'smooth'})}});
  $$('[data-scroll]').forEach(b=>b.onclick=()=>{const target=b.dataset.scroll==='global-search'?$('.global-search'):document.getElementById(b.dataset.scroll);target?.scrollIntoView({behavior:'smooth'});if(b.id==='navSearch')$('#q').focus()});
  $('#navPost').onclick=()=>toast('Resident posting/moderation workflow is not implemented in this build. No ungoverned social-feed posting is being enabled.');
  $('#navMessages').onclick=()=>toast('EasyCommunity does not provide unrestricted in-app chat in this build. Use verified external contact channels when available.');
  $('#navProfile').onclick=()=>toast('Resident profile/preferences are not yet enabled in this development build.');
}
window.addEventListener('load',()=>{setupPrototypeActions();loadHealth();loadListings();loadNotices();loadEvents();loadSaved()});
