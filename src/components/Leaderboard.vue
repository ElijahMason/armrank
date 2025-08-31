<template>
  <main class="main_container">
    <section class="panel" role="region" aria-label="Weight classes">
      <div class="panel_header">
        <div class="chips" role="group" aria-label="Weight class">
          <button
            v-for="c in classes"
            :key="c"
            class="chip"
            :data-cls="c"
            :aria-pressed="String(selected_class === c)"
            @click="selectClass(c)"
          >
            {{ c }}
          </button>
        </div>
        <label class="opt">
          <input type="checkbox" v-model="combine_lower" />
          Combine with lower weight classes
        </label>
      </div>

      <div class="sub_bar">
        <span class="sub_pill">{{ sticky_prefix }}{{ sticky_label }}</span>
      </div>

      <div class="wrap">
        <table class="table">
          <thead>
            <tr>
              <th class="left_hdr">Left</th>
              <th class="rank">#</th>
              <th class="right_hdr">Right</th>
            </tr>
          </thead>
          <tbody ref="tbody_ref">
            <tr v-if="!loaded"><td colspan="3">Loading…</td></tr>
            <tr v-else-if="load_error"><td colspan="3">Failed to load rankings data. Refresh the page and try again.</td></tr>

            <template v-else v-for="(row, i) in first_rows" :key="'f'+i">
              <tr :class="row.row_class" class="lb_row">
                <td class="athlete">
                  <div class="flip_container" :class="{ is_flipped: isCellFlipped('f', i, 'L') }" @click="toggleCellFlip('f', i, 'L', row.left_name)">
                    <div class="flip_inner">
                      <div class="flip_front">
                        <span class="name_text">{{ row.left_name }}</span>
                        <span v-if="isClubLeader(row.left_name)" class="badge_inline">
                          <span class="badge_btn crown" :class="{ show: open_tip_key === 'row-f-left-'+i }" @click.stop="toggleTip('row-f-left-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('row-f-left-'+i)" :aria-label="`${leaderClubOf(row.left_name)} club leader`">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                            <span class="tip">{{ leaderClubOf(row.left_name) }} club leader</span>
                          </span>
                        </span>
                        <div v-if="row.fight_left" class="fight_anim left" aria-hidden="true">
                          <div class="fist_icon fist_left">
                            <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                          </div>
                          <div class="ring ring_one"></div>
                          <div class="ring ring_two"></div>
                          <svg class="bang" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 4l6 12 14-6-8 12 14 4-14 4 8 12-14-6-6 12-6-12-14 6 8-12-14-4 14-4-8-12 14 6 6-12z"/></svg>
                          <div class="fist_icon fist_right">
                            <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                          </div>
                        </div>
                      </div>
                      <div class="flip_back">
                        <div class="flip_content">
                          <span class="points">48</span>
                          <div class="badges">
                            <span v-if="isClubLeader(row.left_name)" class="badge_btn crown" :class="{ show: open_tip_key === 'flip-f-left-'+i }" @click.stop="toggleTip('flip-f-left-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('flip-f-left-'+i)" :aria-label="`${leaderClubOf(row.left_name)} club leader`">
                              <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                              <span class="tip">{{ leaderClubOf(row.left_name) }} club leader</span>
                            </span>
                          </div>
                          <button class="details_btn" @click.stop="openAthleteDetails(row.left_name)" aria-label="Open athlete details">
                            <span class="btn_text">Details</span>
                            <svg class="arrow_right" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="rank">
                  <span class="rank_hit left" @click.stop="toggleCellFlip('f', i, 'L', row.left_name)" aria-label="Flip left athlete"></span>
                  <span class="rank_hit right" @click.stop="toggleCellFlip('f', i, 'R', row.right_name)" aria-label="Flip right athlete"></span>
                  <span v-if="i < 3" class="trophy" :class="'trophy_' + (i+1)">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                    </svg>
                    <span class="trophy_num" aria-hidden="true" :style="(i+1===2||i+1===3)?{transform:'translate(1px, -6px)'}:{}">{{ i + 1 }}</span>
                  </span>
                  <span v-else>{{ i + 1 }}</span>
                </td>
                <td class="athlete">
                  <div class="flip_container" :class="{ is_flipped: isCellFlipped('f', i, 'R') }" @click="toggleCellFlip('f', i, 'R', row.right_name)">
                    <div class="flip_inner">
                      <div class="flip_front">
                        <span class="name_text">{{ row.right_name }}</span>
                        <span v-if="isClubLeader(row.right_name)" class="badge_inline">
                          <span class="badge_btn crown" :class="{ show: open_tip_key === 'row-f-right-'+i }" @click.stop="toggleTip('row-f-right-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('row-f-right-'+i)" :aria-label="`${leaderClubOf(row.right_name)} club leader`">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                            <span class="tip">{{ leaderClubOf(row.right_name) }} club leader</span>
                          </span>
                        </span>
                        <div v-if="row.fight_right" class="fight_anim right" aria-hidden="true">
                          <div class="fist_icon fist_left">
                            <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                          </div>
                          <div class="ring ring_one"></div>
                          <div class="ring ring_two"></div>
                          <svg class="bang" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 4l6 12 14-6-8 12 14 4-14 4 8 12-14-6-6 12-6-12-14 6 8-12-14-4 14-4-8-12 14 6 6-12z"/></svg>
                          <div class="fist_icon fist_right">
                            <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                          </div>
                        </div>
                      </div>
                      <div class="flip_back">
                        <div class="flip_content">
                          <span class="points">48</span>
                          <div class="badges">
                            <span v-if="isClubLeader(row.right_name)" class="badge_btn crown" :class="{ show: open_tip_key === 'flip-f-right-'+i }" @click.stop="toggleTip('flip-f-right-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('flip-f-right-'+i)" :aria-label="`${leaderClubOf(row.right_name)} club leader`">
                              <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                              <span class="tip">{{ leaderClubOf(row.right_name) }} club leader</span>
                            </span>
                          </div>
                          <button class="details_btn" @click.stop="openAthleteDetails(row.right_name)" aria-label="Open athlete details">
                            <span class="btn_text">Details</span>
                            <svg class="arrow_right" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              
            </template>
          </tbody>
        </table>

        <!-- toggle OUTSIDE the table to avoid mobile grid constraints -->
        <div
          v-if="is_collapsible"
          class="toggle_wrap"
          role="button"
          :aria-expanded="String(show_all)"
          aria-label="Toggle full list"
          @click="toggleShowAll"
        >
          <div class="show_more_button" :class="{ is_open: show_all }" aria-hidden="true">
            <svg class="toggle_icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>

        <!-- collapsed items OUTSIDE the table -->
        <div v-if="is_collapsible" class="collapse_wrap" :class="{ open: show_all }" ref="collapse_wrap_ref">
          <div class="rows_grid">
            <template v-for="(row, j) in extra_rows" :key="'x'+j">
            <div class="row_grid" :class="row.row_class">
              <div class="cell athlete">
                <div class="flip_container" :class="{ is_flipped: isCellFlipped('x', j, 'L') }" @click="toggleCellFlip('x', j, 'L', row.left_name)">
                  <div class="flip_inner">
                    <div class="flip_front">
                      <span class="name_text">{{ row.left_name }}</span>
                      <span v-if="isClubLeader(row.left_name)" class="badge_inline">
                        <span class="badge_btn crown" :class="{ show: open_tip_key === 'row-x-left-'+j }" @click.stop="toggleTip('row-x-left-'+j)" tabindex="0" @keyup.enter.stop="toggleTip('row-x-left-'+j)" :aria-label="`${leaderClubOf(row.left_name)} club leader`">
                          <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                          <span class="tip">{{ leaderClubOf(row.left_name) }} club leader</span>
                        </span>
                      </span>
                      <div v-if="row.fight_left" class="fight_anim left" aria-hidden="true">
                        <div class="fist_icon fist_left">
                          <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                        </div>
                        <div class="ring ring_one"></div>
                        <div class="ring ring_two"></div>
                        <svg class="bang" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 4l6 12 14-6-8 12 14 4-14 4 8 12-14-6-6 12-6-12-14 6 8-12-14-4 14-4-8-12 14 6 6-12z"/></svg>
                        <div class="fist_icon fist_right">
                          <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                        </div>
                      </div>
                    </div>
                    <div class="flip_back">
                      <div class="flip_content">
                        <span class="points">48</span>
                        <div class="badges">
                          <span v-if="isClubLeader(row.left_name)" class="badge_btn crown" :class="{ show: open_tip_key === 'flip-x-left-'+j }" @click.stop="toggleTip('flip-x-left-'+j)" tabindex="0" @keyup.enter.stop="toggleTip('flip-x-left-'+j)" :aria-label="`${leaderClubOf(row.left_name)} club leader`">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                            <span class="tip">{{ leaderClubOf(row.left_name) }} club leader</span>
                          </span>
                        </div>
                        <button class="details_btn" @click.stop="openAthleteDetails(row.left_name)" aria-label="Open athlete details">
                          <span class="btn_text">Details</span>
                          <svg class="arrow_right" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="cell rank">
                <span v-if="first_rows_count + j + 1 <= 3" class="trophy" :class="'trophy_' + (first_rows_count + j + 1)">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                  </svg>
                  <span class="trophy_num" aria-hidden="true" :style="(first_rows_count + j + 1===2||first_rows_count + j + 1===3)?{transform:'translate(1px, -6px)'}:{}">{{ first_rows_count + j + 1 }}</span>
                </span>
                <span v-else>{{ first_rows_count + j + 1 }}</span>
              </div>
              <div class="cell athlete">
                <div class="flip_container" :class="{ is_flipped: isCellFlipped('x', j, 'R') }" @click="toggleCellFlip('x', j, 'R', row.right_name)">
                  <div class="flip_inner">
                    <div class="flip_front">
                      <span class="name_text">{{ row.right_name }}</span>
                      <span v-if="isClubLeader(row.right_name)" class="badge_inline">
                        <span class="badge_btn crown" :class="{ show: open_tip_key === 'row-x-right-'+j }" @click.stop="toggleTip('row-x-right-'+j)" tabindex="0" @keyup.enter.stop="toggleTip('row-x-right-'+j)" :aria-label="`${leaderClubOf(row.right_name)} club leader`">
                          <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                          <span class="tip">{{ leaderClubOf(row.right_name) }} club leader</span>
                        </span>
                      </span>
                      <div v-if="row.fight_right" class="fight_anim right" aria-hidden="true">
                        <div class="fist_icon fist_left">
                          <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                        </div>
                        <div class="ring ring_one"></div>
                        <div class="ring ring_two"></div>
                        <svg class="bang" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 4l6 12 14-6-8 12 14 4-14 4 8 12-14-6-6 12-6-12-14 6 8-12-14-4 14-4-8-12 14 6 6-12z"/></svg>
                        <div class="fist_icon fist_right">
                          <img class="fist_img" src="https://api.iconify.design/mdi/boxing-glove.svg?color=%23e74c3c" alt="" aria-hidden="true" />
                        </div>
                      </div>
                    </div>
                    <div class="flip_back">
                      <div class="flip_content">
                        <span class="points">48</span>
                        <div class="badges">
                          <span v-if="isClubLeader(row.right_name)" class="badge_btn crown" :class="{ show: open_tip_key === 'flip-x-right-'+j }" @click.stop="toggleTip('flip-x-right-'+j)" tabindex="0" @keyup.enter.stop="toggleTip('flip-x-right-'+j)" :aria-label="`${leaderClubOf(row.right_name)} club leader`">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                            <span class="tip">{{ leaderClubOf(row.right_name) }} club leader</span>
                          </span>
                        </div>
                        <button class="details_btn" @click.stop="openAthleteDetails(row.right_name)" aria-label="Open athlete details">
                          <span class="btn_text">Details</span>
                          <svg class="arrow_right" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </template>
          </div>
        </div>
        
      </div>
    </section>
    <AthleteDetails
      :open="athlete_modal_open"
      :athlete="selected_athlete"
      :division="divisionLabel"
      :weight="weight_map.get(selected_athlete) || classes[classes.length - 1]"
      :rh_rank="overallRank('RH', selected_athlete)"
      :lh_rank="overallRank('LH', selected_athlete)"
      :club="leaderClubOf(selected_athlete)"
      :points="48"
      @close="athlete_modal_open = false"
    />
  </main>
