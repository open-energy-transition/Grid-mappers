<div class="page-headers">
<h1>Our Progress and Country Logbook</h1>
</div>

Welcome to our team's progress page, where you can see our mapping progress in many different countries.

:question: If you want more detailed information about each country, visit the OSM wiki page about [power networks](https://wiki.openstreetmap.org/wiki/Power_networks).

If you want to join our community, join our OSM [team](https://mapping.team/teams/1570/invitations/eec8b5f8-b212-4013-8707-96245f300fa1), and use our hashtag **#ohmygrid**!
<br>

Here are some [heatmaps](https://yosmhm.neis-one.org/) of the mapping work some of our team has done (more than 100k towers placed!):
<div style="display: flex; justify-content: space-between; gap: 20px; margin: 20px 0;">
  <img src="../images/heatmapahd.png" class="img-border" width="300">
  <img src="../images/heatmapmwi.png" class="img-border" width="300">
  <img src="../images/heatmapTA.png" class="img-border" width="300">
</div>

<!-- LOGBOOK: Add your country below the last country. Some css (in extra.css at "Hide ### from logbook") is being used to remove the ### from the table of contents so please use the same name or tell me -->

<!-- You can find country flag emojis or codes here https://www.webnots.com/copy-paste-country-flag-emoji-symbols/-->

## [**Nepal**](https://wiki.openstreetmap.org/wiki/Power_networks/Nepal) 🇳🇵 
??? success "Mapping progress"
    **Progress timeline**
    
    === "Before (April 2025)"
        ![Nepal before mapping](images/logbook/nepal-march2025.png){: .img-border }
        *April 8th, 2025*
        
    === "After (May 2025)"
        ![Nepal after mapping](images/logbook/nepal-may2025.png){: .img-border }
        *May 2, 2025*

    ### Success stories 
    - Added Nepal's largest power plant (456 MW)
    - Mapped 132kv Nepal-India interconnector
    - Finalised 400kv lines
    - Connected Pokhara-Butwal substations

    ### Key numbers 
    - **+3137** power towers added (10k total)
    - **+1120km** power lines (44% increase, as prior to our mapping, the transmission grid was 2560km)
    - **+980 MW** added capacity (1260 MW total)


<!-- End of country logbook -->
<br>
<!-- Progress Bars Section -->
## **<div class="tools-header">Community mapping progress :rocket:</div>**

<div class="progress-section"> 
   <button id="refresh-btn" style="margin-bottom:1rem;">
     🔄 Refresh stats (only click if the bars are not "loading...")
   </button>


  <div class="progress-item">
    <label>Contributors for <code>#ohmygrid</code>:</label>
    <div class="progress"> <div class="progress-bar" id="contributors-bar" style="background-color: #28a745;"></div> </div>
    <span id="contributors-count">Loading…</span>
  </div>

  <div class="progress-item">
    <label>Total Edits for <code>#ohmygrid</code>:</label>
    <div class="progress">
      <div class="progress-bar" id="edits-bar" style="background-color: #17a2b8;"></div> </div>
    <span id="edits-count">Loading…</span>
  </div>

  <div class="progress-item">
    <label>Towers mapped by our team:</label>
    <div class="progress">
      <div class="progress-bar" id="tower-bar"></div>
    </div>
    <span id="tower-count">Loading…</span>
    <br>
    <span id="tower-updated" style="font-size:0.8em; color:#666">Last updated: —</span>
  </div>
</div>


<script>

    // —— CONFIGURE THESE GOALS ——
  const CONTRIBUTORS_GOAL = 1;
  const EDITS_GOAL        = 10000;
  const TOWER_GOAL        = 10000;
   // —— UPDATE Ohsome (#ohmygrid) —— 
  async function updateOhsome() {
    const contribCountEl = document.getElementById('contributors-count');
    const editsCountEl   = document.getElementById('edits-count');
    const contribBar     = document.getElementById('contributors-bar');
    const editsBar       = document.getElementById('edits-bar');

    // set loading
    contribCountEl.textContent = 'Loading…';
    editsCountEl.textContent   = 'Loading…';
    contribBar.style.width     = '0%';
    editsBar.style.width       = '0%';

    try {
      const startDate = '2025-03-12T22:00:00Z';
      const endDate   = new Date().toISOString();
      const url       = `https://stats.now.ohsome.org/api/stats/ohmygrid?startdate=${startDate}&enddate=${endDate}`;

      const resp = await fetch(url);
      if (!resp.ok) throw new Error(resp.statusText);
      const data = await resp.json();

      // your payload is in data.result
      const users = data.result.users  ?? 0;
      const edits = data.result.edits  ?? 0;

      // write DOM
      contribCountEl.textContent = users.toLocaleString();
      editsCountEl.textContent   = edits.toLocaleString();

      contribBar.style.width = Math.min(100, users / CONTRIBUTORS_GOAL * 100) + '%';
      editsBar.style.width   = Math.min(100, edits / EDITS_GOAL        * 100) + '%';

      // cache
      localStorage.setItem('ohmygrid-ohsome', JSON.stringify({
        users, edits, ts: Date.now()
      }));
    }
    catch(err) {
      console.error('Ohsome error', err);
      contribCountEl.textContent = 'Error';
      editsCountEl.textContent   = 'Error';
    }
  }

 async function loadTowerCount() {
  const towerCountEl   = document.getElementById('tower-count');
  const towerBar       = document.getElementById('tower-bar');
  const towerUpdatedEl = document.getElementById('tower-updated');

  towerCountEl.textContent   = 'Loading…';
  towerBar.style.width       = '0%';
  towerUpdatedEl.textContent = 'Last updated: —';

  try {
    const resp = await fetch('/data/tower-count.json');
    if (!resp.ok) throw new Error(resp.statusText);
    const { towerCount: count, updated } = await resp.json();

    towerCountEl.textContent   = count.toLocaleString();
    towerBar.style.width       = Math.min(100, count / TOWER_GOAL * 100) + '%';
    towerUpdatedEl.textContent = `Last updated: ${new Date(updated).toLocaleString()}`;
  }
  catch(err) {
    console.error('Error loading tower count', err);
    towerCountEl.textContent = 'Error';
    towerUpdatedEl.textContent = '';
  }
}

    // —— MAIN & CACHE HANDLING ——
  function attemptCacheLoad(id, maxAgeMs) {
    try {
      const raw = localStorage.getItem(id);
      if (!raw) return null;
      const { ts, ...rest } = JSON.parse(raw);
      if (Date.now() - ts > maxAgeMs) return null;
      return rest;
    }
    catch { return null; }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // 1h cache
    const oneHour = 60*60*1000;

    // try Ohsome cache
    const oCache = attemptCacheLoad('ohmygrid-ohsome', oneHour);
    if (oCache) {
      // populate from cache
      document.getElementById('contributors-count').textContent = oCache.users.toLocaleString();
      document.getElementById('edits-count').textContent       = oCache.edits.toLocaleString();
      document.getElementById('contributors-bar').style.width = Math.min(100, oCache.users / CONTRIBUTORS_GOAL * 100) + '%';
      document.getElementById('edits-bar').style.width       = Math.min(100, oCache.edits / EDITS_GOAL * 100) + '%';
    } else {
      updateOhsome();
    }

    // try Towers cache
    const tCache = attemptCacheLoad('ohmygrid-towers', oneHour);
    if (tCache) {
      document.getElementById('tower-count').textContent = tCache.count.toLocaleString();
      document.getElementById('tower-bar').style.width   = Math.min(100, tCache.count / TOWER_GOAL * 100) + '%';
    } else {
      loadTowerCount();
    }

    // refresh button now refreshes both
    const btn = document.getElementById('refresh-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        localStorage.removeItem('ohmygrid-ohsome');
        localStorage.removeItem('ohmygrid-towers');
        updateOhsome();
        loadTowerCount();
      });
    }
  });
</script>

You can find more stats for #ohmygrid at [OhsomeNowstats](https://stats.now.ohsome.org/dashboard#hashtag=ohmygrid&start=2025-03-12T22:00:00Z&end=2025-05-14T21:59:59Z&interval=P1M&countries=&topics=).

##**Want to track and see your personal mapping progress (KPI)? :white_check_mark:** <br>
This [repository](https://github.com/open-energy-transition/KPI-OSM/tree/main) has a few different scripts (Overpass and Python) to measure your KPI's, as well as a [web-interface](https://open-energy-transition.github.io/KPI-OSM/). You can see how many towers you have placed and the respective line voltage, the power line length you have edited in km, the amount of MW capacity you added as a % of the country's mapped capacity, and a distribution table by voltage of substations you have added. <br>
<div style="display: flex; justify-content: left; gap: 40px; margin: 20px auto; max-width: 1200px;">
  <img src="../images/kp3.png" class="img-border" width="400">
  <img src="../images/kp4.png" class="img-border" width="400">
</div>

