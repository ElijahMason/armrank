<template>
  <main class="main_container">
    <section class="panel" role="region" aria-label="Admin Supermatches">
      <div class="panel_header admin_header">
        <h2 class="title">Admin • Supermatches</h2>
        <div class="controls">
          <label class="field compact">
            <span class="label">Status</span>
            <select v-model="selectedStatus" class="input select">
              <option value="pending">Pending approval</option>
              <option value="approved">Approved</option>
              <option value="denied">Denied</option>
            </select>
          </label>
        </div>
      </div>

      <div class="table_wrap">
        <table class="data_table" role="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Winner</th>
              <th>Loser</th>
              <th>Hand</th>
              <th>Score</th>
              <th>A Weight</th>
              <th>B Weight</th>
              <th>Location</th>
              <th>Notes</th>
              <th>Submitter</th>
              <th>IP</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in filteredSortedMatches" :key="m.id" class="row" @click="openModal(m)" tabindex="0" @keydown.enter="openModal(m)">
              <td>{{ formatDate(m.date) }}</td>
              <td>{{ m.winner }}</td>
              <td>{{ m.loser }}</td>
              <td>{{ m.hand }}</td>
              <td>{{ m.score }}</td>
              <td>{{ m.weightA || '—' }}</td>
              <td>{{ m.weightB || '—' }}</td>
              <td>{{ m.location || '—' }}</td>
              <td class="notes_cell">{{ m.notes || '—' }}</td>
              <td>{{ m.submitter || 'Anonymous' }}</td>
              <td>
                <button class="reveal_btn" @click.stop="toggleIp(m)">{{ m._ip_revealed ? m.ip : 'Reveal' }}</button>
              </td>
              <td>
                <span class="status_chip" :class="m.status">{{ m.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section v-if="modalOpen" class="modal" role="dialog" aria-modal="true" aria-label="Match details">
      <div class="modal_content">
        <div class="modal_header">
          <h3 class="title">Supermatch Details</h3>
          <button class="close_btn" @click="closeModal" aria-label="Close">×</button>
        </div>
        <div class="modal_body">
          <div class="grid">
            <div><span class="muted">Date</span><div>{{ formatDate(activeMatch.date) }}</div></div>
            <div><span class="muted">Hand</span><div>{{ activeMatch.hand }}</div></div>
            <div><span class="muted">Score</span><div>{{ activeMatch.score || '—' }}</div></div>
            <div><span class="muted">Location</span><div>{{ activeMatch.location || '—' }}</div></div>
            <div><span class="muted">Competitor A</span><div>{{ activeMatch.a }}</div></div>
            <div><span class="muted">A Weight</span><div>{{ activeMatch.weightA || '—' }}</div></div>
            <div><span class="muted">Competitor B</span><div>{{ activeMatch.b }}</div></div>
            <div><span class="muted">B Weight</span><div>{{ activeMatch.weightB || '—' }}</div></div>
            <div><span class="muted">Winner</span><div>{{ activeMatch.winner }}</div></div>
            <div><span class="muted">Loser</span><div>{{ activeMatch.loser }}</div></div>
            <div><span class="muted">Submitter</span><div>{{ activeMatch.submitter || 'Anonymous' }}</div></div>
            <div><span class="muted">IP</span>
              <div>
                <button class="reveal_btn" @click="activeIpRevealed = !activeIpRevealed">{{ activeIpRevealed ? activeMatch.ip : 'Reveal' }}</button>
              </div>
            </div>
            <div class="full"><span class="muted">Notes</span><div class="notes_pre">{{ activeMatch.notes || '—' }}</div></div>
            <div><span class="muted">Status</span><div><span class="status_chip" :class="activeMatch.status">{{ activeMatch.status }}</span></div></div>
            <div v-if="activeMatch.status !== 'pending'"><span class="muted">Decided by</span><div>{{ activeMatch.decidedBy || '—' }}</div></div>
            <div v-if="activeMatch.status !== 'pending'"><span class="muted">Decided at</span><div>{{ formatDateTime(activeMatch.decidedAt) }}</div></div>
          </div>
        </div>
        <div class="modal_footer">
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
      matches: [
        // Dummy data; includes all fields from submission form
        { id:'1', date: addDays(now,-1), a:'John Doe', b:'Mark Owen', winner:'John Doe', loser:'Mark Owen', hand:'RH', score:'3-1', weightA:'220', weightB:'198', location:'Portland, OR', notes:'Ref: A. Smith. Video: https://example.com/v1', submitter:'Peter', ip:'203.0.113.5', status:'pending', _ip_revealed:false },
        { id:'2', date: addDays(now,-4), a:'Alice White', b:'Beth Green', winner:'Beth Green', loser:'Alice White', hand:'LH', score:'3-2', weightA:'144', weightB:'143', location:'Salem, OR', notes:'Event: State Qualifier', submitter:'Anonymous', ip:'198.51.100.22', status:'approved', decidedBy:'elijah@armrank', decidedAt:addDays(now,-2), _ip_revealed:false },
        { id:'3', date: addDays(now,-7), a:'Greg Strong', b:'Tim Fast', winner:'Greg Strong', loser:'Tim Fast', hand:'RH', score:'3-0', weightA:'242', weightB:'220', location:'Eugene, OR', notes:'', submitter:'Coach T', ip:'192.0.2.77', status:'denied', decidedBy:'peter@armrank', decidedAt:addDays(now,-6), _ip_revealed:false },
        { id:'4', date: addDays(now,-2), a:'Henry Bold', b:'Ivan Stone', winner:'Ivan Stone', loser:'Henry Bold', hand:'LH', score:'3-2', weightA:'176', weightB:'198', location:'Corvallis, OR', notes:'Close match; rematch requested', submitter:'Club Rep', ip:'203.0.113.88', status:'pending', _ip_revealed:false },
      ],
    }
    function addDays(ts, days){ return ts - days*24*60*60*1000 }
  },
  computed:{
    filteredSortedMatches(){
      const want = String(this.selectedStatus || 'pending')
      return this.matches
        .filter(m => (m.status || 'pending') === want)
        .slice()
        .sort((a,b)=> b.date - a.date)
    }
  },
  methods:{
    formatDate(ts){ try{ const d=new Date(ts); return d.toISOString().slice(0,10) }catch(e){ return '—' } },
    formatDateTime(ts){ try{ const d=new Date(ts); return d.toLocaleString() }catch(e){ return '—' } },
    openModal(m){ this.activeMatch = { ...m }; this.modalOpen = true; this.activeIpRevealed = false },
    closeModal(){ this.modalOpen = false; this.activeMatch = null; this.activeIpRevealed = false },
    toggleIp(m){ m._ip_revealed = !m._ip_revealed },
    approveActive(){ if(!this.activeMatch) return; this.setStatus('approved') },
    denyActive(){ if(!this.activeMatch) return; this.setStatus('denied') },
    setStatus(status){
      const idx = this.matches.findIndex(x=>x.id===this.activeMatch.id)
      if(idx>=0){
        const decidedBy = 'admin@beta' // dummy; would be current admin identity
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
.select{appearance:none}
.table_wrap{overflow:auto}
.data_table{width:100%;border-collapse:separate;border-spacing:0}
.data_table thead th{position:sticky;top:0;background:var(--header-bg);text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);font-weight:800}
.data_table tbody td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
.data_table tbody tr{cursor:pointer}
.data_table tbody tr:hover{background:rgba(255,255,255,.03)}
.status_chip{display:inline-block;padding:4px 8px;border-radius:999px;border:1px solid var(--border);font-weight:800;text-transform:capitalize}
.status_chip.pending{background:rgba(255,255,255,.04)}
.status_chip.approved{background:linear-gradient(180deg,#20c997,#17a2b8);color:#061626;border-color:transparent}
.status_chip.denied{background:linear-gradient(180deg,#e74c3c,#c0392b)}
.notes_cell{max-width:320px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.reveal_btn{display:inline-flex;align-items:center;justify-content:center;padding:6px 10px;border-radius:999px;border:1px solid var(--border);background:transparent;color:var(--muted);font-weight:800;cursor:pointer}
.modal{position:fixed;left:0;top:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.45);z-index:60}
.modal_content{width:min(760px,92vw);background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.98));border:1px solid var(--border);border-radius:14px;box-shadow:var(--glow);overflow:hidden}
.modal_header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border)}
.modal_body{padding:14px 16px}
.modal_footer{display:flex;justify-content:flex-end;gap:10px;padding:12px 16px;border-top:1px solid var(--border)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.grid .full{grid-column:1/-1}
.muted{color:var(--muted);font-weight:700}
.notes_pre{white-space:pre-wrap}
.approve_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(23,162,184,.55);background:linear-gradient(180deg,#20c997,#17a2b8);color:#061626;font-weight:900}
.deny_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:linear-gradient(180deg, rgba(231,76,60,.18), rgba(231,76,60,.14));color:#ffe6e3;font-weight:900}
@media (max-width:720px){ .grid{ grid-template-columns:1fr } }
</style>

