<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')" role="dialog" aria-modal="true" :aria-label="athlete || 'Athlete details'">
    <div class="modal">
      <div class="modal_header">
        <h2 class="modal_title">{{ athlete }}</h2>
        <div class="spacer"></div>
        <button class="close_btn" @click="$emit('close')" aria-label="Close">×</button>
      </div>

      <div class="content">
        <!-- Arm-specific stats: Left on the left, Right on the right -->
        <div class="hero alt_hero vg_theme arm_hero">
          <div class="arm_card left_arm">
            <div class="arm_title">Left Hand</div>
            <div class="row">
              <div class="label">Fake Skill Level</div>
              <div class="value"><span class="accent">{{ fakeSkill('LH') }}</span></div>
            </div>
            <div class="row">
              <div class="label">Weight Class Rank</div>
              <div class="value">{{ formatRank(lh_class_rank) }}</div>
            </div>
            <div class="row">
              <div class="label">Overall Rank</div>
              <div class="value">{{ formatRank(lh_rank) }}</div>
            </div>
          </div>
          <div class="arm_card right_arm">
            <div class="arm_title">Right Hand</div>
            <div class="row">
              <div class="label">Fake Skill Level</div>
              <div class="value"><span class="accent">{{ fakeSkill('RH') }}</span></div>
            </div>
            <div class="row">
              <div class="label">Weight Class Rank</div>
              <div class="value">{{ formatRank(rh_class_rank) }}</div>
            </div>
            <div class="row">
              <div class="label">Overall Rank</div>
              <div class="value">{{ formatRank(rh_rank) }}</div>
            </div>
          </div>
        </div>

        <!-- General non-arm stats (full width) -->
        <div class="block alt_hero vg_theme general_block">
          <div class="rows">
            <div class="row">
              <div class="label">Skill Points</div>
              <div class="value"><span class="accent">{{ points }}</span></div>
            </div>
            <div class="row">
              <div class="label">Division</div>
              <div class="value">{{ division }}</div>
            </div>
            <div class="row">
              <div class="label">Weight Class</div>
              <div class="value">{{ weight }} lbs</div>
            </div>
            <div class="row" v-if="club || isDeveloper()">
              <div class="label">Club</div>
              <div class="value badge_line">
                <template v-if="club">
                  <span v-if="club_logo" class="club_logo" :style="{ backgroundImage: `url(${club_logo})` }" aria-hidden="true"></span>
                  <span>{{ club }}</span>
                  <span v-if="club_leader" class="badge_btn crown" :class="{ show: open_tip_key === 'popup-crown' }" @click.stop="toggleTip('popup-crown')" tabindex="0" @keyup.enter.stop="toggleTip('popup-crown')" :aria-label="club">
                    <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                    <span class="tip">{{ club }}</span>
                  </span>
                </template>
                <span v-if="isDeveloper()" class="badge_btn dev_crown" :class="{ show: open_tip_key === 'popup-dev' }" @click.stop="toggleTip('popup-dev')" tabindex="0" @keyup.enter.stop="toggleTip('popup-dev')" aria-label="Developer">
                  <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                  <span class="tip">Developer</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <section class="badge_rail">
          <h3 class="rail_title">Badges</h3>
          <div class="rail">
            <div class="rail_inner">
              <!-- RH overall badge -->
              <span v-if="trophyType(rh_rank)" class="badge_item trophy" :class="'trophy_' + rh_rank" :aria-label="trophyTip('RH', rh_rank)">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/></svg>
                <span class="trophy_num" aria-hidden="true">{{ rh_rank }}</span>
                <span class="tip">{{ trophyTip('RH', rh_rank) }}</span>
              </span>
              <span v-else-if="isTopTen(rh_rank)" class="badge_item rank_badge" :class="topTenClass('RH')" :aria-label="trophyTip('RH', rh_rank)">
                <span class="badge_text">{{ rh_rank }}</span>
                <span class="tip">{{ trophyTip('RH', rh_rank) }}</span>
              </span>

              <!-- LH overall badge -->
              <span v-if="trophyType(lh_rank)" class="badge_item trophy" :class="'trophy_' + lh_rank" :aria-label="trophyTip('LH', lh_rank)">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/></svg>
                <span class="trophy_num" aria-hidden="true">{{ lh_rank }}</span>
                <span class="tip">{{ trophyTip('LH', lh_rank) }}</span>
              </span>
              <span v-else-if="isTopTen(lh_rank)" class="badge_item rank_badge" :class="topTenClass('LH')" :aria-label="trophyTip('LH', lh_rank)">
                <span class="badge_text">{{ lh_rank }}</span>
                <span class="tip">{{ trophyTip('LH', lh_rank) }}</span>
              </span>

              <!-- RH class badge -->
              <span v-if="trophyType(rh_class_rank)" class="badge_item trophy" :class="'trophy_' + rh_class_rank" :aria-label="classTrophyTip('RH', rh_class_rank)">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/></svg>
                <span class="trophy_num" aria-hidden="true">{{ rh_class_rank }}</span>
                <span class="tip">{{ classTrophyTip('RH', rh_class_rank) }}</span>
              </span>
              <span v-else-if="isTopTen(rh_class_rank)" class="badge_item rank_badge" :class="topTenClass('RH')" :aria-label="classTrophyTip('RH', rh_class_rank)">
                <span class="badge_text">{{ rh_class_rank }}</span>
                <span class="tip">{{ classTrophyTip('RH', rh_class_rank) }}</span>
              </span>

              <!-- LH class badge -->
              <span v-if="trophyType(lh_class_rank)" class="badge_item trophy" :class="'trophy_' + lh_class_rank" :aria-label="classTrophyTip('LH', lh_class_rank)">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/></svg>
                <span class="trophy_num" aria-hidden="true">{{ lh_class_rank }}</span>
                <span class="tip">{{ classTrophyTip('LH', lh_class_rank) }}</span>
              </span>
              <span v-else-if="isTopTen(lh_class_rank)" class="badge_item rank_badge" :class="topTenClass('LH')" :aria-label="classTrophyTip('LH', lh_class_rank)">
                <span class="badge_text">{{ lh_class_rank }}</span>
                <span class="tip">{{ classTrophyTip('LH', lh_class_rank) }}</span>
              </span>

              <!-- Club leader badge if applicable -->
              <span v-if="club" class="badge_item badge_btn crown" :class="{ show: open_tip_key === 'popup-crown-rail' }" @click.stop="toggleTip('popup-crown-rail')" tabindex="0" @keyup.enter.stop="toggleTip('popup-crown-rail')" :aria-label="club">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                <span class="tip">{{ club }}</span>
              </span>
              <span v-if="isDeveloper()" class="badge_item badge_btn dev_crown" :class="{ show: open_tip_key === 'popup-dev-rail' }" @click.stop="toggleTip('popup-dev-rail')" tabindex="0" @keyup.enter.stop="toggleTip('popup-dev-rail')" aria-label="Developer">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                <span class="tip">Developer</span>
              </span>
            </div>
            <div class="rail_edge left"></div>
            <div class="rail_edge right"></div>
          </div>
        </section>
      </div>

      <div class="actions_bottom">
        <button class="close_action_btn" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AthleteDetails',
  props: {
    open: { type: Boolean, default: false },
    athlete: { type: String, default: '' },
    division: { type: String, default: '' },
    weight: { type: String, default: '' },
    rh_rank: { type: [String, Number], default: '' },
    lh_rank: { type: [String, Number], default: '' },
    rh_class_rank: { type: [String, Number], default: '' },
    lh_class_rank: { type: [String, Number], default: '' },
    club: { type: String, default: '' },
    club_logo: { type: String, default: '' },
    club_leader: { type: Boolean, default: false },
    points: { type: [String, Number], default: 48 },
  },
  data(){
    return { open_tip_key: '' }
  },
  computed: {
    isTopThree(){
      const r = Number(this.rh_rank)
      const l = Number(this.lh_rank)
      const vals = [r, l].filter(n => Number.isFinite(n) && n > 0)
      if(vals.length === 0) return false
      return Math.min(...vals) <= 3
    }
  },
  methods:{
    // TODO: implement real skill level computation once model is ready
    fakeSkill(hand){
      const rank = hand === 'RH' ? Number(this.rh_rank) : Number(this.lh_rank)
      if(!Number.isFinite(rank) || rank <= 0) return '—'
      return Math.max(0, 60 - rank)
    },
    isDeveloper(){
      return String(this.athlete || '').trim().toLowerCase() === 'elijah mason'
    },
    formatRank(r){
      if(r === '' || r === null || r === undefined) return '—'
      const n = Number(r)
      return Number.isFinite(n) && n > 0 ? `#${n}` : '—'
    },
    isTopTen(rank){
      const n = Number(rank)
      return Number.isFinite(n) && n >= 1 && n <= 10
    },
    topTenClass(hand){
      // style variant like clubs: alternate tint (we reuse .top10_a/.top10_b names)
      return hand === 'RH' ? 'top10_a' : 'top10_b'
    },
    trophyType(rank){
      const n = Number(rank)
      return Number.isFinite(n) && n >= 1 && n <= 3
    },
    classTrophyTip(hand, rank){
      const h = hand === 'LH' ? 'Left Hand' : 'Right Hand'
      const n = Number(rank)
      if(!Number.isFinite(n) || n < 1) return `${h} class ranking`
      if(n === 1) return `#1 ${h} (class)`
      return `#${n} ${h} (class)`
    },
    trophyTip(hand, rank){
      const h = hand === 'LH' ? 'Left Hand' : 'Right Hand'
      const n = Number(rank)
      if(!Number.isFinite(n) || n < 1) return `${h} ranking`
      if(n === 1) return `#1 ${h}`
      return `#${n} ${h}`
    },
    toggleTip(k){ this.open_tip_key = this.open_tip_key === k ? '' : k }
  }
}
</script>

