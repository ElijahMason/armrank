<template>
  <main class="main_container">
    <section class="panel">
      <div class="panel_header">
        <h2 class="title">Upcoming Tournaments</h2>
      </div>
      <div class="banners">
        <div v-for="(t, i) in tournaments" :key="i" class="banner">
          <div
            class="banner_img"
            :style="{
              backgroundImage: `linear-gradient(180deg, rgba(0,0,0,.25), rgba(0,0,0,.45)), url('${t.image_url}')`,
              backgroundPosition: t.image_position === 'top' ? 'top center' : 'center',
              backgroundSize: 'cover'
            }"
          ></div>
          <div class="banner_body">
            <div class="banner_head">
              <h3 class="banner_title">{{ t.name }}</h3>
              <div class="banner_date">{{ displayDate(t) }}</div>
            </div>
            <div class="banner_meta">
              <div class="banner_loc">
                {{ t.location }}
                <span v-if="t.pending_details" class="badge_pending_inline">Pending</span>
              </div>
              <button class="banner_cta" @click="openDetails(t)">Details</button>
            </div>
          </div>
        </div>
      </div>
    </section>
    <TournamentDetails :open="details_open" :tournament="selected || {}" @close="details_open=false" />
  </main>
</template>
<script>
import TournamentDetails from '../components/TournamentDetails.vue'
export default {
  name: 'TournamentsPage',
  components: { TournamentDetails },
  data(){
    return {
      details_open:false,
      selected:null,
      tournaments: [
        {
          name: 'LLD Foundation Benefit',
          date: 'Sat, June 13, 2026',
          estimated: false,
          pending_details: false,
          location: 'General Duffy’s Waterhole, 404 SW Forest Ave, Redmond, OR 97756',
          venue: "General Duffy's Waterhole",
          image_url: 'https://visitredmondoregon.com/wp-content/uploads/2022/01/general-duffys-redmond-or-768x512.jpg',
          link: 'https://www.longlivedono.com',
          weigh_ins: ['Fri 6/12 6:00–8:00pm', 'Sat 6/13 10:00–11:30am'],
          schedule_start: 'NOON',
          men_classes: '0–154, 155–176, 177–198, 199–220, 221–242, 243+',
          women_classes: '0–143, 144+',
          masters_classes: 'Right & Left: 0–165, 166–198, 199+',
          kids_classes: 'Kids by age and weight',
          awards: 'Custom awards 1st to 3rd place in all classes',
          entry_fees: '$30 per arm/division',
          spectator: 'FREE to watch',
          contacts: [
            'Jody (541) 390-0249',
            'Denise (406) 690-1630',
            'Leonard (406) 670-0065'
          ]
        },
        {
          name: 'WA State AERS Super 64',
          date: 'Sat, Dec, 2025',
          estimated: true,
          pending_details: true,
          location: 'Vancouver, WA',
          venue: 'Venue to be announced by AERS',
          image_url: 'https://www.clarkcountytoday.com/wp-content/uploads/2023/12/Story_Clark-County-Today-ad3839_20583079282849beb3fe99d53206ed6fmv2.jpg',
          image_position: 'top',
          link: 'https://www.instagram.com/aers.armwrestling/',
          schedule_start: '9:00 AM PST (est)',
          weigh_ins: ['Friday evening (est)', 'Saturday morning (est)'],
          men_classes: '0–154, 155–176, 177–198, 199–220, 221–242, 244–274, 275+',
          women_classes: '0–143, 144–164, 165+',
          masters_classes: 'Masters Right/Left',
          entry_fees: 'Announced by AERS',
          spectator: 'Spectator policy subject to AERS announcement',
          cash_prizes: 'Super 64 purse announced by AERS',
          awards: 'Custom awards'
        },
        {
          name: 'Joe Woody Armwrestling Invitational',
          date: 'Sun, Jul 26, 2026',
          estimated: true,
          pending_details: true,
          location: 'Myrtle Creek, OR',
          venue: 'Millsite Park',
          image_url: 'https://styles.redditmedia.com/t5_4o68b9/styles/image_widget_jyqqf7le8g871.jpg?format=pjpg&s=29626b475b80ee1ce69838b0638d6e2a88f53b81',
          link: 'https://www.facebook.com',
          weigh_ins: ['9:00–11:00 (est)'],
          schedule_start: '11:30 AM – 5:00 PM (est)',
          entry_fees: 'Open $25/arm, Women $15/arm, Novice $10/arm, Kids free (est)',
          cash_prizes: 'Custom medals 1st–3rd; match prizes; $100/$50/$25 payout (Open) (est)',
          benefiting: 'Adapts Suicide Prevention Program (est)',
          men_classes: '165, 198, 242, 243+ — Right & Left',
          women_classes: 'Right/Left: 143, 144+',
          kids_classes: 'Adjusted as needed: 0–5, 6–8, 9–12, 13–16'
        },
        {
          name: 'Willamina 4th of July Tournament',
          date: 'Sat, Jul 4, 2026',
          estimated: true,
          pending_details: true,
          location: 'Willamina, OR',
          venue: 'Garden Spot Park',
          image_url: 'https://storage.googleapis.com/proudcity/willaminaor/uploads/2023/07/community_.jpeg',
          link: 'https://www.willaminaoregon.gov',
          weigh_ins: ['Jul 3 4:00–7:00 PM (est)', 'Jul 4 8:00–10:30 AM (est)'],
          schedule_start: '12:00 PM (est)',
          entry_fees: 'Amateur $25/arm, Open $35/arm, Women $15/arm, Kids free (est)',
          men_classes: 'Open/Amateur R/L: 154, 176, 198, 220, 242, 243+',
          women_classes: 'Right & Left: 0–150, 151+',
          kids_classes: 'By age: 3–5, 6–8, 9–12, 13–16',
          contacts: ['Nicolas Mode (971) 901‑5867']
        }
      ],
    }
  },
  methods:{
    openDetails(t){ this.selected = t; this.details_open = true },
    displayDate(t){
      if(t.pending_details){
        // Try to parse month/year from t.date
        const d = new Date(t.date)
        if(!isNaN(d)){
          return d.toLocaleString(undefined, { month:'long', year:'numeric' }) + ' (est)'
        }
        // Fallback: extract Month word and year if present
        const m = String(t.date).match(/([A-Za-z]+).*?(\d{4})/)
        return m ? `${m[1]} ${m[2]} (est)` : `${t.date} (est)`
      }
      return t.estimated ? `${t.date} (est)` : t.date
    }
  }
}
</script>
<style scoped>
.main_container{width:min(1100px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}
.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border)}
.title{margin:0;font-size:20px}
.banners{display:grid;grid-template-columns:repeat(auto-fill, minmax(320px, 1fr));gap:16px;padding:16px}
.banner{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.banner_img{height:160px;background-size:cover;background-position:center}
.banner_body{padding:14px;display:flex;flex-direction:column;gap:10px}
.banner_head{display:flex;justify-content:space-between;align-items:center;gap:8px}
.banner_title{margin:0;font-size:18px}
.banner_date{color:var(--muted);font-weight:700}
.banner_meta{display:flex;justify-content:space-between;align-items:center;color:var(--muted)}
.badge_pending_inline{margin-left:8px; font-weight:900; font-size:11px; padding:2px 6px; border-radius:999px; border:2px solid var(--accent); color:var(--text)}
.banner_cta{display:inline-flex;align-items:center;justify-content:center;padding:8px 12px;border-radius:999px;border:1px solid rgba(215,180,58,.22);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16));color:var(--text);font-weight:800;text-decoration:none;cursor:pointer}
.banner_cta:hover{filter:brightness(1.06)}
</style> 