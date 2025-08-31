<template>
  <main class="main_container">
    <section class="panel" role="region" aria-label="Admin Supermatches">
      <div class="panel_header admin_header">
        <h2 class="title">Supermatch History</h2>
      </div>

      <div class="sub_bar">
        <div class="status_select" role="group" aria-label="Filter status">
          <select v-model="selectedStatus" class="input select gold_select" aria-label="Status filter">
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="denied">Denied</option>
          </select>
        </div>
      </div>

      <div class="table_wrap">
        <table class="data_table" role="table">
          <thead>
            <tr>
              <th class="th_date">Date</th>
              <th class="th_icon col_submitter_icon" title="Submitter">👤</th>
              <th class="th_submitter col_submitter_name">Submitter</th>
              <th>Match</th>
              <th class="th_score">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in filteredSortedMatches" :key="m.id" class="row" @click="openModal(m)" tabindex="0" @keydown.enter="openModal(m)">
              <td class="date_cell">{{ formatDate(m.date) }}</td>
              <td class="submitter_icon_cell col_submitter_icon">
                <span class="tooltip_host" :aria-label="submitterShortLabel(m)">
                  <span class="icon_cell">{{ submitterIcon(m) }}</span>
                  <span class="tooltip">{{ submitterShortLabel(m) }}</span>
                </span>
              </td>
              <td class="submitter_name_cell col_submitter_name">
                <span class="tooltip_host" :aria-label="submitterShortLabel(m)">
                  <span class="icon_cell small">{{ submitterIcon(m) }}</span>
                  <span class="tooltip">{{ submitterShortLabel(m) }}</span>
                </span>
                <span class="submitter_name">{{ m.submitter || 'Anonymous' }}</span>
              </td>
              <td class="match_cell">
                <div class="names"><span class="winner">{{ m.winner }}</span> <span class="vs">vs</span> <span class="loser">{{ m.loser }}</span></div>
                <div class="meta"><span class="hand_chip" :class="m.hand">{{ m.hand === 'RH' ? 'Right' : 'Left' }} hand</span></div>
              </td>
              <td class="score_cell">{{ m.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="modalOpen" class="modal" role="dialog" aria-modal="true" aria-label="Match details">
      <div class="modal_content">
        <div class="modal_header">
          <div class="modal_title_group">
            <h3 class="title">Supermatch</h3>
            <div class="subtitle">{{ activeMatch.winner }} over {{ activeMatch.loser }} • {{ formatDate(activeMatch.date) }}</div>
          </div>
          <div class="header_actions">
            <span class="status_chip" :class="activeMatch.status">{{ activeMatch.status }}</span>
            <button class="close_btn" @click="closeModal" aria-label="Close">×</button>
          </div>
        </div>
        <div class="modal_body">
          <div class="section">
            <div class="section_title">Details</div>
            <div class="grid">
              <div><span class="muted">Date</span><div>{{ formatDate(activeMatch.date) }}</div></div>
              <div><span class="muted">Location</span><div>{{ activeMatch.location || '—' }}</div></div>
              <div><span class="muted">Hand</span><div><span class="hand_chip" :class="activeMatch.hand">{{ activeMatch.hand === 'RH' ? 'Right' : 'Left' }} hand</span></div></div>
              <div><span class="muted">Score</span><div>{{ activeMatch.score || '—' }}</div></div>
            </div>
          </div>
          <div class="section">
            <div class="section_title">Submission</div>
            <div class="grid">
              <div>
                <span class="muted">Submitter</span>
                <div class="submitter_line">
                  <span class="tooltip_host clickable" @click.stop="modalTipOpen = !modalTipOpen">
                    <span class="icon_cell">{{ submitterIcon(activeMatch) }}</span>
                    <span class="tooltip" :class="{ open: modalTipOpen }">{{ submitterShortLabel(activeMatch) }}</span>
                  </span>
                  <span>{{ activeMatch.submitter || 'Anonymous' }}</span>
                </div>
              </div>
              <div>
                <span class="muted">IP</span>
                <div>
                  <button class="reveal_btn" @click="activeIpRevealed = !activeIpRevealed">{{ activeIpRevealed ? activeMatch.ip : 'Reveal' }}</button>
                </div>
              </div>
              <div class="full"><span class="muted">Notes</span><div class="notes_pre">{{ activeMatch.notes || '—' }}</div></div>
            </div>
          </div>
          <div class="section">
            <div class="section_title">Competitors</div>
            <div class="grid">
              <div><span class="muted">Competitor A</span><div>{{ activeMatch.a }}</div></div>
              <div><span class="muted">A Weight</span><div>{{ activeMatch.weightA ? activeMatch.weightA + ' lbs' : '—' }}</div></div>
              <div><span class="muted">Competitor B</span><div>{{ activeMatch.b }}</div></div>
              <div><span class="muted">B Weight</span><div>{{ activeMatch.weightB ? activeMatch.weightB + ' lbs' : '—' }}</div></div>
            </div>
          </div>
          <div class="section" v-if="activeMatch.status !== 'pending'">
            <div class="section_title">Decision</div>
            <div class="grid">
              <div><span class="muted">Decided by</span><div>{{ activeMatch.decidedBy || '—' }}</div></div>
              <div><span class="muted">Decided at</span><div>{{ formatDateTime(activeMatch.decidedAt) }}</div></div>
            </div>
          </div>
        </div>
        <div class="modal_footer">
          <button class="close_footer_btn" @click="closeModal">Close</button>
          <div class="spacer"></div>
          <button class="deny_btn" @click="denyActive" :disabled="activeMatch.status==='denied'">Deny</button>
          <button class="approve_btn" @click="approveActive" :disabled="activeMatch.status==='approved'">Approve</button>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AdminSupermatches',
  data(){
    const now = Date.now()
    return {
      selectedStatus: 'pending',
      modalOpen: false,
      activeMatch: null,
      activeIpRevealed: false,
      modalTipOpen: false,
      matches: [
        // Dummy data; includes all fields + submitter metadata
        { id:'1', date: addDays(now,-1), a:'John Doe', b:'Mark Owen', winner:'John Doe', loser:'Mark Owen', hand:'RH', score:'3-1', weightA:'220', weightB:'198', location:'Portland, OR', notes:'Ref: A. Smith. Video: https://example.com/v1', submitter:'Peter', ip:'203.0.113.5', status:'pending', loggedIn:true, trust:0, isAdmin:false, _ip_revealed:false },
        { id:'2', date: addDays(now,-4), a:'Alice White', b:'Beth Green', winner:'Beth Green', loser:'Alice White', hand:'LH', score:'3-2', weightA:'144', weightB:'143', location:'Salem, OR', notes:'Event: State Qualifier', submitter:'Anonymous', ip:'198.51.100.22', status:'approved', decidedBy:'elijah@armrank', decidedAt:addDays(now,-2), loggedIn:false, trust:0, isAdmin:false, _ip_revealed:false },
        { id:'3', date: addDays(now,-7), a:'Greg Strong', b:'Tim Fast', winner:'Greg Strong', loser:'Tim Fast', hand:'RH', score:'3-0', weightA:'242', weightB:'220', location:'Eugene, OR', notes:'', submitter:'Coach T', ip:'192.0.2.77', status:'denied', decidedBy:'peter@armrank', decidedAt:addDays(now,-6), loggedIn:true, trust:2, isAdmin:false, _ip_revealed:false },
        { id:'4', date: addDays(now,-2), a:'Henry Bold', b:'Ivan Stone', winner:'Ivan Stone', loser:'Henry Bold', hand:'LH', score:'3-2', weightA:'176', weightB:'198', location:'Corvallis, OR', notes:'Close match; rematch requested', submitter:'Club Rep', ip:'203.0.113.88', status:'pending', loggedIn:true, trust:-1, isAdmin:false, _ip_revealed:false },
        { id:'5', date: addDays(now,-3), a:'Zed Power', b:'Quinn Hart', winner:'Zed Power', loser:'Quinn Hart', hand:'RH', score:'3-0', weightA:'243+', weightB:'242', location:'Bend, OR', notes:'Quick pins', submitter:'Admin Mike', ip:'203.0.113.99', status:'pending', loggedIn:true, trust:3, isAdmin:true, _ip_revealed:false },
        { id:'6', date: addDays(now,-5), a:'Leo King', b:'Oscar Flint', winner:'Oscar Flint', loser:'Leo King', hand:'LH', score:'3-1', weightA:'198', weightB:'220', location:'Medford, OR', notes:'Great crowd', submitter:'Q Guest', ip:'198.51.100.45', status:'pending', loggedIn:false, trust:0, isAdmin:false, _ip_revealed:false },
        { id:'7', date: addDays(now,-6), a:'Sam North', b:'Ray West', winner:'Sam North', loser:'Ray West', hand:'RH', score:'3-2', weightA:'176', weightB:'176', location:'Hillsboro, OR', notes:'Overtime grip set', submitter:'TrustedUser77', ip:'192.0.2.101', status:'approved', decidedBy:'elijah@armrank', decidedAt:addDays(now,-1), loggedIn:true, trust:5, isAdmin:false, _ip_revealed:false },
        { id:'8', date: addDays(now,-8), a:'Tom Rivers', b:'Kyle Moss', winner:'Kyle Moss', loser:'Tom Rivers', hand:'RH', score:'3-2', weightA:'220', weightB:'220', location:'Newberg, OR', notes:'', submitter:'FlaggedDude', ip:'192.0.2.202', status:'denied', decidedBy:'peter@armrank', decidedAt:addDays(now,-7), loggedIn:true, trust:-2, isAdmin:false, _ip_revealed:false },
      ],
    }
    function addDays(ts, days){ return ts - days*24*60*60*1000 }
  },
  computed:{
    selectedStatusLabel(){
      const map = { pending:'Pending', approved:'Approved', denied:'Denied' }
      return map[this.selectedStatus] || 'Pending'
    },
    filteredSortedMatches(){
      const want = String(this.selectedStatus || 'pending')
      return this.matches
        .filter(m => (m.status || 'pending') === want)
        .slice()
        .sort((a,b)=> b.date - a.date)
    }
  },
  methods:{
    formatDate(ts){
      try{ const d=new Date(ts); return d.toLocaleDateString('en-US',{year:'2-digit',month:'numeric',day:'numeric'}) }catch(e){ return '—' }
    },
    formatDateTime(ts){ try{ const d=new Date(ts); return d.toLocaleString('en-US',{ dateStyle:'short', timeStyle:'short' }) }catch(e){ return '—' } },
    submitterIcon(m){ if(m?.isAdmin) return '🕵️‍♂️'; if((m?.trust ?? 0) < 0) return '🚩'; if(m?.loggedIn && (m?.trust ?? 0) >= 1) return '👥'; if(m?.loggedIn) return '👤'; return '🌚' },
    submitterIconLabel(m){ if(m?.isAdmin) return 'Admin'; if((m?.trust ?? 0) < 0) return 'Flagged (trust < 0)'; if(m?.loggedIn && (m?.trust ?? 0) >= 1) return 'Logged in, trusted (trust ≥ 1)'; if(m?.loggedIn) return 'Logged in'; return 'Anonymous (not logged in)' },
    submitterShortLabel(m){ if(m?.isAdmin) return 'Admin'; if((m?.trust ?? 0) < 0) return 'Flagged'; if(m?.loggedIn && (m?.trust ?? 0) >= 1) return 'Trusted'; if(m?.loggedIn) return 'Logged in'; return 'Anonymous' },
    openModal(m){ this.activeMatch = { ...m }; this.modalOpen = true; this.activeIpRevealed = false },
    closeModal(){ this.modalOpen = false; this.activeMatch = null; this.activeIpRevealed = false },
    toggleIp(m){ m._ip_revealed = !m._ip_revealed },
    approveActive(){ if(!this.activeMatch) return; this.setStatus('approved') },
    denyActive(){ if(!this.activeMatch) return; this.setStatus('denied') },
    setStatus(status){
      const idx = this.matches.findIndex(x=>x.id===this.activeMatch.id)
      if(idx>=0){
        const decidedBy = 'admin@beta'
        const decidedAt = Date.now()
        this.matches.splice(idx,1,{ ...this.activeMatch, status, decidedBy, decidedAt })
        this.activeMatch.status = status
        this.activeMatch.decidedBy = decidedBy
        this.activeMatch.decidedAt = decidedAt
      }
    },
  }
}
</script>

<style scoped>
.main_container{width:min(1200px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}
.admin_header{display:flex;align-items:center;justify-content:space-between}
.controls{display:flex;gap:12px;align-items:center}
.field.compact{display:grid;gap:6px}
.select{appearance:none;border:1px solid var(--border);border-radius:10px;background:rgba(255,255,255,.02);color:var(--text);padding:8px 10px;min-width:180px}
.select:focus{outline:none;border-color:rgba(215,180,58,.55)}
.select option{background:#0b1630;color:var(--text);padding:6px}
.select optgroup{background:#0b1630;color:var(--muted)}
.sub_bar{position:sticky; top:0; z-index:5; background:var(--header-bg); border-bottom:1px solid var(--border); padding:10px 16px; display:flex; align-items:center; gap:12px}
.table_wrap{overflow:visible; height:auto; max-height:none;}
.data_table{width:100%;max-width:100%;border-collapse:collapse;font-size:15px; table-layout:auto}
.data_table thead th{background:var(--header-bg);color:var(--muted);text-align:left;padding:10px 12px;border-bottom:1px solid var(--border)}
.data_table thead th.th_date{width:92px}
.data_table thead th.th_icon{width:56px;text-align:center}
.data_table thead th.th_score{width:86px}
.data_table tbody td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.data_table tbody tr{cursor:pointer}
.data_table tbody tr:hover td{background:rgba(10,23,64,.35)}
.data_table tbody tr:nth-child(odd) td{ background:rgba(255,255,255,.02) }
.data_table tbody tr:nth-child(even) td{ background:rgba(255,255,255,.01) }
.match_cell{display:flex;flex-direction:column;gap:6px;min-width:0}
.names{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-weight:900}
.names .winner{color:#20c997;text-shadow:0 0 12px rgba(32,201,151,.18)}
.names .vs{color:var(--muted);font-weight:900}
.names .loser{color:#ff9b91;text-shadow:0 0 12px rgba(231,76,60,.18)}
.meta{display:flex;gap:8px;align-items:center}
.hand_chip{display:inline-flex;align-items:center;justify-content:center;padding:3px 8px;border-radius:999px;border:1px solid var(--border);background:rgba(255,255,255,.04);font-weight:800;font-size:12px}
.hand_chip.RH{background:linear-gradient(180deg,#20c997,#17a2b8);color:#061626;border-color:transparent}
.hand_chip.LH{background:linear-gradient(180deg,#2ea6ff,#1e90ff);color:#061626;border-color:transparent}
.date_cell{white-space:nowrap}
.score_cell{font-weight:900}
.submitter_icon_cell{text-align:center}
.submitter_line{display:flex;align-items:center;gap:8px}
.submitter_icon{display:inline-flex;width:26px;height:26px;align-items:center;justify-content:center;border-radius:8px;border:1px solid var(--border);background:rgba(255,255,255,.03)}
.icon_cell{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:8px;border:1px solid var(--border);background:rgba(255,255,255,.03)}
.icon_cell.small{width:20px;height:20px;margin-right:6px}
.col_submitter_icon{ display:none }
.tooltip_host{position:relative;display:inline-flex;align-items:center;justify-content:center}
.tooltip{position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);white-space:nowrap;padding:6px 8px;border-radius:8px;border:1px solid var(--border);background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.98));color:var(--text);font-weight:800;font-size:12px;opacity:0;pointer-events:none;transition:opacity .15s ease}
.tooltip_host:hover .tooltip{opacity:1}
.tooltip.open{opacity:1}
.tooltip_host.clickable{cursor:pointer}
.status_chip{display:inline-block;padding:4px 10px;border-radius:999px;border:1px solid var(--border);font-weight:900;text-transform:capitalize}
.status_chip.pending{background:rgba(255,255,255,.04)}
.status_chip.approved{background:linear-gradient(180deg,#20c997,#17a2b8);color:#061626;border-color:transparent}
.status_chip.denied{background:linear-gradient(180deg,#e74c3c,#c0392b)}
.reveal_btn{display:inline-flex;align-items:center;justify-content:center;padding:6px 10px;border-radius:999px;border:1px solid var(--border);background:transparent;color:var(--muted);font-weight:800;cursor:pointer}
.modal{position:fixed;left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.45);z-index:60}
.modal_content{width:min(820px,94vw);max-height:88vh;background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.98));border:1px solid var(--border);border-radius:14px;box-shadow:var(--glow);display:flex;flex-direction:column;overflow:hidden}
.modal_header{position:sticky;top:0;display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border);background:linear-gradient(180deg, rgba(11,22,48,1), rgba(8,18,40,1));z-index:1}
.modal_title_group{display:flex;flex-direction:column;gap:4px}
.subtitle{color:var(--muted);font-weight:700}
.header_actions{display:flex;align-items:center;gap:10px}
.close_btn{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;border:1px solid var(--border);background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.04));color:var(--text);font-weight:900;cursor:pointer}
.close_btn:hover{filter:brightness(1.08)}
.modal_body{padding:14px 16px;overflow:auto}
.section{display:grid;gap:10px;margin-bottom:14px}
.section_title{font-weight:900}
.modal_footer{display:flex;align-items:center;gap:10px;padding:12px 16px;border-top:1px solid var(--border);background:linear-gradient(180deg, rgba(11,22,48,1), rgba(8,18,40,1))}
.modal_footer .spacer{flex:1}
.close_footer_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid var(--border);background:linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.06));color:var(--muted);font-weight:900;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.grid .full{grid-column:1/-1}
.muted{color:var(--muted);font-weight:700}
.notes_pre{white-space:pre-wrap}

/* Gold select styled like rankings pill but squarer */
.gold_select{position:relative; appearance:none; border:2px solid var(--accent); background:transparent; color:var(--text); padding:8px 34px 8px 12px; border-radius:10px; font-weight:900}
.status_select{position:relative}
.status_select::after{content:"\25BE"; position:absolute; right:12px; top:50%; transform:translateY(-50%); color:var(--accent); pointer-events:none; font-size:14px}
.approve_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(23,162,184,.55);background:linear-gradient(180deg,#20c997,#17a2b8);color:#061626;font-weight:900}
.deny_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:linear-gradient(180deg, rgba(231,76,60,.18), rgba(231,76,60,.14));color:#ffe6e3;font-weight:900}
/* Hide scrollbars universally while keeping scroll */
html, body, .modal, .panel, .wrap, .rows_grid, .member_list, .table_wrap, .modal_body{
  -ms-overflow-style: none;
  scrollbar-width: none;
}
html::-webkit-scrollbar,
body::-webkit-scrollbar,
.modal::-webkit-scrollbar,
.panel::-webkit-scrollbar,
.wrap::-webkit-scrollbar,
.rows_grid::-webkit-scrollbar,
.member_list::-webkit-scrollbar,
.table_wrap::-webkit-scrollbar,
.modal_body::-webkit-scrollbar{ display:none }

@media (max-width:720px){
  .grid{ grid-template-columns:1fr }
  .data_table thead th{ padding:8px 10px }
  .data_table tbody td{ padding:8px 10px }
  .names{ gap:4px }
  .hand_chip{ padding:3px 8px }
  .col_submitter_name{ display:none }
  .col_submitter_icon{ display:table-cell }
}
</style>