</template>

<script>
import AthleteDetails from './AthleteDetails.vue'
export default {
  name: 'Leaderboard',
  components: { AthleteDetails },
  props: {
    rankings_tab_name: { type: String, required: true },
    weights_tab_name: { type: String, required: true },
    classes: { type: Array, required: true },
    default_selected_class: { type: String, required: true },
    sticky_prefix: { type: String, default: '' },
    max_initial_rows: { type: Number, default: 10 },
  },
  data() {
    const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
    const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
    const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()

    return {
      sheet_id_raw,
      sheet_id,

      selected_class: null,
      combine_lower: true,
      loaded: false,
      load_error: false,
      show_all: false,
      // flip state
      flipped_cells: new Set(), // keys: `${section}-${index}-${side}` where side is 'L' or 'R'
      open_tip_key: '',
      // modal
      athlete_modal_open: false,
      selected_athlete: '',

      left_list_raw: [],
      right_list_raw: [],
      weight_map: new Map(),
      left_challenge_map: new Map(),
      right_challenge_map: new Map(),
      // clubs
      leader_name_to_club: new Map(),
    }
  },
  computed: {
    sticky_label() {
      const cls = this.selected_class || this.default_selected_class
      const base_top = this.classes[this.classes.length - 1]
      if (this.combine_lower && cls === base_top) {
        return 'Combined overall'
      }
      const plus_label = base_top && base_top.includes('+') ? `${base_top} lbs` : `${cls} lbs`
      const text = cls === base_top ? plus_label : `${cls} lbs`
      const extra = this.combine_lower && cls !== this.classes[0] ? ' + lower' : ''
      return `${text}${extra}`
    },

    classes_to_combine() {
      const i = this.classes.indexOf(this.selected_class)
      return this.classes.slice(0, i + 1)
    },
    left_groups() {
      const index = new Map(this.left_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.left_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || this.classes[this.classes.length - 1]
        map.get(cls).push({ name, rank: index.get(name), cls })
      })
      this.classes.forEach(c => map.get(c).sort((a, b) => a.rank - b.rank))
      return map
    },
    right_groups() {
      const index = new Map(this.right_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.right_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || this.classes[this.classes.length - 1]
        map.get(cls).push({ name, rank: index.get(name), cls })
      })
      this.classes.forEach(c => map.get(c).sort((a, b) => a.rank - b.rank))
      return map
    },
    left_list() {
      if (this.combine_lower) {
        return this.classes_to_combine
          .flatMap(c => this.left_groups.get(c) || [])
          .sort((a, b) => a.rank - b.rank)
      }
      return (this.left_groups.get(this.selected_class) || []).slice()
    },
    right_list() {
      if (this.combine_lower) {
        return this.classes_to_combine
          .flatMap(c => this.right_groups.get(c) || [])
          .sort((a, b) => a.rank - b.rank)
      }
      return (this.right_groups.get(this.selected_class) || []).slice()
    },
    rows() {
      const n = Math.max(this.left_list.length, this.right_list.length)
      const out = []
      for (let i = 0; i < n; i++) {
        const rank = i + 1
        const left_name = this.left_list[i]?.name || ''
        const right_name = this.right_list[i]?.name || ''
        let row_class = ''
        if (rank <= 3) {
          row_class = (rank === 1 ? 'top1' : rank === 2 ? 'top2' : 'top3')
        }
        const fight_left = i > 0 && this.left_challenge_map.get(left_name) === true
        const fight_right = i > 0 && this.right_challenge_map.get(right_name) === true
        out.push({ left_name, right_name, row_class, fight_left, fight_right })
      }
      return out
    },
    first_rows(){
      const limit = this.max_initial_rows
      return this.rows.slice(0, Math.min(limit, this.rows.length))
    },
    extra_rows(){
      const limit = this.max_initial_rows
      return this.rows.slice(limit)
    },
    is_collapsible(){
      return this.rows.length > this.max_initial_rows
    },
    first_rows_count(){
      return this.first_rows.length
    },
    divisionLabel(){
      return this.rankings_tab_name.includes('_F') ? 'Women' : 'Men'
    },
    leaderClubLabel(){
      const c = this.leaderClubOf(this.flipped_athlete)
      return c ? `${c} club leader` : 'Club leader'
    },
  },
  methods: {
    selectClass(cls) {
      this.selected_class = cls
    },
    toggleShowAll(){
      this.show_all = !this.show_all
    },
    onRowAthleteClick(){ /* no-op after per-cell flip introduced */ },
    toggleCellFlip(section, index, side, name){
      const key = `${section}-${index}-${side}`
      if(this.flipped_cells.has(key)) this.flipped_cells.delete(key)
      else this.flipped_cells.add(key)
      // force reactive update by recreating the Set
      this.flipped_cells = new Set(this.flipped_cells)
    },
    isCellFlipped(section, index, side){
      const key = `${section}-${index}-${side}`
      return this.flipped_cells.has(key)
    },
    toggleTip(key){
      this.open_tip_key = this.open_tip_key === key ? '' : key
    },
    isClubLeader(name){
      const target = String(name || '').trim().toLowerCase()
      return this.leader_name_to_club.has(target)
    },
    leaderClubOf(name){
      const target = String(name || '').trim().toLowerCase()
      return this.leader_name_to_club.get(target) || ''
    },
    overallRank(hand, name){
      const n = String(name || '').trim()
      if(!n) return ''
      if(hand === 'RH'){
        const i = this.right_list_raw.findIndex(x => String(x || '').trim() === n)
        return i >= 0 ? i + 1 : ''
      }else{
        const i = this.left_list_raw.findIndex(x => String(x || '').trim() === n)
        return i >= 0 ? i + 1 : ''
      }
    },
    openAthleteDetails(name){
      this.selected_athlete = name
      this.athlete_modal_open = true
    },
    gvizCsv(tab) {
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
            if (ch === '"') {
              q = !q
              continue
            }
            if (ch === ',' && !q) {
              out.push(cur)
              cur = ''
            } else {
              cur += ch
            }
          }
          out.push(cur)
          return out.map(s => s.trim())
        })
    },
    weightClass(lbs) {
      const top = this.classes[this.classes.length - 1]
      if (lbs === '' || lbs === null || Number.isNaN(Number(lbs))) return top
      const w = Number(lbs)
      if (w === -1) return top
      const thresholds = this.classes
        .filter(c => !c.includes('+'))
        .map(c => Number(c))
        .sort((a,b)=>a-b)
      for (const t of thresholds) {
        if (w <= t) return String(t)
      }
      return top
    },
    triggerSwapAnimation() {
      const el = this.$refs.tbody_ref
      if (!el) return
      el.classList.remove('swap')
      void el.offsetWidth
      el.classList.add('swap')
      el.addEventListener('animationend', () => el.classList.remove('swap'), { once: true })
    },
    async load() {
      try {
        const [rank_csv, wt_csv] = await Promise.all([
          fetch(this.gvizCsv(this.rankings_tab_name)).then(r => r.text()),
          fetch(this.gvizCsv(this.weights_tab_name)).then(r => r.text()),
        ])

        const r_rows = this.csvToRows(rank_csv)
        this.left_list_raw = r_rows.slice(1).map(r => r[0]).filter(Boolean)
        this.right_list_raw = r_rows.slice(1).map(r => r[2]).filter(Boolean)

        const leftChal = new Map()
        const rightChal = new Map()
        r_rows.slice(1).forEach(r => {
          const left_name = (r[0] || '').trim()
          const left_flag = (r[1] || '').trim().toLowerCase()
          const right_name = (r[2] || '').trim()
          const right_flag = (r[3] || '').trim().toLowerCase()
          if (left_name) leftChal.set(left_name, left_flag === 'challenging')
          if (right_name) rightChal.set(right_name, right_flag === 'challenging')
        })
        this.left_challenge_map = leftChal
        this.right_challenge_map = rightChal

        const w_rows = this.csvToRows(wt_csv)
        const map = new Map()
        w_rows.slice(1).forEach(r => {
          const name = (r[0] || '').trim()
          if (!name) return
          const lbs = r[1] !== undefined ? r[1] : ''
          map.set(name, this.weightClass(lbs))
        })
        this.weight_map = map

        this.loaded = true
        this.$nextTick(() => this.triggerSwapAnimation())
      } catch (e) {
        console.error(e)
        this.load_error = true
        this.loaded = true
      }
    },
    async loadClubs(){
      try{
        const url = new URL('clubs.json', import.meta.env.BASE_URL)
        const res = await fetch(url)
        if(!res.ok) return
        const clubs = await res.json()
        const map = new Map()
        clubs.forEach(c => {
          const clubName = String(c?.name || '').trim()
          const leaders = Array.isArray(c?.leaders) ? c.leaders : []
          leaders.forEach(l => {
            const key = String(l || '').trim().toLowerCase()
            if(key) map.set(key, clubName)
          })
        })
        this.leader_name_to_club = map
      }catch{}
    }
  },
  created(){
    this.selected_class = this.default_selected_class
  },
  mounted() {
    this.load()
    this.loadClubs()
  },
  watch: {
    selected_class() {
      this.show_all = false
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    combine_lower() {
      this.show_all = false
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    rows() {
      this.$nextTick(() => this.triggerSwapAnimation())
    }
  },
}
</script>

<style scoped>
.main_container{width:min(1100px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}

.chips{display:flex;gap:6px;flex-wrap:wrap;margin:0}
.chip{border:1px solid var(--border);background:var(--panel);color:var(--muted);padding:6px 10px;border-radius:999px;font-weight:700;cursor:pointer;transition:.2s ease;line-height:1}
.chip:hover{color:var(--text)}
.chip[aria-pressed="true"]{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2));border-color:transparent;box-shadow:0 6px 18px rgba(215,180,58,.18)}

