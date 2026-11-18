(() => {
  for (const group of document.querySelectorAll('.type-panels')) {
    const panels = [...group.querySelectorAll('.type-panel')];
    const links = [...group.previousElementSibling.querySelectorAll('a')];
    group.dataset.enhanced = 'true';
    const activate = () => {
      const selected = panels.find(panel => '#' + panel.id === location.hash) || panels[0];
      panels.forEach(panel => panel.classList.toggle('is-active', panel === selected));
      links.forEach(link => {
        if (link.hash === '#' + selected.id) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
    };
    window.addEventListener('hashchange', activate);
    activate();
  }
  for (const box of document.querySelectorAll('[data-checklist]')) {
    const key = 'hamamatsu-checklist-v1:' + box.dataset.checklist;
    const checks = [...box.querySelectorAll('input[type=checkbox]')];
    let storageAvailable = true;
    try { const values = JSON.parse(localStorage.getItem(key) || '[]'); checks.forEach((c,i)=>c.checked=values.includes(i)); } catch { storageAvailable=false; }
    const show = () => { box.querySelector('.check-progress').textContent = `${checks.filter(c=>c.checked).length} / ${checks.length} 項目を確認済み` + (storageAvailable ? '' : '（このブラウザでは保存できません）'); };
    const save = () => { try { localStorage.setItem(key,JSON.stringify(checks.flatMap((c,i)=>c.checked?[i]:[]))); } catch { storageAvailable=false; } show(); };
    checks.forEach(c=>c.addEventListener('change',save));
    box.querySelector('.check-reset').addEventListener('click',()=>{checks.forEach(c=>c.checked=false);save();});show();
  }
  const today = new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  for(const card of document.querySelectorAll('[data-end-date]')) {
    if(today>card.dataset.endDate){card.classList.add('expired');card.querySelector('.news-status').textContent='案内期間終了・記録';}
  }
  const q=document.querySelector('#directory-query'), category=document.querySelector('#directory-category');
  if(q && category){
    const rows=[...document.querySelectorAll('.directory-list li')];
    const normalize=s=>s.normalize('NFKC').toLowerCase();
    const filter=()=>{const terms=normalize(q.value).trim().split(/\s+/).filter(Boolean);let n=0;
      rows.forEach(row=>{row.hidden=!!((category.value&&row.dataset.category!==category.value)||!terms.every(t=>normalize(row.dataset.search).includes(t)));if(!row.hidden)n++;});
      document.querySelector('#directory-count').textContent=`${n}件 / 全${rows.length}件`;
      document.querySelector('#directory-empty').hidden=n!==0;
    };
    q.addEventListener('input',filter);category.addEventListener('change',filter);
    document.querySelector('.directory-clear').addEventListener('click',()=>{q.value='';category.value='';filter();q.focus();});filter();
  }
})();
