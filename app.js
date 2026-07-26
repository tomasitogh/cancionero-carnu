// ─── BUILT-IN COLLECTIONS ────────────────────────────────────────────
const BUILTIN = [{
  id:'iglesia', name:'Iglesia', sub:'Pascua Joven San Isidro',
  emoji:'⛪', color:'#00838f', readonly:true, songs:SONGS
}];

// ─── STATE ───────────────────────────────────────────────────────────
let S = {
  view:'home', col:null, colTab:'songs',
  song:null, songIdx:null,
  sl:null, slPos:0,
  delta:0, showChords:true, fontSize:14,
  addToSl:null,  // setlist we're adding songs to
  scrollTimer:null, touchX:0
};

// ─── PERSISTENCE ─────────────────────────────────────────────────────
let darkMode = localStorage.getItem('cjsi_dark')==='1';
const hist = JSON.parse(localStorage.getItem('cjsi_hist')||'{}');
let userCols = JSON.parse(localStorage.getItem('cjsi_cols')||'[]');
// pls stored per collection: cjsi_pls_{colId}
function getPls(colId){ return JSON.parse(localStorage.getItem('cjsi_pls_'+colId)||'[]'); }
function savePls(colId,pls){ localStorage.setItem('cjsi_pls_'+colId, JSON.stringify(pls)); }
function saveHist(){ localStorage.setItem('cjsi_hist', JSON.stringify(hist)); }
function saveCols(){ localStorage.setItem('cjsi_cols', JSON.stringify(userCols)); }
function allCols(){ return [...BUILTIN, ...userCols]; }

// ─── DARK MODE ───────────────────────────────────────────────────────
function applyDark(){ document.documentElement.setAttribute('data-dark', darkMode?'1':''); }
function toggleDark(){ darkMode=!darkMode; localStorage.setItem('cjsi_dark',darkMode?'1':''); applyDark(); }
applyDark();