.opt{display:flex;align-items:center;gap:8px;color:var(--muted);font-weight:700}
.opt input{accent-color:var(--accent)}

.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid var(--border)}
.sub_bar{position:sticky; top:0; z-index:5; background:var(--header-bg); border-bottom:1px solid var(--border); padding:10px 16px; display:flex; align-items:center; gap:12px}
.sub_pill{font-weight:800; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); padding:6px 10px; border-radius:999px}
.wrap{overflow: visible !important; height: auto; max-height: none; margin-bottom:0; padding-bottom:0; -webkit-overflow-scrolling: auto; overscroll-behavior: auto; touch-action: auto}

.table{width:100%;max-width:100%;border-collapse:collapse;font-size:15px; table-layout:auto}
.table thead th{background:var(--header-bg);color:var(--muted);text-align:left;padding:10px 12px;border-bottom:1px solid var(--border)}
.table tbody td{padding:10px 12px;border-bottom:1px solid var(--border);min-width:0;word-break:break-word;background:transparent}
.table tbody tr:hover td{background:rgba(10,23,64,.35)}

/* perfectly centered # column with turquoise tint; remove any underlines */
th.rank, td.rank{width:64px; min-width:64px; text-align:center; vertical-align:middle}
/* ensure overlays in athlete cells can sit between rows */
.athlete{min-width:0; overflow:visible; position:relative; z-index:1}
.name_text{display:inline-block; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}

