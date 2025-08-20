<template>
	<main class="main_container">
		<section class="panel" role="region" aria-label="Oregon Clubs">
			<div class="panel_header"><h2 class="title">Find a club to train with <span class="new_badge">NEW</span></h2></div>
			<div v-if="is_loading" class="clubs_grid skeletons">
				<div v-for="n in 6" :key="'sk'+n" class="club_card sk">
					<div class="club_hero sk_box"></div>
					<div class="club_body">
						<div class="club_head">
							<div class="sk_line w40"></div>
							<div class="sk_pill w20"></div>
						</div>
						<div class="club_meta">
							<div class="sk_line w30"></div>
							<div class="sk_line w30"></div>
						</div>
						<div class="lt_spacer"></div>
						<div class="stats">
							<div class="sk_pill w30"></div>
							<div class="sk_pill w20"></div>
							<div class="sk_pill w30"></div>
						</div>
					</div>
				</div>
			</div>
			<div v-else class="clubs_grid" :class="{ is_ready: !is_loading }">
				<div v-for="(c, i) in clubs_sorted" :key="i" class="club_card" @click="openClub(c)" role="button" :aria-label="`Open ${c.name}`" tabindex="0" @keyup.enter="openClub(c)">
					<div class="club_hero" aria-hidden="true">
						<img class="club_img" :src="resolveImage(c.image_url || 'default_club.png')" loading="lazy" alt="" v-img-loaded />
						<div class="hero_overlay"></div>
					</div>
					<div class="club_body">
						<div class="club_head">
							<h3 class="club_name">{{ c.name }}</h3>
							<span class="open_badge" title="Open to new members">Open</span>
						</div>
						<div class="club_meta">
							<div class="loc">{{ c.city }} • {{ c.region }}</div>
							<div class="leader" v-if="c.leaders?.length">Leader: {{ (c.leaders || []).join(', ') }}</div>
						</div>
						<div class="lt_spacer"></div>
						<div class="stats">
							<span class="badge members">{{ c.members_count || memberCount(c.name) }} members</span>
							<span v-if="isActive(c)" class="badge active">Active</span>
							<span v-if="hasWeeklyPractice(c)" class="badge weekly">Weekly practice</span>
							<span v-if="isOutOfState(c)" class="badge out_of_state">Out of state</span>
							<span v-if="c.founded" class="badge founded">Founded {{ c.founded }}</span>
						</div>
					</div>
				</div>
			</div>
			<div v-if="!is_loading && clubs_sorted.length === 0" class="empty_state" role="status" aria-live="polite">
				<div class="empty_title">No clubs match your filters</div>
				<div class="empty_sub">Try clearing filters or checking back later as clubs are added.</div>
				<button class="cta_btn" @click="clearFilters">Clear filters</button>
			</div>
			<div class="panel_footer">
				<div class="add_callout">
					Missing a club? <router-link class="link" :to="{ name: 'leaderboards', query:{ goto:'feedback' } }">Send an update</router-link>.
				</div>
			</div>
			<ClubDetails
				:open="details_open"
				:club="selected || {}"
				:rankings_tab_name_men="rankings_tab_name"
				:weights_tab_name_men="weights_tab_name"
				:rankings_tab_name_women="rankings_tab_name_women"
				:weights_tab_name_women="weights_tab_name_women"
				:classes_men="classes"
				:classes_women="classes_women"
				:max_initial_members="5"
				@close="details_open=false"
			/>
		</section>
	</main>
</template>

