const API = location.origin;

async function jsonOrThrow(res){
  if(!res.ok){
    const txt = await res.text().catch(()=>'');
    throw new Error(`HTTP ${res.status}: ${txt}`);
  }
  return res.json();
}

function escapeHtml(str){
  return String(str).replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));
}

/* --- CREATE --- */
async function createDevice(){
  try{
    const name = document.getElementById('d_name').value.trim();
    const firmware_version = document.getElementById('d_fw').value.trim();
    const is_on = document.getElementById('d_on').checked;
    const r = await fetch(`${API}/devices`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({name, firmware_version, is_on})
    });
    const j = await jsonOrThrow(r);
    alert(`Устройство создано (id=${j.id})`);
    document.getElementById('d_name').value='';
    document.getElementById('d_fw').value='';
    document.getElementById('d_on').checked=false;
    loadAll();
  }catch(e){ alert(e.message) }
}

async function createBattery(){
  try{
    const name = document.getElementById('b_name').value.trim();
    const nominal_voltage = parseFloat(document.getElementById('b_volt').value);
    const remaining_capacity = parseFloat(document.getElementById('b_cap').value);
    const service_life_months = parseInt(document.getElementById('b_life').value,10);
    const r = await fetch(`${API}/batteries`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({name, nominal_voltage, remaining_capacity, service_life_months})
    });
    const j = await jsonOrThrow(r);
    alert(`АКБ создана (id=${j.id})`);
    document.getElementById('b_name').value='';
    document.getElementById('b_volt').value='';
    document.getElementById('b_cap').value='';
    document.getElementById('b_life').value='';
    loadAll();
  }catch(e){ alert(e.message) }
}

/* --- LINKING --- */
async function linkSelected(){
  try{
    const did = parseInt(document.getElementById('sel_device').value,10);
    const bid = parseInt(document.getElementById('sel_battery').value,10);
    const r = await fetch(`${API}/devices/${did}/batteries/${bid}`, {method:'POST'});
    const j = await jsonOrThrow(r);
    alert(j.message || 'OK');
    loadAll();
    const v = document.getElementById('view_sel_device').value;
    if (String(did)===String(v)) viewLinks();
  }catch(e){ alert(e.message) }
}

async function viewLinks(){
  try{
    const did = parseInt(document.getElementById('view_sel_device').value,10);
    const r = await fetch(`${API}/devices/${did}/batteries`);
    const batteries = await jsonOrThrow(r);
    const box = document.getElementById('links_chips');
    box.innerHTML = batteries.map(b => `
      <label class="chip">
        <input type="checkbox" data-bid="${b.id}" style="margin-right:6px">
        #${b.id} · ${escapeHtml(b.name)}
      </label>
    `).join('');
  }catch(e){ alert(e.message) }
}

async function unlinkSelected(){
  try{
    const did = parseInt(document.getElementById('view_sel_device').value,10);
    const checks = [...document.querySelectorAll('#links_chips input[type=checkbox]:checked')];
    if(checks.length===0){ alert('Выберите хотя бы одну АКБ'); return; }
    for(const c of checks){
      const bid = parseInt(c.getAttribute('data-bid'),10);
      await fetch(`${API}/devices/${did}/batteries/${bid}`, {method:'DELETE'});
    }
    viewLinks(); loadAll();
  }catch(e){ alert(e.message) }
}

/* --- DEVICE actions --- */
async function toggleDevice(id, current){
  try{
    const r = await fetch(`${API}/devices/${id}`, {
      method:'PATCH', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({is_on: !current})
    });
    await jsonOrThrow(r);
    loadAll();
  }catch(e){ alert(e.message) }
}

async function deleteDevice(id){
  if(!confirm('Удалить устройство #' + id + '?')) return;
  try{
    const r = await fetch(`${API}/devices/${id}`, {method:'DELETE'});
    if(!r.ok && r.status!==204){
      const t = await r.text().catch(()=>'');
      throw new Error(`HTTP ${r.status}: ${t}`);
    }
    loadAll();
  }catch(e){ alert(e.message) }
}

/* --- BATTERY actions --- */
async function deleteBattery(id){
  if(!confirm('Удалить АКБ #' + id + '?')) return;
  try{
    const r = await fetch(`${API}/batteries/${id}`, {method:'DELETE'});
    if(!r.ok && r.status!==204){
      const t = await r.text().catch(()=>'');
      throw new Error(`HTTP ${r.status}: ${t}`);
    }
    loadAll();
  }catch(e){ alert(e.message) }
}

/* --- RENDER --- */
async function loadAll(){
  const [rd, rb] = await Promise.all([ fetch(`${API}/devices`), fetch(`${API}/batteries`) ]);
  const devices = await jsonOrThrow(rd);
  const batteries = await jsonOrThrow(rb);

  // selects
  const devSel = document.getElementById('sel_device');
  const viewSel = document.getElementById('view_sel_device');
  devSel.innerHTML = devices.map(d => `<option value="${d.id}">#${d.id} · ${escapeHtml(d.name)}</option>`).join('');
  viewSel.innerHTML = devSel.innerHTML;
  const batSel = document.getElementById('sel_battery');
  batSel.innerHTML = batteries.map(b => `<option value="${b.id}">#${b.id} · ${escapeHtml(b.name)}</option>`).join('');

  // fetch links for each device
  const linksByDevice = {};
  await Promise.all(devices.map(async d => {
    const r = await fetch(`${API}/devices/${d.id}/batteries`);
    linksByDevice[d.id] = (await jsonOrThrow(r)).map(b => b.id);
  }));

  // devices table
  const dBody = document.getElementById('tbl_devices');
  dBody.innerHTML = devices.map(d => {
    const ids = linksByDevice[d.id] || [];
    const toggleLabel = d.is_on ? 'Выключить' : 'Включить';
    const toggleClass = d.is_on ? 'btn-warn' : 'btn-ok';
    return `<tr>
      <td>${d.id}</td>
      <td>${escapeHtml(d.name)}</td>
      <td>${escapeHtml(d.firmware_version)}</td>
      <td>${d.is_on?'✔':''}</td>
      <td>${ids.join(', ')}</td>
      <td class="actions">
        <button class="${toggleClass}" onclick="toggleDevice(${d.id}, ${d.is_on})">${toggleLabel}</button>
        <button class="btn-danger" onclick="deleteDevice(${d.id})">Удалить</button>
      </td>
    </tr>`;
  }).join('');

  // batteries table
  const bBody = document.getElementById('tbl_batteries');
  bBody.innerHTML = batteries.map(b => `<tr>
    <td>${b.id}</td>
    <td>${escapeHtml(b.name)}</td>
    <td>${b.nominal_voltage}</td>
    <td>${b.remaining_capacity}</td>
    <td>${b.service_life_months}</td>
    <td class="actions">
      <button class="btn-danger" onclick="deleteBattery(${b.id})">Удалить</button>
    </td>
  </tr>`).join('');
}

window.addEventListener('load', loadAll);