td.rank{
  display:flex; align-items:center; justify-content:center;
  font-weight:900; color:var(--accent);
  background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)) !important;
  border-left:none !important; border-right:none !important;
  border-bottom:1px solid var(--border) !important;
  border-radius:6px;
  padding:10px 0 !important;
}
td.rank::before, td.rank::after, th.rank::before, th.rank::after{ content:none !important; display:none !important }

/* fight overlay - centered between current row and the one above; nudged up 30px */
.fight_anim{ position:absolute; left:0; right:0; top:-50%; height:200%; transform: translateY(-22px); display:flex; align-items:center; justify-content:center; pointer-events:none; z-index:400 }
.fight_anim.left{ justify-content:center }
.fight_anim.right{ justify-content:center }

.fist_icon{ width:32px; height:32px }
.fist_img{ width:100%; height:100%; display:block; filter:drop-shadow(0 0 12px rgba(231,76,60,.45)); transform-origin:50% 50% }
.fist_left .fist_img{ transform: rotate(200deg) }
.fist_right .fist_img{ transform: rotate(20deg) }

/* one fist comes down from above, the other rises from below */
.fist_left{ animation:challengeFromTop 1.4s cubic-bezier(.25,.8,.2,1) infinite }
.fist_right{ animation:challengeFromBottom 1.4s cubic-bezier(.25,.8,.2,1) infinite }