<script>
import ClubDetails from '../components/ClubDetails.vue'
export default {
	components:{ ClubDetails },
	directives:{
		imgLoaded:{
			mounted(el){
				const onLoad=()=>{ el.classList.add('is_loaded') }
				if(el.complete){ onLoad() }
				el.addEventListener('load', onLoad, { once:true })
			}
		}
	},
	data(){
		// Google Sheet for club membership (first row = club names, columns list members in order)
		const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
		const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
		const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()
		return {
			is_loading:true,
			only_oregon:false,
			selected:null,
			details_open:false,
			sheet_id_raw,
			sheet_id,
			club_membership: new Map(),
			rankings_tab_name: 'Rankings',
			weights_tab_name: 'Weights',
			rankings_tab_name_women: 'Rankings_F',
			weights_tab_name_women: 'Weights_F',
			classes: ['154','176','198','220','242','243+'],
			classes_women: ['143','144+'],
			// rank/weight maps for computing talent metrics
			rank_left_men_cls: new Map(),
			rank_right_men_cls: new Map(),
			rank_left_women_cls: new Map(),
			rank_right_women_cls: new Map(),
			weight_men: new Map(),
			weight_women: new Map(),
			club_talent_map: new Map(),
			medals_footer_map: new Map(),
			clubs: [
				{ name: 'Brute Squad', city: 'Portland', region: 'Portland Metro', leaders: ['Mark Owen'], verified: true, image_url: 'https://m.media-amazon.com/images/M/MV5BODUzZThmOGQtYjJlZS00NTRhLTllOWEtNjU4NWQ4OTQxODE1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', training:['Weekly practice'], avg_practice_size:17, desc:'Meets Sundays at 4:00pm.', members_count:80, leader_footer: { num:'4x', tail:' World Champion' }, city_medal_rank:1, medals_this_year:159, supermatches_hosted:13 },
				{ name: 'Strong Arms', city: 'Salem', region: 'Willamette Valley', leaders: ['Jacob Abbot'], verified: true, image_url: null, training:['Weekly practice'] },
				{ name: 'Grip Titans', city: 'Roseburg', region: 'Southern Oregon', leaders: ['Peter Lalande'], verified: true, image_url: null, members_count:65, training:['Friday nights'], avg_practice_size:15, medals_this_year:40 },
				{ name: 'Wrist Crackers', city: 'Tri-Cities', region: 'Washington', leaders: ['Beaumont Zunker'], verified: true, image_url: null, members_count:40, out_of_state:true },
				{ name: 'Capital City Grippers', city: 'Salem', region: 'Willamette Valley', leaders: [], verified: true, image_url: null, members_count:12, training:['Fridays 5:30pm'], desc:'Meets Fridays at 5:30pm.' },
				{ name: 'Amity Wrist Breakers', city: 'Amity', region: 'Willamette Valley', leaders: ['Nicolas Mode'], verified: true, image_url: null, members_count:49 },
			],
		}
	},
	computed:{
		clubs_filtered(){
			return this.clubs.filter(c => this.only_oregon ? !this.isOutOfState(c) : true)
		},
		clubs_sorted(){
			return this.clubs_filtered.slice().sort((a,b)=>{
				const ao = this.isOutOfState(a)
				const bo = this.isOutOfState(b)
				if(ao !== bo) return ao - bo
				return (b.members_count||0) - (a.members_count||0)
			})
		},
	},
	methods:{
		clearFilters(){ this.only_oregon = false },
		resolveImage(path){
			const base = (import.meta && import.meta.env && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/'
			const p = String(path || '').trim()
			if(!p) return base + 'default_club.png'
			if(/^https?:\/\//i.test(p)) return p
			return base + p.replace(/^\//,'')
		},
		gvizCsv(tab){
			return `https://docs.google.com/spreadsheets/d/${this.sheet_id}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(tab)}`
		},
		csvToRows(csv) {
			return csv
				.trim()
				.split(/\r?\n/)
				.map(line => {
					const out = []
					let cur = ''
					let q = false
					for (let i = 0; i < line.length; i++) {
						const ch = line[i]
						if (ch === '"') { q = !q; continue }
						if (ch === ',' && !q) { out.push(cur); cur = '' } else { cur += ch }
					}
					out.push(cur)
					return out.map(s => s.trim())
				})
		},
		async loadMembership(){
			try{
				const csv = await fetch(this.gvizCsv('Clubs')).then(r=>r.text())
				const rows = this.csvToRows(csv)
				const header = rows[0] || []
				const clubNames = header.map(h=>String(h||'').trim()).filter(Boolean)
				const membersByClub = new Map(clubNames.map(n=>[n, []]))
				for(let i=1;i<rows.length;i++){
					const r = rows[i]
					for(let j=0;j<clubNames.length;j++){
						const name = String(r[j] || '').trim()
						if(!name) continue
						membersByClub.get(clubNames[j]).push(name)
					}
				}
				this.club_membership = membersByClub
				this.computeTalentMetrics()
			}catch(e){ /* ignore */ }
		},
		membersOf(clubName){
			return this.club_membership.get(clubName) || []
		},
		memberCount(clubName){
			return this.membersOf(clubName).length
		},
		async loadRanks(){
			try{
				const [rm, wm, rw, ww] = await Promise.all([
					fetch(this.gvizCsv(this.rankings_tab_name)).then(r=>r.text()),
					fetch(this.gvizCsv(this.weights_tab_name)).then(r=>r.text()),
					fetch(this.gvizCsv(this.rankings_tab_name_women)).then(r=>r.text()),
					fetch(this.gvizCsv(this.weights_tab_name_women)).then(r=>r.text()),
				])
				const rankRowsM = this.csvToRows(rm)
				const rankRowsW = this.csvToRows(rw)
				const weightRowsM = this.csvToRows(wm)
				const weightRowsW = this.csvToRows(ww)
				// weight maps
				this.weight_men = this.makeWeightMap(weightRowsM, this.classes)
				this.weight_women = this.makeWeightMap(weightRowsW, this.classes_women)
				// class rank maps
				this.rank_left_men_cls = this.makeClassRankIndex(rankRowsM, 0, this.weight_men)
				this.rank_right_men_cls = this.makeClassRankIndex(rankRowsM, 2, this.weight_men)
				this.rank_left_women_cls = this.makeClassRankIndex(rankRowsW, 0, this.weight_women)
				this.rank_right_women_cls = this.makeClassRankIndex(rankRowsW, 2, this.weight_women)
				this.computeTalentMetrics()
			}catch(e){ /* ignore */ }
		},
		makeWeightMap(rows, classes){
			const map = new Map()
			rows.slice(1).forEach(r=>{
				const name = (r[0] || '').trim()
				if(!name) return
				const raw = r[1]
				const str = raw === undefined ? '' : String(raw).trim()
				const lbs = str === '' ? '' : Number(str)
				map.set(name, this.weightClass(lbs, classes))
			})
			return map
		},
		weightClass(lbs, classes){
			const top = classes[classes.length - 1]
			if (lbs === '' || lbs === null || Number.isNaN(Number(lbs))) return top
			const w = Number(lbs)
			if (w === -1) return top
			const thresholds = classes.filter(c=>!c.includes('+')).map(Number).sort((a,b)=>a-b)
			for (const t of thresholds){ if(w <= t) return String(t) }
			return top
		},
		makeClassRankIndex(rows, nameCol, weightMap){
			const out = new Map()
			const perClassCounts = new Map()
			rows.slice(1).forEach(r=>{
				const name = (r[nameCol] || '').trim()
				if(!name) return
				const cls = weightMap.get(name)
				if(!cls) return
				const next = (perClassCounts.get(cls) || 0) + 1
				perClassCounts.set(cls, next)
				out.set(name, next)
			})
			return out
		},
		computeTalentMetrics(){
			// prerequisites
			if(this.clubs.length === 0 || this.club_membership.size === 0 || (this.weight_men.size === 0 && this.weight_women.size === 0)) return
			const labelFor = (key)=> key === 'light' ? 'Lightweight talent' : key === 'middle' ? 'Middleweight talent' : key === 'heavy' ? 'Heavyweight talent' : 'Superheavyweight talent'
			const perClubBest = new Map()
			for(const c of this.clubs){
				const members = this.membersOf(c.name)
				const countsMen = Object.create(null)
				const countsWomen = Object.create(null)
				for(const m of members){
					const name = String(m || '').trim()
					if(!name) continue
					const clsM = this.weight_men.get(name)
					if(clsM){
						const lm = this.rank_left_men_cls.get(name)
						const rm = this.rank_right_men_cls.get(name)
						if(lm && lm <= 10){ countsMen[clsM] = (countsMen[clsM] || 0) + 1 }
						if(rm && rm <= 10){ countsMen[clsM] = (countsMen[clsM] || 0) + 1 }
					}
					const clsW = this.weight_women.get(name)
					if(clsW){
						const lw = this.rank_left_women_cls.get(name)
						const rw = this.rank_right_women_cls.get(name)
						if(lw && lw <= 10){ countsWomen[clsW] = (countsWomen[clsW] || 0) + 1 }
						if(rw && rw <= 10){ countsWomen[clsW] = (countsWomen[clsW] || 0) + 1 }
					}
				}
				const light = (countsMen['154']||0) + (countsMen['176']||0) + (countsWomen['143']||0)
				const middle = (countsMen['176']||0) + (countsMen['198']||0) + (countsWomen['144+']||0)
				const heavy = (countsMen['220']||0) + (countsMen['242']||0)
				const superh = (countsMen['243+']||0)
				const ordered = [ ['light', light], ['middle', middle], ['heavy', heavy], ['super', superh] ]
				ordered.sort((a,b)=> b[1]-a[1])
				// pick highest, tie broken by array order due to stable sort pre-order; ensure original order priority
				const bestKey = ordered[0][0]
				const bestVal = ordered[0][1]
				perClubBest.set(c.name, { key:bestKey, label: labelFor(bestKey), count: bestVal })
			}
			// compute state best and average across clubs (based on each club's best)
			const values = Array.from(perClubBest.values()).map(v=>v.count)
			const max = Math.max(0, ...values)
			const avg = values.length ? (values.reduce((a,b)=>a+b,0) / values.length) : 0
			const maxCount = values.filter(v=>v===max).length
			const isUniqueMax = maxCount === 1
			const out = new Map()
			for(const [name, v] of perClubBest.entries()){
				const isBest = isUniqueMax && v.count === max
				const pct = avg > 0 ? Math.round(((v.count - avg) / avg) * 100) : 0
				let footer_accent = '—'
				let footer_tail = ''
				if(isBest){ footer_accent = '#1'; footer_tail = ' in the state' }
				else if(pct > 0){ footer_accent = `${pct}%+`; footer_tail = ' than average' }
				out.set(name, { ...v, footer_accent, footer_tail, is_state_best: isBest, pct_over_avg: pct })
			}
			this.club_talent_map = out
		},
		computeMedalsFooters(){
			const pairs = this.clubs
				.filter(c=>Number.isFinite(Number(c.medals_this_year)))
				.map(c=>[c.name, Number(c.medals_this_year)])
			if(pairs.length === 0){ this.medals_footer_map = new Map(); return }
			const values = pairs.map(([,v])=>v)
			const max = Math.max(...values)
			const isUniqueMax = values.filter(v=>v===max).length === 1
			const nonMax = values.filter(v=>v!==max)
			const avg = nonMax.length ? (nonMax.reduce((a,b)=>a+b,0) / nonMax.length) : max
			const map = new Map()
			for(const [name, v] of pairs){
				const isBest = isUniqueMax && v === max
				const pct = avg > 0 ? Math.round(((v - avg) / avg) * 100) : 0
				let accent = '—', tail = ''
				if(isBest){ accent = '#1'; tail = ' in the state' }
				else if(pct > 0){ accent = `${pct}%+`; tail = ' than average' }
				map.set(name, { accent, tail })
			}
			this.medals_footer_map = map
		},
		heroBg(url){
			const u = url || '/default_club.png'
			return `linear-gradient(180deg, rgba(0,0,0,.25), rgba(0,0,0,.45)), url('${u}')`
		},
		isOutOfState(c){
			if(c && c.out_of_state === true) return true
			return String(c?.region || '').toLowerCase().includes('out of state')
		},
		isActive(c){
			return true
		},
		hasWeeklyPractice(c){
			return Array.isArray(c?.training) && c.training.join(' ').toLowerCase().includes('weekly')
		},
		openClub(c){
			const talent = this.club_talent_map.get(c.name) || null
			const medalsFooter = this.medals_footer_map.get(c.name) || null
			const medals_footer_accent = c.medals_footer_accent || medalsFooter?.accent || '—'
			const medals_footer_tail = c.medals_footer_tail || medalsFooter?.tail || ''
			this.selected = { ...c, members: this.membersOf(c.name), talent_metric: talent, medals_footer_accent, medals_footer_tail }
			this.details_open = true
		},
		async loadClubs(){
			try{
				this.is_loading = true
				let res = await fetch('docs/clubs.json', { cache:'no-cache' })
				if(!res.ok) res = await fetch('clubs.json', { cache:'no-cache' })
				if(!res.ok) throw new Error('Failed')
				const json = await res.json()
				if(Array.isArray(json) && json.length){ this.clubs = json }
				this.computeTalentMetrics(); this.computeMedalsFooters()
			}catch(e){ /* fall back to inline */ this.computeTalentMetrics(); this.computeMedalsFooters() }
			finally{ this.is_loading = false }
		},
	},
	mounted(){ this.loadClubs(); this.loadMembership(); this.loadRanks() }
}
</script>

<style scoped>
.main_container{width:min(1100px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}
.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border)}
.title{margin:0;font-size:20px}
.filters{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.input.search{width:260px;max-width:92vw;border:1px solid var(--border);border-radius:10px;background:rgba(255,255,255,.02);color:var(--text);padding:8px 10px;font-family:inherit;font-size:14px}
.input.search:focus{outline:none;border-color:rgba(215,180,58,.35)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--border);background:var(--panel);color:var(--muted);padding:6px 10px;border-radius:999px;font-weight:700;cursor:pointer;transition:.2s ease;line-height:1}
.chip:hover{color:var(--text)}
.chip[aria-pressed="true"]{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2));border-color:transparent;box-shadow:0 6px 18px rgba(215,180,58,.18)}
.chip.clear{border-style:dashed}