<style scoped>
.overlay{position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:flex-start; justify-content:center; padding:16px; z-index:100; overflow:auto; -webkit-overflow-scrolling:touch}
.modal{width:min(720px,100%); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); border:1px solid var(--border); border-radius:16px; box-shadow:var(--glow); overflow:auto; max-height:calc(100vh - 32px)}
.modal_header{display:flex; align-items:center; justify-content:flex-start; gap:10px; padding:14px 16px; border-bottom:1px solid var(--border)}
.modal_title{margin:0}
.spacer{flex:1}
/* Header close button matches ClubDetails */
.close_btn{background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.04)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:6px 12px; cursor:pointer; font-size:20px; line-height:1; transition:.18s ease}
.close_btn:hover{filter:brightness(1.08)}
.content{padding:12px 16px}
.hero{display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr)); gap:10px; margin-bottom:10px}
.arm_hero{ grid-template-columns:repeat(2, minmax(140px,1fr)) }
.arm_card{ background:rgba(255,255,255,.04); border:1px solid var(--border); border-radius:10px; padding:10px }
.arm_card .arm_title{ font-weight:900; margin-bottom:8px }
.arm_card .row{ display:flex; align-items:center; justify-content:space-between; gap:10px; margin:6px 0 }
.alt_hero{background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.015)); border:1px solid var(--border); border-radius:12px; padding:12px}
.vg_theme{ position:relative; overflow:hidden }
.vg_theme::before{ content:""; position:absolute; inset:-40px; background:radial-gradient(220px 120px at 20% -10%, rgba(215,180,58,.18), transparent 60%), radial-gradient(220px 120px at 120% 110%, rgba(20,130,150,.18), transparent 60%); pointer-events:none }
.stat{background:rgba(255,255,255,.04); border:1px solid var(--border); border-radius:10px; padding:10px}
.label{color:var(--muted); font-weight:700}
.value{font-weight:900; display:flex; align-items:center; gap:8px}
.value.badge_line{ display:flex; align-items:center; gap:8px }
.accent{color:var(--accent)}
.grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(260px,1fr)); gap:14px}
.block{background:rgba(255,255,255,.02); border:1px solid var(--border); border-radius:12px; padding:12px}
.block h3{margin:0 0 8px 0}
.rows{display:flex; flex-direction:column; gap:8px}
.row{display:flex; gap:10px; align-items:center; justify-content:space-between}
.row .label{color:var(--muted); font-weight:700}
.list{margin:0; padding-left:18px}
.actions_bottom{ display:flex; justify-content:flex-end; padding:12px 16px; border-top:1px solid var(--border) }
.close_action_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; cursor:pointer}