.bang{ width:32px; height:32px; margin:0 10px; fill:#ff4d4d; filter:drop-shadow(0 0 10px rgba(255,77,77,.65)); animation:bangPop 1.4s ease-in-out infinite }
.ring{ position:absolute; width:34px; height:34px; border:2px solid rgba(255,77,77,.7); border-radius:50%; }
.ring_one{ animation:ringPulse 1.4s ease-out infinite }
.ring_two{ animation:ringPulse 1.4s ease-out infinite; animation-delay:.25s }

@keyframes challengeFromTop{
  0%{ transform:translate(-18px, -34px) rotate(-12deg) scale(.96); opacity:.85 }
  40%{ transform:translate(-8px, -10px) rotate(-6deg) scale(1.06); opacity:1 }
  50%{ transform:translate(-4px, -4px) rotate(-2deg) scale(1.1); opacity:1 }
  60%{ transform:translate(-8px, -8px) rotate(-5deg) scale(1.04); opacity:.98 }
  100%{ transform:translate(-18px, -34px) rotate(-12deg) scale(.96); opacity:.85 }
}
@keyframes challengeFromBottom{
  0%{ transform:translate(18px, 34px) rotate(12deg) scale(.96); opacity:.85 }
  40%{ transform:translate(8px, 10px) rotate(6deg) scale(1.06); opacity:1 }
  50%{ transform:translate(4px, 4px) rotate(2deg) scale(1.1); opacity:1 }
  60%{ transform:translate(8px, 8px) rotate(5deg) scale(1.04); opacity:.98 }
  100%{ transform:translate(18px, 34px) rotate(12deg) scale(.96); opacity:.85 }
}
@keyframes bangPop{ 0%,100%{ transform:translateY(6px) scale(.85) rotate(0deg); opacity:.75 } 45%{ transform:translateY(-2px) scale(1.28) rotate(8deg); opacity:1 } 55%{ transform:translateY(-2px) scale(1.18) rotate(-8deg); opacity:1 } }
@keyframes ringPulse{ 0%{ transform:scale(.6); opacity:.9 } 70%{ transform:scale(1.7); opacity:.25 } 100%{ transform:scale(1.9); opacity:0 } }

/* Smooth swap animation (disabled for show/hide) */
@keyframes fadeSlide { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
tbody.swap{ animation: fadeSlide .22s ease both }
@media(prefers-reduced-motion:reduce){ tbody.swap{ animation:none } }

/* Collapsing area for extra rows */
.collapse_cell{ padding:0 !important; background:transparent !important; border-bottom:none !important }
.collapse_wrap{ max-height:0; overflow:hidden; transition:max-height .28s ease; will-change:max-height }
.collapse_wrap.open{ max-height:2000px }
.rows_grid{ display:block; width:100% }
.row_grid{ display:grid; grid-template-columns:minmax(0,1fr) 64px minmax(0,1fr); align-items:center }
.row_grid .cell{ padding:10px 12px; border-bottom:1px solid var(--border) }
.row_grid .cell.athlete{ position:relative; overflow:visible; z-index:1 }
.row_grid .cell.rank{ display:flex; align-items:center; justify-content:center; font-weight:900; color:var(--accent); background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)) !important; border-left:none !important; border-right:none !important; border-bottom:1px solid var(--border) !important; border-radius:6px; padding:10px 0 !important }