.clubs_grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;padding:16px}
.clubs_grid .club_card{opacity:0;transform:translateY(4px)}
.clubs_grid.is_ready .club_card{opacity:1;transform:translateY(0);transition:opacity .24s ease, transform .24s ease}
.club_card{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--border);border-radius:12px;overflow:hidden;transition:transform .18s ease, box-shadow .18s ease}
.club_card:hover{transform:translateY(-2px);box-shadow:0 14px 32px rgba(0,0,0,.25)}
.club_hero{height:160px;position:relative}
.club_img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;filter:blur(10px);transform:scale(1.04);transition:filter .3s ease, transform .3s ease}
.club_img.is_loaded{filter:blur(0);transform:none}
.hero_overlay{position:absolute;inset:0;background:linear-gradient(180deg, rgba(0,0,0,.25), rgba(0,0,0,.45))}
.club_body{display:flex;flex-direction:column;gap:10px;padding:14px;flex:1}
.club_head{display:flex;align-items:center;justify-content:space-between;gap:8px}
.club_name{margin:0;font-size:20px}
.open_badge{font-weight:900;font-size:11px;padding:2px 6px;border-radius:999px;border:2px solid #2ecc71;color:#dfffe9;background:linear-gradient(180deg, rgba(46,204,113,.15), rgba(46,204,113,.12))}
.club_meta{display:flex;gap:12px;flex-wrap:wrap;color:var(--muted)}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-top:auto}
.badge{font-weight:900;font-size:11px;padding:4px 8px;border-radius:999px;border:1px solid var(--border);background:rgba(255,255,255,.02);color:var(--text)}
.badge.members{border-color:rgba(20,130,150,.35);background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16))}
.badge.active{border-color:#2ecc71;background:linear-gradient(180deg, rgba(46,204,113,.15), rgba(46,204,113,.12))}
.badge.weekly{border-color:#3498db;background:linear-gradient(180deg, rgba(52,152,219,.14), rgba(52,152,219,.10))}
.badge.founded{border-color:rgba(215,180,58,.35);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16))}
.badge.out_of_state{border-color:#9eabc9;background:linear-gradient(180deg, rgba(158,171,201,.18), rgba(158,171,201,.12))}
.schedule{display:flex;gap:8px;flex-wrap:wrap}
.pill{font-weight:800;font-size:12px;padding:6px 10px;border-radius:999px;border:1px solid var(--border);background:rgba(255,255,255,.02);color:var(--text)}
.cta_row{display:flex;gap:8px;flex-wrap:wrap}
.cta_btn{display:inline-flex;align-items:center;justify-content:center;padding:8px 12px;border-radius:999px;border:1px solid rgba(215,180,58,.22);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16));color:var(--text);font-weight:800;text-decoration:none;cursor:pointer}
.cta_btn:hover{filter:brightness(1.06)}
.note{color:var(--muted)}
.panel_footer{padding:12px 16px;border-top:1px solid var(--border)}
.add_callout{font-weight:700}
.link{color:var(--text)}