// ─── TRANSPOSITION ───────────────────────────────────────────────────
const NOTES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
const ENH={Db:1,Eb:3,Fb:4,Gb:6,Ab:8,Bb:10,Cb:11};
function nIdx(n){ const i=NOTES.indexOf(n); return i>=0?i:(ENH[n]??-1); }
function trNote(n,d){ const i=nIdx(n); return i<0?n:NOTES[((i+d)%12+12)%12]; }
function trChord(ch,d){
  const m=ch.match(/^([A-G][#b]?)(.*?)(\/[A-G][#b]?)?$/);
  if(!m)return ch;
  return trNote(m[1],d)+(m[2]||'')+(m[3]?'/'+trNote(m[3].slice(1),d):'');
}
function trLine(line,d){
  if(!d||!line.trim())return line;
  const re=/[A-G][#b]?(?:m(?:aj)?|dim|aug|sus[24]?|add\d+)?(?:M?[0-9]*)(?:\/[A-G][#b]?)?/g;
  const hits=[]; let m;
  while((m=re.exec(line))!==null){ if(/^[A-G]/.test(m[0]))hits.push({i:m.index,s:m[0]}); }
  let res=line;
  for(let k=hits.length-1;k>=0;k--){ const {i,s}=hits[k]; res=res.slice(0,i)+trChord(s,d)+res.slice(i+s.length); }
  return res;
}
function capoHint(song, d){
  if(!d)return'';
  const dn=((d%12)+12)%12;
  if(dn===0)return'';
  if(dn<=7)return'Capo '+dn+' con acordes de '+song.k;
  return'Bajar '+(12-dn)+' semitono'+(12-dn>1?'s':'');
}
function curKey(){ const i=nIdx(S.song.k); return i<0?S.song.k:NOTES[((i+S.delta)%12+12)%12]; }

// ─── NAVIGATION ──────────────────────────────────────────────────────
function goBack(){
  if(S.addToSl){ S.addToSl=null; renderSlEdit(); return; }
  if(S.view==='song'){ S.sl?renderSlPlay():renderCol(); return; }
  if(S.view==='sl-edit'){ renderCol(); return; }
  if(S.view==='sl-play'){ renderSlEdit(); return; }
  if(S.view==='add-col'){ renderHome(); return; }
  renderHome();
}

function updateHdr(title, sub, showBack){
  document.getElementById('hdr-title').textContent = title;
  document.getElementById('hdr-sub').textContent = sub||'';
  document.getElementById('hdr-sub').hidden = !sub;
  document.getElementById('hdr-back').hidden = !showBack;
}

function setMain(html){ document.getElementById('main').innerHTML=html; window.scrollTo(0,0); }

// ─── HOME ─────────────────────────────────────────────────────────────
function renderHome(){
  S.view='home'; S.col=null; S.sl=null;
  stopScroll();
  updateHdr('CANCIONERO','PASCUA JOVEN SAN ISIDRO',false);
  const cols = allCols();
  let cards = cols.map((c,i)=>`
    <div class="col-card" onclick="openCol('${c.id}')">
      <div class="col-stripe" style="background:${c.color||'var(--acc)'}"></div>
      <div class="col-emoji">${c.emoji||'🎵'}</div>
      <div class="col-name">${esc(c.name)}</div>
      ${c.sub?`<div class="col-sub">${esc(c.sub)}</div>`:''}
      <div class="col-count">${c.songs.length} canción${c.songs.length!==1?'es':''}</div>
      ${!c.readonly?`<span onclick="event.stopPropagation();deleteCol('${c.id}')" style="position:absolute;top:8px;right:8px;font-size:16px;color:var(--danger);padding:4px">✕</span>`:''}
    </div>`).join('');
  cards += `<div class="col-card col-new" onclick="renderAddCol()"><span>+</span><span>Nueva colección</span></div>`;
  setMain(`<div class="section"><div class="col-grid">${cards}</div><div class="safe-b"></div></div>`);
}

function openCol(id){
  const col = allCols().find(c=>c.id===id);
  if(!col)return;
  S.col=col; S.colTab='songs'; S.addToSl=null;
  renderCol();
}

// ─── COLLECTION ───────────────────────────────────────────────────────
function renderCol(){
  S.view='col'; S.sl=null;
  stopScroll();
  updateHdr(S.col.name, S.col.sub||'', true);
  renderColContent();
}

function renderColContent(){
  const tab = S.colTab;
  let content = `
    <div class="section">
      <div class="tabs">
        <button class="tab ${tab==='songs'?'on':''}" onclick="switchColTab('songs')">Canciones</button>
        <button class="tab ${tab==='sl'?'on':''}" onclick="switchColTab('sl')">Setlists</button>
      </div>
      <div id="col-tab-content"></div>
    </div>`;
  setMain(content);
  renderColTab();
}

function switchColTab(t){ S.colTab=t; renderColTab(); }

function renderColTab(){
  const el=document.getElementById('col-tab-content');
  if(!el)return;
  if(S.colTab==='songs') el.innerHTML=buildSongsTab();
  else el.innerHTML=buildSlTab();
}

function buildSongsTab(){
  if(!S.col.songs.length) return `<div class="empty">Sin canciones.<br><br>
    <button class="btn btn-outline btn-sm" onclick="renderAddSongForm()">+ Agregar canción</button></div>`;
  let rows = S.col.songs.map((s,i)=>`
    <div class="srow" onclick="openSong(${i})">
      <span class="rnum">${s.n}</span>
      <span class="rname">${esc(s.t)}${s.a?'<br><span style="font-size:11px;color:var(--text2)">'+esc(s.a)+'</span>':''}</span>
      <span class="rkey">${s.k}${s.c?' c.'+s.c:''}</span>
    </div>`).join('');
  const addBtn = !S.col.readonly?`<button class="btn btn-dashed mt12" onclick="renderAddSongForm()">+ Agregar canción</button>`:'';
  return `<input class="srch" placeholder="Buscar…" oninput="filterSongs(this.value)">
    <div id="songs-list">${rows}</div>${addBtn}<div class="safe-b"></div>`;
}

function filterSongs(q){
  const el=document.getElementById('songs-list'); if(!el)return;
  const ql=q.toLowerCase();
  el.querySelectorAll('.srow').forEach(r=>{
    r.hidden = q&&!r.querySelector('.rname').textContent.toLowerCase().includes(ql);
  });
}

function buildSlTab(){
  const pls = getPls(S.col.id);
  let cards = pls.length ? pls.map((pl,i)=>`
    <div class="slcard" onclick="openSlEdit(${i})">
      <div class="slcard-name">${esc(pl.name)}</div>
      <div class="slcard-ct">${pl.songs.length} tema${pl.songs.length!==1?'s':''}</div>
      <button class="sldel" onclick="event.stopPropagation();deleteSl(${i})">✕</button>
    </div>`).join('') : `<div class="empty">Sin setlists todavía.</div>`;
  return `<button class="btn btn-dashed mb12" onclick="newSl()">+ Nueva setlist</button>${cards}<div class="safe-b"></div>`;
}

// ─── SETLIST ─────────────────────────────────────────────────────────
function newSl(){
  const name=prompt('Nombre del setlist:'); if(!name||!name.trim())return;
  const pls=getPls(S.col.id);
  pls.push({id:Date.now(),name:name.trim(),songs:[]});
  savePls(S.col.id,pls);
  openSlEdit(pls.length-1);
}
function deleteSl(i){
  if(!confirm('¿Eliminar este setlist?'))return;
  const pls=getPls(S.col.id); pls.splice(i,1); savePls(S.col.id,pls);
  switchColTab('sl'); renderColTab();
}
function openSlEdit(i){
  const pls=getPls(S.col.id); S.sl=pls[i]; S.view='sl-edit';
  renderSlEdit();
}
function renderSlEdit(){
  S.addToSl=null;
  updateHdr(S.sl.name,'',true);
  const pls=getPls(S.col.id);
  let items = S.sl.songs.length ? S.sl.songs.map((si,pos)=>{
    const s=S.col.songs[si];
    return `<div class="sl-item">
      <span style="font-size:12px;color:var(--text2);min-width:18px">${pos+1}</span>
      <span class="sl-item-name">${s.n}. ${esc(s.t)}</span>
      <span class="sl-item-key">${s.k}${s.c?' c.'+s.c:''}</span>
      <button class="mvbtn" onclick="slMove(${pos},-1)" ${pos===0?'disabled':''}>↑</button>
      <button class="mvbtn" onclick="slMove(${pos},1)" ${pos===S.sl.songs.length-1?'disabled':''}>↓</button>
      <button class="rmbtn" onclick="slRemove(${pos})">✕</button>
    </div>`;
  }).join('') : `<div class="empty">Sin canciones.<br>Usá el botón de abajo.</div>`;

  setMain(`<div class="section">
    <div class="row-btns mt12">
      <button class="btn btn-primary btn-sm" style="flex:1" onclick="playSlFrom(0)">▶ Tocar</button>
      <button class="btn btn-outline btn-sm" style="flex:1" onclick="openAddSongs()">+ Canciones</button>
    </div>
    ${items}
    <div class="safe-b"></div>
  </div>`);
}

function slMove(pos,dir){
  const sl=S.sl; const arr=sl.songs;
  if(pos+dir<0||pos+dir>=arr.length)return;
  [arr[pos],arr[pos+dir]]=[arr[pos+dir],arr[pos]];
  const pls=getPls(S.col.id); const idx=pls.findIndex(p=>p.id===sl.id);
  if(idx>=0){pls[idx]=sl; savePls(S.col.id,pls);}
  renderSlEdit();
}
function slRemove(pos){
  S.sl.songs.splice(pos,1);
  const pls=getPls(S.col.id); const idx=pls.findIndex(p=>p.id===S.sl.id);
  if(idx>=0){pls[idx]=S.sl; savePls(S.col.id,pls);}
  renderSlEdit();
}
function openAddSongs(){
  S.addToSl=S.sl; S.view='add-songs';
  updateHdr('Agregar canciones',S.col.name,true);
  let rows = S.col.songs.map((s,i)=>{
    const inSl=S.sl.songs.includes(i);
    return `<div class="srow" onclick="toggleSong(${i})">
      <span class="rnum">${s.n}</span>
      <span class="rname">${esc(s.t)}</span>
      <span class="raction" id="ra${i}">${inSl?'✓':'+'}</span>
    </div>`;
  }).join('');
  setMain(`<div class="section mt12">${rows}<div class="safe-b"></div></div>`);
}
function toggleSong(i){
  const sl=S.sl; const inSl=sl.songs.includes(i);
  if(inSl) sl.songs=sl.songs.filter(x=>x!==i); else sl.songs.push(i);
  const pls=getPls(S.col.id); const idx=pls.findIndex(p=>p.id===sl.id);
  if(idx>=0){pls[idx]=sl; savePls(S.col.id,pls);}
  const el=document.getElementById('ra'+i); if(el) el.textContent=sl.songs.includes(i)?'✓':'+';
}
function playSlFrom(pos){
  if(!S.sl.songs.length){alert('El setlist está vacío.');return;}
  S.slPos=pos; openSong(S.sl.songs[pos]);
}

// ─── SONG VIEW ───────────────────────────────────────────────────────
function openSong(idx){
  S.songIdx=idx; S.song=S.col.songs[idx];
  S.delta=hist[(S.col.id+'-'+S.song.n)]??0;
  S.showChords=true; S.fontSize=14;
  S.view='song';
  pushURL(S.col.id, S.song.n);
  renderSongView();
}
function renderSongView(){
  stopScroll();
  const s=S.song; const inSl=!!S.sl;
  updateHdr(s.n+'. '+s.t,'',true);

  const shareBtn = `<button class="sv-navbtn" onclick="shareSong()" title="Compartir">🔗</button>`;
  const navHtml = shareBtn + (inSl ? `
    <div class="sv-nav" style="margin-left:auto">
      ${S.slPos>0?`<button class="sv-navbtn" onclick="slNav(-1)">&#8592;</button>`:''}
      <span class="sv-counter">${S.slPos+1} / ${S.sl.songs.length}</span>
      ${S.slPos<S.sl.songs.length-1?`<button class="sv-navbtn" onclick="slNav(1)">&#8594;</button>`:''}
    </div>` : '');

  setMain(`
    <div class="sv-hdr">${navHtml}</div>
    <div class="section">
      <div class="card mt12">
        <div style="font-size:19px;font-weight:700;text-align:center;margin-bottom:3px">${esc(s.t)}</div>
        ${s.a?`<div style="font-size:12px;color:var(--text2);text-align:center;margin-bottom:12px">${esc(s.a)}</div>`:'<div style="height:12px"></div>'}
        <div class="ctrl" id="ctrl-row">
          <span class="ctrl-label">TONO:</span>
          <span class="key-disp" id="kd">${curKey()}${s.c?' (capo '+s.c+')':''}</span>
          <span class="capo-pill" id="cp" ${!S.delta?'hidden':''}>${capoHint(s,S.delta)}</span>
          <button class="cbt" onclick="shiftKey(-1)">&#8722;1</button>
          <button class="cbt" onclick="shiftKey(+1)">+1</button>
          <div class="ml-auto" style="display:flex;gap:6px;align-items:center">
            <span style="font-size:12px;color:var(--text2)">A</span>
            <button class="cbt" onclick="chSz(-1)" style="padding:6px 9px">&#8722;</button>
            <button class="cbt" onclick="chSz(+1)" style="padding:6px 9px">+</button>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">
          <label class="tgl-wrap">
            <label class="tgl"><input type="checkbox" id="cht" checked onchange="toggleChords(this.checked)"><span class="tgl-tr"></span><span class="tgl-th"></span></label>
            <span class="tgl-lbl">Acordes</span>
          </label>
        </div>
        <div class="kbar" id="kbar"></div>
        <div class="ascroll">
          <label>Scroll</label>
          <input type="range" id="spd" min="1" max="10" value="3">
          <button class="ascroll-btn" id="scbtn" onclick="toggleScroll()">&#9654;</button>
        </div>
        <div id="sb"></div>
        ${inSl?`<p class="swipe-hint">← deslizá para navegar →</p>`:''}
      </div>
      <div class="safe-b"></div>
    </div>`);

  buildKbar(); renderBody();
  // Swipe for setlist nav
  if(inSl){
    const main=document.getElementById('main');
    main.addEventListener('touchstart',e=>{S.touchX=e.touches[0].clientX;},{passive:true});
    main.addEventListener('touchend',e=>{
      const dx=e.changedTouches[0].clientX-S.touchX;
      if(Math.abs(dx)>60){ if(dx<0)slNav(1); else slNav(-1); }
    },{passive:true});
  }
}
function slNav(d){
  const np=S.slPos+d;
  if(np<0||np>=S.sl.songs.length)return;
  S.slPos=np; openSong(S.sl.songs[np]);
}
function shiftKey(d){
  S.delta=((S.delta+d)%12+12)%12;
  hist[S.col.id+'-'+S.song.n]=S.delta; saveHist();
  updateKdisp(); renderBody();
}
function chSz(d){
  S.fontSize=Math.max(11,Math.min(20,S.fontSize+d));
  const sb=document.getElementById('sb'); if(sb) sb.style.fontSize=S.fontSize+'px';
}
function toggleChords(on){ S.showChords=on; renderBody(); }
function toggleScroll(){
  const btn=document.getElementById('scbtn'); if(!btn)return;
  if(S.scrollTimer){ stopScroll(); btn.textContent='▶'; btn.classList.remove('on'); }
  else{ btn.textContent='⏸'; btn.classList.add('on');
    S.scrollTimer=setInterval(()=>{ const spd=parseInt(document.getElementById('spd')?.value||3); window.scrollBy(0,spd*0.4); },50); }
}
function stopScroll(){ if(S.scrollTimer){clearInterval(S.scrollTimer);S.scrollTimer=null;} }
function updateKdisp(){
  const kn=curKey(); const s=S.song;
  const kd=document.getElementById('kd'); if(kd) kd.textContent=kn+(s.c?' (capo '+s.c+')':'');
  const cp=document.getElementById('cp'); if(cp){ const h=capoHint(s,S.delta); cp.textContent=h; cp.hidden=!h; }
  document.querySelectorAll('.kb').forEach(b=>b.classList.toggle('on',b.dataset.n===kn));
}
function buildKbar(){
  const bar=document.getElementById('kbar'); if(!bar)return;
  bar.innerHTML=NOTES.map(n=>`<button class="kb${n===curKey()?' on':''}" data-n="${n}" onclick="setKey('${n}')">${n}</button>`).join('');
}
function setKey(n){
  const orig=nIdx(S.song.k); const i=NOTES.indexOf(n);
  let d=((i-orig)%12+12)%12; if(d>6)d-=12;
  S.delta=d; hist[S.col.id+'-'+S.song.n]=d; saveHist();
  updateKdisp(); renderBody();
}
function renderBody(){
  const sb=document.getElementById('sb'); if(!sb)return;
  sb.innerHTML=''; sb.style.fontSize=S.fontSize+'px';
  if(!S.song.i||!S.song.i.length){ sb.innerHTML='<div style="color:var(--text2);text-align:center;padding:20px">Sin letra disponible</div>'; return; }
  for(const item of S.song.i){
    const el=document.createElement('span');
    if(item.t==='g'){el.className='gl';}
    else if(item.t==='s'){el.className='sl2';el.textContent=item.x;}
    else{
      if(S.showChords&&item.c&&item.c.trim()){
        const cl=document.createElement('span');cl.className='cl';cl.textContent=trLine(item.c,S.delta);sb.appendChild(cl);
      }
      el.className='ll';el.textContent=item.y;
    }
    sb.appendChild(el);
  }
}

// ─── ADD COLLECTION ───────────────────────────────────────────────────
const EMOJIS=['🎵','🎸','🎹','🎺','🎻','🥁','🎶','🎤','⛪','🏔️','🌊','🌟','🙏','✝️','🎭','🎪'];
const COLORS=['#00838f','#e53935','#8e24aa','#1e88e5','#43a047','#f4511e','#6d4c41','#546e7a'];
let nc={emoji:'🎵',color:COLORS[0]};
function renderAddCol(){
  S.view='add-col';
  updateHdr('Nueva colección','',true);
  const em=EMOJIS.map(e=>`<div class="emoji-opt${nc.emoji===e?' on':''}" onclick="pickEmoji('${e}')">${e}</div>`).join('');
  const sw=COLORS.map(c=>`<div class="swatch${nc.color===c?' on':''}" style="background:${c}" onclick="pickColor('${c}')"></div>`).join('');
  setMain(`<div class="section mt12 card">
    <div class="lbl">Emoji</div>
    <div class="emoji-grid mb12">${em}</div>
    <div class="lbl">Color</div>
    <div class="swatch-row mb12">${sw}</div>
    <div class="lbl">Nombre</div>
    <input class="inp mb12" id="nc-name" placeholder="Ej: Rock, Misa, Pop…">
    <div class="lbl">Subtítulo (opcional)</div>
    <input class="inp mb12" id="nc-sub" placeholder="Ej: Años 80-90">
    <button class="btn btn-primary mt8" onclick="createCol()">Crear colección</button>
    <div class="safe-b"></div>
  </div>`);
}
function pickEmoji(e){nc.emoji=e;document.querySelectorAll('.emoji-opt').forEach(el=>el.classList.toggle('on',el.textContent===e));}
function pickColor(c){nc.color=c;document.querySelectorAll('.swatch').forEach(el=>el.classList.toggle('on',el.style.background===c));}
function createCol(){
  const name=document.getElementById('nc-name')?.value.trim();
  if(!name){alert('Ingresá un nombre.');return;}
  const sub=document.getElementById('nc-sub')?.value.trim()||'';
  const col={id:'u'+Date.now(),name,sub,emoji:nc.emoji,color:nc.color,readonly:false,songs:[]};
  userCols.push(col); saveCols(); nc={emoji:'🎵',color:COLORS[0]};
  renderHome();
}
function deleteCol(id){
  if(!confirm('¿Eliminar esta colección?'))return;
  userCols=userCols.filter(c=>c.id!==id); saveCols(); renderHome();
}

// ─── ADD SONG TO COLLECTION ───────────────────────────────────────────
function renderAddSongForm(){
  updateHdr('Agregar canción',S.col.name,true);
  setMain(`<div class="section mt12 card">
    <div class="lbl">Título</div>
    <input class="inp mb12" id="ns-t" placeholder="Nombre de la canción">
    <div class="lbl">Artista / Autor (opcional)</div>
    <input class="inp mb12" id="ns-a" placeholder="Ej: Hillsong, Marcos Witt…">
    <div class="lbl">Tono</div>
    <div class="kbar mb12" style="margin-bottom:16px">
      ${NOTES.map(n=>`<button class="kb${n==='G'?' on':''}" onclick="pickSongKey('${n}')" id="nsk-${n.replace('#','s')}">${n}</button>`).join('')}
    </div>
    <input type="hidden" id="ns-k" value="G">
    <div class="lbl">Link de Spotify (opcional)</div>
    <input class="inp mb12" id="ns-sp" placeholder="https://open.spotify.com/track/…">
    <button class="btn btn-primary mt8" onclick="saveNewSong()">Agregar</button>
    <div class="safe-b"></div>
  </div>`);
}
function pickSongKey(n){
  document.getElementById('ns-k').value=n;
  document.querySelectorAll('[id^=nsk-]').forEach(b=>b.classList.remove('on'));
  document.getElementById('nsk-'+n.replace('#','s'))?.classList.add('on');
}
function saveNewSong(){
  const t=document.getElementById('ns-t')?.value.trim();
  if(!t){alert('Ingresá un título.');return;}
  const s={n:S.col.songs.length+1,t,a:document.getElementById('ns-a')?.value.trim()||'',
    k:document.getElementById('ns-k')?.value||'G',c:null,i:[],
    sp:document.getElementById('ns-sp')?.value.trim()||''};
  // Update in userCols
  const uc=userCols.find(c=>c.id===S.col.id);
  if(uc){uc.songs.push(s);saveCols();}
  S.col.songs.push(s); // update local ref
  renderCol();
}

// ─── HELPERS ─────────────────────────────────────────────────────────
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// ─── URL SHARING ─────────────────────────────────────────────────────
function pushURL(colId, songNum){
  try{ history.pushState({}, '', location.pathname+'?col='+encodeURIComponent(colId)+'&song='+songNum); }catch(e){}
}
function shareSong(){
  const url = location.href;
  const btn = document.querySelector('[onclick="shareSong()"]');
  if(navigator.share){ navigator.share({title:S.song.t, url}); }
  else if(navigator.clipboard){ navigator.clipboard.writeText(url).then(()=>{
    if(btn){const o=btn.textContent;btn.textContent='✓';setTimeout(()=>btn.textContent=o,1500);}
  }); }
  else{ prompt('Copiá este link:', url); }
}
function initFromURL(){
  const p = new URLSearchParams(location.search);
  const colId = p.get('col');
  const songNum = parseInt(p.get('song'));
  if(colId && !isNaN(songNum)){
    const col = allCols().find(c=>c.id===colId);
    if(col){
      const idx = col.songs.findIndex(s=>s.n===songNum);
      if(idx>=0){ S.col=col; openSong(idx); return; }
    }
  }
  renderHome();
}

// ─── INIT ─────────────────────────────────────────────────────────────
initFromURL();