/* Trophy SVG (bigger) with number overlay */
.trophy{ position:relative; display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px; transform: translateY(4px) }
.trophy svg{ width:34px; height:34px; display:block }
.trophy_1 svg{ fill: var(--accent) }
.trophy_2 svg{ fill: var(--silver) }
.trophy_3 svg{ fill: var(--bronze) }

/* Show more row replacement (outside table) */
.toggle_wrap{ display:flex; align-items:center; justify-content:center; padding:8px 0; background:linear-gradient(180deg, rgba(20,130,150,.10), rgba(12,100,120,.08)); border-top:1px solid var(--border); border-bottom:1px solid var(--border); cursor:pointer; -webkit-tap-highlight-color: transparent }
.show_more_button{ display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; border-radius:999px; transition:.18s ease; pointer-events:none }
.show_more_button:hover{ filter:brightness(1.06) }
.toggle_icon{ transition: transform .18s ease }
.show_more_button.is_open .toggle_icon{ transform: rotate(180deg) }

/* Sticky bottom toggle when expanded */
.bottom_sticky{ position:sticky; bottom:0; display:flex; justify-content:center; padding:4px 0; background:linear-gradient(180deg, rgba(11,22,48,0), rgba(11,22,48,.78)); border-top:1px solid var(--border) }