/* Pin badges to bottom by adding a spacer in flex column */
.lt_spacer{flex:1}

/* Skeletons */
.skeletons .sk_box,.skeletons .sk_line,.skeletons .sk_pill{position:relative;overflow:hidden;background:rgba(255,255,255,.06);border-radius:8px}
.skeletons .sk_line{height:14px}
.skeletons .sk_line.w40{width:40%}
.skeletons .sk_line.w30{width:30%}
.skeletons .sk_pill{height:22px;border-radius:999px}
.skeletons .sk_pill.w20{width:20%}
.skeletons .sk_pill.w30{width:30%}
.skeletons .sk_box{height:160px;border-radius:0}
.skeletons .sk_box::after,.skeletons .sk_line::after,.skeletons .sk_pill::after{content:"";position:absolute;inset:0;transform:translateX(-100%);background:linear-gradient(90deg, transparent, rgba(255,255,255,.08), transparent);animation:shimmer 1.2s infinite}
@keyframes shimmer{100%{transform:translateX(100%)}}

.empty_state{padding:20px 16px;display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.empty_title{font-weight:900}
.empty_sub{color:var(--muted)}

@media(max-width:520px){
  .club_hero{height:140px}
}

.new_badge{
  margin-left:10px;
  font-weight:900;
  font-size:13px;
  padding:3px 8px;
  border-radius:999px;
  display:inline-flex;
  align-items:center;
  line-height:1;
  vertical-align:middle;
  border:2px solid var(--accent);
  color:#070e1c;
  background:linear-gradient(180deg, var(--accent), var(--accent-2));
  transform: translateY(-4px);
}
</style> 