/* Badge Wall */
/* Video-game-like horizontal badge rail */
.badge_rail{ position:relative; background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.015)); border:1px solid var(--border); border-radius:12px; padding:12px; margin-top:10px; overflow:visible }
.rail_title{ margin:0 0 8px 0 }
.rail{ position:relative; background:linear-gradient(90deg, rgba(215,180,58,.08), rgba(12,100,120,.08)); border:1px dashed rgba(255,255,255,.12); border-radius:10px; padding:10px 12px; overflow:visible }
.rail_inner{ display:flex; align-items:center; gap:12px; min-width:max-content }
.rail_edge{ position:absolute; top:40px; bottom:12px; width:20px; pointer-events:none; background:linear-gradient(90deg, rgba(11,22,48,0), rgba(11,22,48,.8)) }
.rail_edge.left{ left:12px; transform:rotate(180deg) }
.rail_edge.right{ right:12px }
.badge_item{ position:relative; display:inline-flex; align-items:center; justify-content:center }
.badge_item.trophy{ width:34px; height:34px }
.badge_item .tip{ position:absolute; bottom:calc(100% + 6px); left:0; background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:6px 8px; font-weight:800; font-size:12px; opacity:0; pointer-events:none; transition:opacity .16s ease; white-space:nowrap }
.badge_item:hover .tip{ opacity:1 }
.rank_badge{ display:inline-flex; align-items:center; justify-content:center; min-width:28px; height:28px; padding:0 8px; border-radius:999px; font-weight:900; font-size:12px; position:relative }
.rank_badge.top10_a{background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)); color:var(--accent); border:1px solid rgba(215,180,58,.35)}
.rank_badge.top10_b{background:rgba(255,255,255,.12); color:#9fb0d0; border:1px solid rgba(255,255,255,.18)}

/* Crown badge + tooltip */
.icon{width:18px; height:18px}
.club_logo{ width:22px; height:22px; border-radius:50%; background-size:cover; background-position:center; border:1px solid var(--border) }
.badge_btn{ position:relative; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:999px }
.crown{background:linear-gradient(180deg, rgba(215,180,58,.2), rgba(185,147,34,.18)); color:var(--accent); border:1px solid rgba(215,180,58,.45)}
.crown_icon{fill:currentColor}
.dev_crown{ background:linear-gradient(180deg, rgba(150,60,215,.22), rgba(120,40,185,.18)); color:#b68cff; border:1px solid rgba(182,140,255,.45) }
.badge_btn .tip{ position:absolute; bottom:calc(100% + 8px); left:0; right:auto; transform:translateX(0) translateY(6px); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:8px 10px; display:inline-block; min-width:0; width:max-content; max-width:min(78vw, 320px); white-space:normal; overflow-wrap:anywhere; word-break:normal; text-align:left; font-weight:800; font-size:12px; box-shadow:var(--glow); opacity:0; pointer-events:none; transition:opacity .16s ease, transform .16s ease; z-index:2 }
.badge_btn .tip::after{ content:""; position:absolute; top:100%; left:14px; transform:translateX(0); width:0; height:0; border-left:6px solid transparent; border-right:6px solid transparent; border-top:6px solid var(--border) }
.badge_btn:hover .tip, .badge_btn.show .tip{ opacity:1; transform:translateX(0) translateY(0); pointer-events:auto }

/* Trophy styles mirrored from leaderboard */
.trophy{ position:relative; display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px }
.trophy svg{ width:34px; height:34px; display:block }
.trophy_1 svg{ fill: var(--accent) }
.trophy_2 svg{ fill: var(--silver) }
.trophy_3 svg{ fill: var(--bronze) }
.trophy_num{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:14px; color:#0b1630; text-shadow:0 1px 0 rgba(255,255,255,.45); transform: translateY(-6px); pointer-events:none }
.rank_badges{ display:inline-flex; align-items:center; gap:8px }
</style>