/* Prevent bottom border from peeking at the end of the list */
.table tbody tr:last-child td{ border-bottom:none !important }
.rows_grid .row_grid:last-child .cell{ border-bottom:none !important }
.wrap{ position:relative }
.wrap::after{ content:""; position:absolute; left:0; right:0; bottom:-2px; height:6px; background:linear-gradient(180deg, rgba(11,22,48,0), rgba(11,22,48,1)); pointer-events:none }

/* Static tints for top 3 rows */
tbody tr.top1 td{ background:linear-gradient(180deg, rgba(215,180,58,.14), rgba(185,147,34,.12)) !important }
tbody tr.top2 td{ background:linear-gradient(180deg, rgba(192,192,192,.16), rgba(170,170,170,.12)) !important }
tbody tr.top3 td{ background:linear-gradient(180deg, rgba(205,127,50,.16), rgba(175,107,40,.12)) !important }
.row_grid.top1 .cell{ background:linear-gradient(180deg, rgba(215,180,58,.14), rgba(185,147,34,.12)) }
.row_grid.top2 .cell{ background:linear-gradient(180deg, rgba(192,192,192,.16), rgba(170,170,170,.12)) }
.row_grid.top3 .cell{ background:linear-gradient(180deg, rgba(205,127,50,.16), rgba(175,107,40,.12)) }

/* Mobile */
@media(max-width:760px){
  /* No table-row hacks required now; collapsed UI already outside table */
}

/* Nudge trophy number slightly downward and center */
.trophy_num{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:900;
  font-size:14px;
  color:#0b1630;
  text-shadow:0 1px 0 rgba(255,255,255,.45);
  transform: translateY(-7px);
  pointer-events:none;
}
/* Slight horizontal tweak for 2 and 3 */
.trophy_2 .trophy_num,
.trophy_3 .trophy_num{ transform: translate(0px, -7px) }

@media(max-width:760px){
  .trophy_2 .trophy_num,
  .trophy_3 .trophy_num{ transform: translate(0px, -7px) }
}

.left_hdr{text-align:right !important}
.right_hdr{text-align:left}
.table thead th.rank{ text-align:center }

.table tbody td.athlete:first-child{ text-align:right }
.table tbody td.athlete:last-child{ text-align:left }

.row_grid .cell.athlete:first-child{ text-align:right }
.row_grid .cell.athlete:last-child{ text-align:left }

/* Flip details UI */
.lb_row{ cursor:pointer }
.flip_details_row .flip_cell{ padding:0 !important; background:transparent !important; border-bottom:none !important }
.flip_details_card{ padding:8px 12px; border-bottom:1px solid var(--border) }
.flip_card{ display:flex; align-items:center; gap:12px; justify-content:space-between; background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92)); border:1px solid var(--border); border-radius:10px; padding:10px 12px }
.flip_main{ display:flex; align-items:center; gap:12px }
.points_badges{ display:flex; align-items:center; gap:14px; flex-wrap:wrap }
.points{ font-weight:900; color:var(--text); background:rgba(255,255,255,.06); border:1px solid var(--border); padding:6px 10px; border-radius:999px }
.badges{ display:flex; align-items:center; gap:8px }

/* Gray details button with right arrow */
.details_btn{ display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; border:1px solid var(--border); background:rgba(255,255,255,.06); color:var(--muted); cursor:pointer }
.details_btn .arrow_right{ width:18px; height:18px }
.details_btn:hover{ filter:brightness(1.06); color:var(--text) }

/* Crown badge + tooltip (reused style) */
.icon{width:18px; height:18px}
.badge_btn{ position:relative; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:999px }
.crown{background:linear-gradient(180deg, rgba(215,180,58,.2), rgba(185,147,34,.18)); color:var(--accent); border:1px solid rgba(215,180,58,.45)}
.crown_icon{fill:currentColor}
.badge_btn .tip{ position:absolute; bottom:calc(100% + 8px); left:0; right:auto; transform:translateX(0) translateY(6px); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:8px 10px; display:inline-block; min-width:0; width:max-content; max-width:min(78vw, 320px); white-space:normal; overflow-wrap:anywhere; word-break:normal; text-align:left; font-weight:800; font-size:12px; box-shadow:var(--glow); opacity:0; pointer-events:none; transition:opacity .16s ease, transform .16s ease; z-index:2 }
.badge_btn .tip::after{ content:""; position:absolute; top:100%; left:14px; transform:translateX(0); width:0; height:0; border-left:6px solid transparent; border-right:6px solid transparent; border-top:6px solid var(--border) }
/* Right-align crown tooltip to avoid viewport overflow like in ClubDetails */
.crown.badge_btn .tip{ right:0; left:auto; text-align:right; width:max-content; min-width:0; max-width:min(78vw, 320px) }
.crown.badge_btn .tip::after{ left:auto; right:14px }
.badge_btn:hover .tip, .badge_btn.show .tip{ opacity:1; transform:translateX(0) translateY(0); pointer-events:auto }
.badge_inline{ display:inline-flex; margin-left:6px }

/* Per-cell 3D flip */
.flip_container{ position:relative; perspective:1000px; display:block }
.flip_inner{ position:relative; transform-style:preserve-3d; transition:transform .35s ease; min-height:28px }
.flip_container.is_flipped .flip_inner{ transform:rotateY(180deg) }
.flip_front, .flip_back{ position:absolute; inset:0; backface-visibility:hidden; -webkit-backface-visibility:hidden; display:flex; align-items:center; gap:8px }
.flip_front{ justify-content:flex-end }
.flip_back{ transform:rotateY(180deg); justify-content:space-between; background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92)); border:1px solid var(--border); border-radius:8px; padding:6px 8px }
.flip_content{ display:flex; align-items:center; gap:10px }
.rank{ position:relative }
.rank_hit{ position:absolute; top:0; bottom:0; width:48%; cursor:pointer }
.rank_hit.left{ left:2% }
.rank_hit.right{ right:2% }
</style> 