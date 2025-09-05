<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')" @wheel="onOverlayWheel" @touchmove="onOverlayTouchMove" role="dialog" aria-modal="true" :aria-label="club?.name || 'Club details'">
    <div class="modal">
      <div class="modal_header">
        <h2 class="modal_title">{{ club.name }}</h2>
        <div class="spacer"></div>
        <button v-if="dev && !edit_mode" class="icon_btn" @click="startEdit" aria-label="Edit">
          <svg viewBox="0 0 24 24" class="icon"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zm2.92 2.33H5v-.92l9.06-9.06.92.92L5.92 19.58zM20.71 7.04a1.003 1.003 0 0 0 0-1.42l-2.34-2.34a1.003 1.003 0 0 0-1.42 0l-1.83 1.83 3.75 3.75 1.84-1.82z"/></svg>
        </button>
        <button class="close_btn" @click="onCloseClick" aria-label="Close">×</button>
      </div>

      <div class="scroll_area">
      <div class="content" v-if="!edit_mode">
      <div class="stats_row">
        <div class="stat_card">
          <div class="stat_icon crown_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Leader</div>
            <div class="stat_value">{{ leader_display }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer" v-if="leader_footer_obj">
            <template v-if="leader_footer_obj.mode === 'dual'">
              <span class="accent">{{ leader_footer_obj.num }}</span>{{ leader_footer_obj.tail_before }}<span class="accent">{{ leader_footer_obj.num2 }}</span>{{ leader_footer_obj.tail_after }}
            </template>
            <template v-else>
              <span class="accent">{{ leader_footer_obj.num }}</span>{{ leader_footer_obj.tail }}
            </template>
          </div>
          <div class="stat_footer" v-else-if="leader_is_multiple">See description</div>
          <div class="stat_footer" v-else-if="leader_highlight"><span class="accent">{{ leader_highlight.num }}</span>{{ leader_highlight.tail }}</div>
          <div class="stat_footer" v-else><span class="accent">—</span></div>
        </div>
        <div class="stat_card">
          <div class="stat_icon users_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M16 11c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3zM8 11c1.66 0 3-1.34 3-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.76 0-5 1.79-5 4v2h10v-2c0-2.21-2.24-4-5-4zm8 0c-.66 0-1.29.08-1.87.23 1.7.8 2.87 2.2 2.87 3.77v2h6v-2c0-2.21-2.69-4-7-4z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Members</div>
            <div class="stat_value">{{ club.members_count || members.length }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer">{{ members_footer_prefix }}<span class="accent">{{ members_footer_accent }}</span>{{ members_footer_tail }}</div>
        </div>
        <div class="stat_card">
          <div class="stat_icon location_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M12 2C8.14 2 5 5.14 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.86-3.14-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Location</div>
            <div class="stat_value">{{ location_label }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer"><span class="accent">#{{ location_rank }}</span> in {{ city_label }}</div>
        </div>
        <div class="stat_card">
          <div class="stat_icon active_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M13 3L4 14h7l-1 7 9-11h-7z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Average Practice Size</div>
            <div class="stat_value">{{ club.avg_practice_size || avg_practice_size }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer"><span class="accent">{{ avg_practice_footer_accent }}</span>{{ avg_practice_footer_tail }}</div>
        </div>
        <div class="stat_card" v-if="show_practice_card">
          <div class="stat_icon practice_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M7 2v2H5a2 2 0 0 0-2 2v2h18V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2H7zm14 8H3v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V10zm-7 2v4h4v-2h-2v-2h-2z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Weekly Practice</div>
            <div class="stat_value">{{ practice_day || '' }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer" v-if="practice_start"><span class="accent">{{ practice_start }}</span><template v-if="practice_end"> - {{ practice_end }}</template></div>
        </div>
        <div class="stat_card" v-if="club?.out_of_state === true">
          <div class="stat_icon oos_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M2.5 19h19v2h-19v-2zm19-9.5l-2.8.8L14 5.1 12.2 5.6l2.9 4-7.2 1-.6-2L3 10.7v2l6.4-.9 6 1.7 6.1-1.8v-2.2z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Out of State</div>
            <div class="stat_value">No rankings data yet</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer">Washington Rankings coming soon</div>
        </div>
        <div class="stat_card" v-if="show_talent_card">
          <div class="stat_icon talent_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4zm-6 8v-1c0-2.21 3.58-3 6-3s6 .79 6 3v1H6zm10.6-9.2l1.1-2.4 1.1 2.4 2.4 1.1-2.4 1.1-1.1 2.4-1.1-2.4-2.4-1.1 2.4-1.1z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">{{ talent_label }}</div>
            <div class="stat_value">{{ talent_number }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer"><span class="accent">{{ talent_footer_accent }}</span>{{ talent_footer_tail }}</div>
        </div>
        <div class="stat_card" v-if="show_medals_card">
          <div class="stat_icon trophy_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Medals won this year</div>
            <div class="stat_value">{{ medals_this_year_value }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer"><span class="accent">{{ medals_footer_accent }}</span>{{ medals_footer_tail }}</div>
        </div>
        <div class="stat_card" v-if="show_supermatches_card">
          <div class="stat_icon match_icon_bubble" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M7 6h10v2H7V6zm0 5h10v2H7v-2zm0 5h10v2H7v-2z"/></svg>
          </div>
          <div class="stat_body">
            <div class="stat_label">Supermatches hosted</div>
            <div class="stat_value">{{ supermatches_hosted_value }}</div>
          </div>
          <div class="stat_divider"></div>
          <div class="stat_footer"><span class="accent">{{ supermatches_upcoming_value }}</span> upcoming</div>
        </div>
      </div>

      <div class="join_box">
        <div class="join_img" :style="{ backgroundImage: heroBg(club.image_url) }" aria-hidden="true"></div>
        <div class="join_body">
          <div class="join_text">Interested in joining? Contact {{ leader_name }} on Facebook for more info:</div>
          <div v-if="club.desc" class="join_desc">{{ club.desc }}</div>
          <a v-if="facebook_url" class="social_btn fb_btn" :href="facebook_url" target="_blank" rel="noopener">
            <svg class="social_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12.06C22 6.505 17.523 2 12 2S2 6.505 2 12.06C2 17.08 5.657 21.21 10.438 22v-7.03H7.898v-2.91h2.54V9.845c0-2.5 1.492-3.89 3.777-3.89 1.094 0 2.238.196 2.238.196v2.47h-1.26c-1.243 0-1.63.774-1.63 1.567v1.886h2.773l-.443 2.91h-2.33V22C18.343 21.21 22 17.08 22 12.06z"/></svg>
            Facebook
          </a>
          <span v-else class="social_btn fb_btn disabled" aria-disabled="true">
            <svg class="social_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12.06C22 6.505 17.523 2 12 2S2 6.505 2 12.06C2 17.08 5.657 21.21 10.438 22v-7.03H7.898v-2.91h2.54V9.845c0-2.5 1.492-3.89 3.777-3.89 1.094 0 2.238.196 2.238.196v2.47h-1.26c-1.243 0-1.63.774-1.63 1.567v1.886h2.773l-.443 2.91h-2.33V22C18.343 21.21 22 17.08 22 12.06z"/></svg>
            Facebook
          </span>
          <a v-if="instagram_url" class="social_btn ig_btn" :href="instagram_url" target="_blank" rel="noopener">
            <svg class="social_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10c2.76 0 5 2.24 5 5v10c0 2.76-2.24 5-5 5H7c-2.76 0-5-2.24-5-5V7c0-2.76 2.24-5 5-5zm10 2H7C5.9 4 5 4.9 5 6v12c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5zM17.5 6A1.5 1.5 0 1 1 16 7.5 1.5 1.5 0 0 1 17.5 6z"/></svg>
            Instagram
          </a>
          <button v-if="show_phone_button && !phone_revealed" class="ghost_btn" @click="phone_revealed = true" aria-label="Reveal phone number">
            <svg class="phone_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 0 0 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V21c0 .55-.45 1-1 1C10.85 22 2 13.15 2 2c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.24.2 2.45.57 3.57.11.35.03.74-.24 1.02l-2.21 2.2z"/></svg>
            Phone
          </button>
          <a v-if="show_phone_button && phone_revealed" class="ghost_btn" :href="phone_tel_href">
            <svg class="phone_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 0 0 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V21c0 .55-.45 1-1 1C10.85 22 2 13.15 2 2c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.24.2 2.45.57 3.57.11.35.03.74-.24 1.02l-2.21 2.2z"/></svg>
            {{ phone_display }}
          </a>
        </div>
      </div>

      <div class="list_wrap">
        <div class="list_head">
          <div class="label">Featured members <span class="muted_count">({{ members.length }})</span></div>
        </div>
        <ul class="member_list">
          <li v-for="(m, i) in first_members" :key="i" class="member_item">
            <div class="badge_wrap">
              <div v-if="bestBadge(m) && bestBadge(m).type === 'trophy'" class="badge_btn" :class="{ show: open_tip_key === 'perf-'+i }" @click.stop="toggleTip('perf-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('perf-'+i)">
                <span class="trophy" :class="'trophy_' + bestBadge(m).rank" :aria-label="bestBadge(m).tooltip">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                  </svg>
                  <span class="trophy_num" aria-hidden="true">{{ bestBadge(m).rank }}</span>
                </span>
                <div class="tip">{{ bestBadge(m).tooltip }}</div>
              </div>
              <div v-else-if="bestBadge(m)" class="rank_badge badge_btn" :class="[bestBadge(m).type, { show: open_tip_key === 'perf-'+i }]" @click.stop="toggleTip('perf-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('perf-'+i)" :aria-label="bestBadge(m).tooltip">
                <span class="badge_text">{{ bestBadge(m).rank }}</span>
                <div class="tip">{{ bestBadge(m).tooltip }}</div>
              </div>
            </div>
            <span class="member_name">{{ m }}</span>
            <div class="leader_wrap" v-if="isClubLeader(m)">
              <div class="badge_btn crown" :class="{ show: open_tip_key === 'crown-'+i }" @click.stop="toggleTip('crown-'+i)" tabindex="0" @keyup.enter.stop="toggleTip('crown-'+i)" :aria-label="`${club.name} club leader`">
                <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                <div class="tip">{{ club.name }} club leader</div>
              </div>
            </div>
          </li>
        </ul>
        <div class="collapse_wrap" :class="{ open: show_all }">
          <ul class="member_list extra_list">
            <li v-for="(m, j) in extra_members" :key="'x'+j" class="member_item extra_item">
              <div class="badge_wrap">
                <div v-if="bestBadge(m) && bestBadge(m).type === 'trophy'" class="badge_btn" :class="{ show: open_tip_key === 'perf-'+(first_members_count + j) }" @click.stop="toggleTip('perf-'+(first_members_count + j))" tabindex="0" @keyup.enter.stop="toggleTip('perf-'+(first_members_count + j))">
                  <span class="trophy" :class="'trophy_' + bestBadge(m).rank" :aria-label="bestBadge(m).tooltip">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                      <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                    </svg>
                    <span class="trophy_num" aria-hidden="true">{{ bestBadge(m).rank }}</span>
                  </span>
                  <div class="tip">{{ bestBadge(m).tooltip }}</div>
                </div>
                <div v-else-if="bestBadge(m)" class="rank_badge badge_btn" :class="[bestBadge(m).type, { show: open_tip_key === 'perf-'+(first_members_count + j) }]" @click.stop="toggleTip('perf-'+(first_members_count + j))" tabindex="0" @keyup.enter.stop="toggleTip('perf-'+(first_members_count + j))" :aria-label="bestBadge(m).tooltip">
                  <span class="badge_text">{{ bestBadge(m).rank }}</span>
                  <div class="tip">{{ bestBadge(m).tooltip }}</div>
                </div>
              </div>
              <span class="member_name">{{ m }}</span>
              <div class="leader_wrap" v-if="isClubLeader(m)">
                <div class="badge_btn crown" :class="{ show: open_tip_key === 'crown-'+(first_members_count + j) }" @click.stop="toggleTip('crown-'+(first_members_count + j))" tabindex="0" @keyup.enter.stop="toggleTip('crown-'+(first_members_count + j))" :aria-label="`${club.name} club leader`">
                  <svg viewBox="0 0 24 24" aria-hidden="true" class="icon crown_icon"><path d="M5 7l4 3 3-5 3 5 4-3 1 10H4L5 7z"/></svg>
                  <div class="tip">{{ club.name }} club leader</div>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div class="toggle_wrap" v-if="extra_members.length" role="button" :aria-expanded="String(show_all)" @click="toggleShowAll">
          <div class="show_more_button" :class="{ is_open: show_all }" aria-hidden="true">
            <svg class="toggle_icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
        </div>
      </div>
      </div>
      <div v-if="edit_mode" class="edit_panel">
        <div class="edit_grid">
          <label class="edit_field">
            <span class="ef_label">Name</span>
            <input v-model="draft.name" :class="['ef_input', { is_good: isFieldGood('name', draft.name) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">City</span>
            <input v-model="draft.city" :class="['ef_input', { is_good: isFieldGood('city', draft.city) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Region/State</span>
            <input v-model="draft.region" :class="['ef_input', { is_good: isFieldGood('region', draft.region) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Leaders (comma-separated)</span>
            <textarea v-model="leadersCsv" :class="['ef_textarea','auto_grow', { is_good: isFieldGood('leaders', leadersCsv) }]" rows="1"></textarea>
          </label>
          <label class="edit_field">
            <span class="ef_label">Members count</span>
            <input v-model.number="draft.members_count" type="number" min="0" :class="['ef_input', { is_good: isFieldGood('members_count', draft.members_count) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Avg practice size</span>
            <input v-model.number="draft.avg_practice_size" type="number" min="0" :class="['ef_input', { is_good: isFieldGood('avg_practice_size', draft.avg_practice_size) }]" />
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Practice/training text</span>
            <textarea v-model="trainingText" :class="['ef_textarea','auto_grow', { is_good: isFieldGood('training', trainingText) }]" rows="1" placeholder="e.g., Wed 6pm - 9pm"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Description</span>
            <textarea v-model="draft.desc" :class="['ef_textarea','auto_grow', { is_good: isFieldGood('desc', draft.desc) }]" rows="2"></textarea>
          </label>
          <label class="edit_field">
            <span class="ef_label">Facebook URL</span>
            <input v-model="draft.facebook" :class="['ef_input', { is_good: isFieldGood('url', draft.facebook) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Instagram URL</span>
            <input v-model="draft.instagram" :class="['ef_input', { is_good: isFieldGood('url', draft.instagram) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Medals this year</span>
            <input v-model.number="draft.medals_this_year" type="number" min="0" :class="['ef_input', { is_good: isFieldGood('number', draft.medals_this_year) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Supermatches hosted</span>
            <input v-model.number="draft.supermatches_hosted" type="number" min="0" :class="['ef_input', { is_good: isFieldGood('number', draft.supermatches_hosted) }]" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Supermatches upcoming</span>
            <input v-model.number="draft.supermatches_upcoming" type="number" min="0" :class="['ef_input', { is_good: isFieldGood('number', draft.supermatches_upcoming) }]" />
          </label>
          <label class="edit_field checkbox">
            <input type="checkbox" v-model="draft.out_of_state" />
            <span>Out of State</span>
          </label>
        </div>
      </div>
      </div>

      <div class="actions_bottom">
        <div v-if="edit_mode" class="edit_actions">
          <button class="ghost_btn" @click="discardEdit">Discard</button>
          <button class="primary_btn" @click="saveEdit">Save</button>
        </div>
        <button v-if="!edit_mode && $route?.query?.from==='athlete'" class="back_from_club" @click="goBackToAthlete" aria-label="Back to athlete details">
          <svg class="back_icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Back
        </button>
        <button v-if="!edit_mode" class="close_action_btn" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>
<script>
import { isDevMode } from '../utils/devMode'
export default {
  name: 'ClubDetails',
  props: {
    open: { type: Boolean, default: false },
    club: { type: Object, required: true },
    rankings_tab_name_men: { type: String, required: true },
    weights_tab_name_men: { type: String, required: true },
    rankings_tab_name_women: { type: String, required: true },
    weights_tab_name_women: { type: String, required: true },
    classes_men: { type: Array, required: true },
    classes_women: { type: Array, required: true },
    max_initial_members: { type: Number, default: 5 },
  },
  data(){
    const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
    const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
    const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()
    return {
      dev:false,
      edit_mode:false,
      draft:null,
      show_all:false,
      open_tip_key:'',
      tip_timer:null,
      sheet_id,
      phone_revealed:false,
      // class ranks per division and hand
      rank_left_men_cls: new Map(),
      rank_right_men_cls: new Map(),
      rank_left_women_cls: new Map(),
      rank_right_women_cls: new Map(),
      // overall ranks per division and hand
      rank_left_men_overall: new Map(),
      rank_right_men_overall: new Map(),
      rank_left_women_overall: new Map(),
      rank_right_women_overall: new Map(),
      // weight maps
      weight_men: new Map(),
      weight_women: new Map(),
      // mock stats
      avg_practice_size: 12,
      medals_this_year: 159,
      supermatches_hosted: 13,
    }
  },
  computed:{
    leadersCsv:{
      get(){ return (Array.isArray(this.draft?.leaders) ? this.draft.leaders : []).join(', ') },
      set(v){ const arr = String(v||'').split(',').map(s=>s.trim()).filter(Boolean); this.draft.leaders = arr }
    },
    trainingText:{
      get(){ return (Array.isArray(this.draft?.training) ? this.draft.training : []).join(' • ') },
      set(v){ const arr = String(v||'').split(/•|\,|\n/).map(s=>s.trim()).filter(Boolean); this.draft.training = arr }
    },
    members(){
      return Array.isArray(this.club?.members) ? this.club.members : []
    },
    leader_is_multiple(){
      return Array.isArray(this.club?.leaders) && this.club.leaders.length > 1
    },
    leader_display(){
      return this.leader_is_multiple ? 'Multiple' : this.leader_name
    },
    is_amity(){ return (this.club?.name || '') === 'Amity Wrist Breakers' },
    first_members(){
      return this.members.slice(0, this.max_initial_members)
    },
    extra_members(){
      return this.members.slice(this.max_initial_members)
    },
    first_members_count(){
      return this.first_members.length
    },
    leader_name(){
      return Array.isArray(this.club?.leaders) && this.club.leaders.length ? this.club.leaders[0] : '—'
    },
    leader_footer_obj(){
      const v = this.club && this.club.leader_footer
      if(!v) return null
      if(typeof v === 'string'){
        return { num:'', tail:` ${v}` }
      }
      if(v && typeof v === 'object' && 'tail' in v){
        const num = typeof v.num === 'string' ? v.num : String(v.num || '')
        return { num, tail: String(v.tail || '') }
      }
      if(v && typeof v === 'object' && ('num2' in v || 'tail_before' in v)){
        const num = String(v.num || '')
        const tail_before = String(v.tail_before || '')
        const num2 = String(v.num2 || '')
        const tail_after = String(v.tail_after || '')
        return { mode:'dual', num, tail_before, num2, tail_after }
      }
      return null
    },
    leader_highlight(){
      const name = (this.leader_name || '').trim()
      if(!name || name === 'TBD') return null
      const cands = []
      const menW = this.weight_men.get(name)
      const womenW = this.weight_women.get(name)
      const pushOverall = (rank, hand, division)=>{ if(rank === 1) cands.push({ rank, hand, division, isOverall:true }) }
      const pushClass = (rank, hand, weight, division)=>{ if(rank && Number.isFinite(rank)) cands.push({ rank, hand, weight, division, isOverall:false }) }
      // men
      pushOverall(this.rank_right_men_overall.get(name), 'RH', 'Men')
      pushOverall(this.rank_left_men_overall.get(name), 'LH', 'Men')
      pushClass(this.rank_right_men_cls.get(name), 'RH', menW, 'Men')
      pushClass(this.rank_left_men_cls.get(name), 'LH', menW, 'Men')
      // women
      pushOverall(this.rank_right_women_overall.get(name), 'RH', 'Women')
      pushOverall(this.rank_left_women_overall.get(name), 'LH', 'Women')
      pushClass(this.rank_right_women_cls.get(name), 'RH', womenW, 'Women')
      pushClass(this.rank_left_women_cls.get(name), 'LH', womenW, 'Women')
      if(cands.length === 0) return null
      // Prefer overall, then lower rank
      cands.sort((a,b)=>{
        const ao = a.isOverall ? 0 : 1
        const bo = b.isOverall ? 0 : 1
        if(ao !== bo) return ao - bo
        return a.rank - b.rank
      })
      const best = cands[0]
      // Try to collapse to both hands if equal context
      const same = cands.find(x => x !== best && x.rank === best.rank && x.isOverall === best.isOverall && (best.isOverall || x.weight === best.weight) && x.division === best.division)
      const hand = same ? 'both' : best.hand
      const divLabel = best.division === 'Women' ? " Women's" : ''
      const num = `#${best.rank}`
      let tail = ''
      if(best.isOverall){
        tail = `${divLabel} overall ${hand}`
      }else{
        tail = `${divLabel} ${best.weight}lbs ${hand}`
      }
      return { num, tail: ` ${tail} in the state` }
    },
    city_label(){
      return (this.club?.city || '').trim() || 'City'
    },
    location_rank(){
      const n = Number(this.club?.city_medal_rank)
      return Number.isFinite(n) && n > 0 ? n : 1
    },
    members_footer_prefix(){
      return this.club?.members_footer_prefix || ''
    },
    members_footer_accent(){
      return this.club?.members_footer_accent || '—'
    },
    members_footer_tail(){
      return this.club?.members_footer_tail || ''
    },
    avg_practice_footer_accent(){
      return this.club?.avg_practice_footer_accent || '—'
    },
    avg_practice_footer_tail(){
      return this.club?.avg_practice_footer_tail || ''
    },
    is_brute(){ return (this.club?.name || '') === 'Brute Squad' },
    practice_text(){
      const arr = Array.isArray(this.club?.training) ? this.club.training : []
      const txt = arr.filter(Boolean).join(' • ')
      return txt
    },
    practice_day(){
      const txt = (this.practice_text || '').toLowerCase()
      const names = {
        sunday:'Sunday', monday:'Monday', tuesday:'Tuesday', wednesday:'Wednesday', thursday:'Thursday', friday:'Friday', saturday:'Saturday',
        sun:'Sunday', mon:'Monday', tue:'Tuesday', tues:'Tuesday', wed:'Wednesday', thu:'Thursday', thur:'Thursday', thurs:'Thursday', fri:'Friday', sat:'Saturday'
      }
      for(const [k,label] of Object.entries(names)){
        const re = new RegExp(`\\b${k}s?\\b`, 'i')
        if(re.test(txt)) return label
      }
      return ''
    },
    practice_start(){
      const txt = (this.practice_text || '')
      const m = txt.match(/\b(\d{1,2}(:\d{2})?\s?(am|pm))\b/i)
      return m ? m[1].replace(/\s+/g,'').toLowerCase().replace(/am|pm/, s=>s.toLowerCase()) : ''
    },
    practice_end(){
      const txt = (this.practice_text || '')
      const m = txt.match(/-\s*(\d{1,2}(:\d{2})?\s?(am|pm))\b/i)
      if(m) return m[1].replace(/\s+/g,'').toLowerCase().replace(/am|pm/, s=>s.toLowerCase())
      return this.practice_start ? '9:00pm' : ''
    },
    has_practice(){ return this.practice_text.length > 0 },
    card_count_without_practice(){
      // Leader, Members, Location, Average always present
      let n = 4
      if(this.club?.out_of_state === true) n++
      if(this.show_talent_card) n++
      if(this.has_medals) n++
      if(this.has_supermatches) n++
      return n
    },
    show_practice_card(){
      if(!this.has_practice) return false
      if(this.card_count_without_practice < 6) return true
      // if already 6 or more, replace medals; for Brute Squad specifically, we will hide supermatches instead
      if(this.is_amity) return true
      return this.has_medals || this.is_brute
    },
    show_medals_card(){
      if(!this.has_medals) return false
      if(this.card_count_without_practice < 6) return true
      // if already 6+, hide medals if we're showing practice and not Brute Squad
      if(this.is_amity) return false
      if(this.show_practice_card && !this.is_brute) return false
      return true
    },
    show_supermatches_card(){
      if(!this.has_supermatches) return false
      // if Brute Squad and practice card is showing, hide supermatches
      if(this.is_brute && this.show_practice_card) return false
      return true
    },
    show_talent_card(){
      const n = this.club?.name || ''
      return ['Grip Titans','Capital City Grippers','Amity Wrist Breakers'].includes(n) && !!this.club?.talent_metric
    },
    talent_label(){
      const base = this.club?.talent_metric?.label || ''
      return base ? `${base} (top 10)` : ''
    },
    talent_number(){
      const n = Number(this.club?.talent_metric?.count)
      return Number.isFinite(n) ? `${n}` : ''
    },
    talent_footer_accent(){
      return this.club?.talent_metric?.footer_accent || '—'
    },
    talent_footer_tail(){
      return this.club?.talent_metric?.footer_tail || ''
    },
    has_medals(){
      return Number.isFinite(Number(this.club?.medals_this_year))
    },
    has_supermatches(){
      return Number.isFinite(Number(this.club?.supermatches_hosted))
    },
    medals_this_year_value(){
      return this.club?.medals_this_year ?? this.medals_this_year
    },
    medals_footer_accent(){
      return this.club?.medals_footer_accent || '#1'
    },
    medals_footer_tail(){
      return this.club?.medals_footer_tail || ' in the state'
    },
    supermatches_hosted_value(){
      return this.club?.supermatches_hosted ?? this.supermatches_hosted
    },
    supermatches_upcoming_value(){
      const n = Number(this.club?.supermatches_upcoming)
      return Number.isFinite(n) ? n : 0
    },
    location_label(){
      const city = (this.club?.city || '').trim()
      const region = (this.club?.region || '').trim()
      const isOOS = this.club?.out_of_state === true || /washington/i.test(region)
      if(isOOS){
        if(city && region) return `${city} ${region}`
        if(region) return region
        return city || '—'
      }
      if(city) return `${city} Oregon`
      return region ? `${region} Oregon` : 'Oregon'
    },
    facebook_url(){
      return this.club?.facebook || ''
    },
    instagram_url(){
      return this.club?.instagram || ''
    },
    show_phone_button(){
      return (this.club?.name || '') === 'Amity Wrist Breakers'
    },
    phone_display(){
      return '(971) 901-5867'
    },
    phone_tel_href(){
      return 'tel:+19719015867'
    },
  },
  methods:{
    isFieldGood(kind, value){
      try{
        const v = (value==null?'' : String(value)).trim()
        if(kind==='number') return String(value).trim() !== '' && Number(value) >= 0
        if(kind==='url') return !v || /^https?:\/\//i.test(v)
        if(kind==='leaders') return v.length>0
        if(kind==='name' || kind==='city' || kind==='region' || kind==='desc' || kind==='training') return v.length>0
        return !!v
      }catch{ return false }
    },
    onCloseClick(){ this.edit_mode = false; this.$emit('close') },
    startEdit(){ this.edit_mode = true; this.draft = this.makeDraftFromClub() },
    discardEdit(){ this.edit_mode = false; this.draft = this.makeDraftFromClub() },
    saveEdit(){
      const d = this.draft || {}
      // basic fields
      this.club.name = d.name
      this.club.city = d.city
      this.club.region = d.region
      this.club.members_count = d.members_count
      this.club.avg_practice_size = d.avg_practice_size
      this.club.training = Array.isArray(d.training) ? d.training.slice() : []
      this.club.leaders = Array.isArray(d.leaders) ? d.leaders.slice() : []
      this.club.members = Array.isArray(this.club.members) ? this.club.members.slice() : []
      this.club.out_of_state = !!d.out_of_state
      this.club.facebook = d.facebook
      this.club.instagram = d.instagram
      this.club.desc = d.desc
      // metrics
      this.club.medals_this_year = d.medals_this_year
      this.club.supermatches_hosted = d.supermatches_hosted
      this.club.supermatches_upcoming = d.supermatches_upcoming
      if(d.talent_metric){ this.club.talent_metric = { ...(this.club.talent_metric||{}), ...d.talent_metric } }
      this.edit_mode = false
    },
    makeDraftFromClub(){
      const c = this.club || {}
      return {
        name: c.name || '',
        city: c.city || '',
        region: c.region || '',
        members_count: c.members_count ?? (Array.isArray(c.members) ? c.members.length : 0),
        avg_practice_size: c.avg_practice_size ?? this.avg_practice_size,
        training: Array.isArray(c.training) ? c.training.slice() : [],
        leaders: Array.isArray(c.leaders) ? c.leaders.slice() : [],
        out_of_state: !!c.out_of_state,
        facebook: c.facebook || '',
        instagram: c.instagram || '',
        desc: c.desc || '',
        medals_this_year: c.medals_this_year ?? this.medals_this_year,
        supermatches_hosted: c.supermatches_hosted ?? this.supermatches_hosted,
        supermatches_upcoming: c.supermatches_upcoming ?? 0,
        talent_metric: c.talent_metric ? { ...c.talent_metric } : null,
      }
    },
    goBackToAthlete(){
      try{
        const ath = String(this.$route?.query?.ath || '').trim()
        const div = String(this.$route?.query?.div || '').trim()
        this.$emit('close')
        this.$router.push({ name:'leaderboards', query:{ goto:'athlete', ath, div } })
      }catch{}
    },
    onOverlayWheel(evt){ try{ if(evt && evt.target === evt.currentTarget) evt.preventDefault() }catch{} },
    onOverlayTouchMove(evt){ try{ if(evt && evt.target === evt.currentTarget) evt.preventDefault() }catch{} },
    resolveImage(path){
      const base = (import.meta && import.meta.env && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/'
      const p = String(path || '').trim()
      if(!p) return base + 'default_club.png'
      if(/^https?:\/\//i.test(p)) return p
      return base + p.replace(/^\//,'')
    },
    toggleShowAll(){ this.show_all = !this.show_all },
    toggleTip(key){
      this.open_tip_key = this.open_tip_key === key ? '' : key
      if(this.tip_timer){ clearTimeout(this.tip_timer); this.tip_timer = null }
      if(this.open_tip_key){ this.tip_timer = setTimeout(()=>{ this.open_tip_key = '' }, 2200) }
    },
    heroBg(url){
      const u = this.resolveImage(url || 'default_club.png')
      return `linear-gradient(180deg, rgba(0,0,0,.25), rgba(0,0,0,.55)), url('${u}')`
    },
    gvizCsv(tab){
      return `https://docs.google.com/spreadsheets/d/${this.sheet_id}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(tab)}`
    },
    async loadData(){
      try{
        const [rm, wm, rw, ww] = await Promise.all([
          fetch(this.gvizCsv(this.rankings_tab_name_men)).then(r=>r.text()),
          fetch(this.gvizCsv(this.weights_tab_name_men)).then(r=>r.text()),
          fetch(this.gvizCsv(this.rankings_tab_name_women)).then(r=>r.text()),
          fetch(this.gvizCsv(this.weights_tab_name_women)).then(r=>r.text()),
        ])
        const rankRowsM = this.csvToRows(rm)
        const rankRowsW = this.csvToRows(rw)
        const weightRowsM = this.csvToRows(wm)
        const weightRowsW = this.csvToRows(ww)
        // Build weight maps first
        this.weight_men = this.makeWeightMap(weightRowsM, this.classes_men)
        this.weight_women = this.makeWeightMap(weightRowsW, this.classes_women)
        // Then compute class ranks by hand and division
        this.rank_left_men_cls = this.makeClassRankIndex(rankRowsM, 0, this.weight_men)
        this.rank_right_men_cls = this.makeClassRankIndex(rankRowsM, 2, this.weight_men)
        this.rank_left_women_cls = this.makeClassRankIndex(rankRowsW, 0, this.weight_women)
        this.rank_right_women_cls = this.makeClassRankIndex(rankRowsW, 2, this.weight_women)
        // Overall ranks (absolute sheet order)
        this.rank_left_men_overall = this.makeOverallIndex(rankRowsM, 0)
        this.rank_right_men_overall = this.makeOverallIndex(rankRowsM, 2)
        this.rank_left_women_overall = this.makeOverallIndex(rankRowsW, 0)
        this.rank_right_women_overall = this.makeOverallIndex(rankRowsW, 2)

        
      }catch(e){ console.error('Failed loading rank/weight data', e) }
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
    makeOverallIndex(rows, nameCol){
      const idx = new Map()
      rows.slice(1).forEach((r,i)=>{
        const name = (r[nameCol] || '').trim()
        if(!name) return
        idx.set(name, i+1)
      })
      return idx
    },
    csvToRows(csv){
      return csv.trim().split(/\r?\n/).map(line=>{
        const out = []
        let cur = ''
        let q = false
        for (let i = 0; i < line.length; i++){
          const ch = line[i]
          if(ch === '"'){ q = !q; continue }
          if(ch === ',' && !q){ out.push(cur); cur = '' } else { cur += ch }
        }
        out.push(cur)
        return out.map(s=>s.trim())
      })
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
    isClubLeader(name){
      const leaders = Array.isArray(this.club?.leaders) ? this.club.leaders : []
      const target = String(name || '').trim().toLowerCase()
      return leaders.some(l => String(l || '').trim().toLowerCase() === target)
    },
    allBadges(name){
      const out = []
      // Class-based top 10
      const lm = this.rank_left_men_cls.get(name)
      const rm = this.rank_right_men_cls.get(name)
      const wm = this.weight_men.get(name)
      if(lm && lm <= 10){ out.push(this.makeBadge(name, lm, 'LH', wm, 'Men')) }
      if(rm && rm <= 10){ out.push(this.makeBadge(name, rm, 'RH', wm, 'Men')) }
      const lw = this.rank_left_women_cls.get(name)
      const rw = this.rank_right_women_cls.get(name)
      const ww = this.weight_women.get(name)
      if(lw && lw <= 10){ out.push(this.makeBadge(name, lw, 'LH', ww, 'Women')) }
      if(rw && rw <= 10){ out.push(this.makeBadge(name, rw, 'RH', ww, 'Women')) }
      // Overall precedence: only if #1 overall
      const olm = this.rank_left_men_overall.get(name)
      const orm = this.rank_right_men_overall.get(name)
      const olw = this.rank_left_women_overall.get(name)
      const orw = this.rank_right_women_overall.get(name)
      if(olm === 1){ out.push(this.makeBadge(name, 1, 'LH', 'overall', 'Men', true)) }
      if(orm === 1){ out.push(this.makeBadge(name, 1, 'RH', 'overall', 'Men', true)) }
      if(olw === 1){ out.push(this.makeBadge(name, 1, 'LH', 'overall', 'Women', true)) }
      if(orw === 1){ out.push(this.makeBadge(name, 1, 'RH', 'overall', 'Women', true)) }

      // Sort by: overall first, then trophy, then lower rank
      return out
        .filter(b => !!b.weight)
        .sort((a,b)=>{
          const ao = a.isOverall ? 0 : 1
          const bo = b.isOverall ? 0 : 1
          if(ao !== bo) return ao - bo
          const at = a.rank <= 3 ? 0 : 1
          const bt = b.rank <= 3 ? 0 : 1
          if(at !== bt) return at - bt
          return a.rank - b.rank
        })
    },
    bestBadge(name){
      const badges = this.allBadges(name)
      if(badges.length === 0) return null
      const first = badges[0]
      // Collapse both-hands if same rank and same context (overall or same weight)
      const sameKey = (b)=> `${b.division}|${b.isOverall ? 'overall' : b.weight}`
      const other = badges.find(b => b !== first && b.rank === first.rank && sameKey(b) === sameKey(first))
      if(other){
        const hand = 'both'
        return { ...first, hand, tooltip: this.tooltipText(first.name, first.rank, first.isOverall ? 'overall' : first.weight, hand, first.division) }
      }
      return first
    },
    makeBadge(name, rank, hand, weight, division, isOverall=false){
      const type = rank <= 3 ? 'trophy' : (rank <= 5 ? 'top10_a' : 'top10_b')
      return { name, rank, hand, weight, division, isOverall, type, tooltip: this.tooltipText(name, rank, weight, hand, division, isOverall) }
    },
    tooltipText(name, rank, weight, hand, division, isOverall=false){
      const handLabel = hand === 'both' ? 'both' : (hand === 'LH' ? 'LH' : 'RH')
      const divLabel = division === 'Women' ? "Women's" : ''
      let wtLabel = ''
      if(isOverall){
        wtLabel = 'overall'
      }else{
        wtLabel = String(weight).includes('overall') ? 'overall' : `${weight}lbs${String(weight).includes('+') && !String(weight).endsWith('lbs') ? '' : ''}`
      }
      return this.titleCaseTooltip(`#${rank} ${divLabel ? divLabel + ' ' : ''}${wtLabel} ${handLabel}`.trim())
    },
    titleCaseTooltip(text){
      const str = String(text == null ? '' : text)
      return str.replace(/[A-Za-z][A-Za-z']*/g, (w)=>{
        const up = w.toUpperCase()
        if(up === 'RH' || up === 'LH') return up
        const low = w.toLowerCase()
        return low.charAt(0).toUpperCase() + low.slice(1)
      })
    },
    makeClassRankIndexStrict(rows, nameCol, weightMap){
      const out = new Map()
      let lastClass = null
      let counter = 0
      rows.slice(1).forEach(r=>{
        const name = (r[nameCol] || '').trim()
        if(!name) return
        const cls = weightMap.get(name)
        if(!cls) return
        if(cls !== lastClass){ counter = 1; lastClass = cls } else { counter += 1 }
        out.set(name, counter)
      })
      return out
    }
  },
  watch:{
    open(val){
      try{
        const body = document && document.body
        if(body){ body.style.overflow = val ? 'hidden' : '' }
      }catch{}
      if(val){ this.loadData(); try{ this.dev = isDevMode() }catch{}; this.draft = this.makeDraftFromClub() }
    }
  },
}
</script>
<style scoped>
.overlay{position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:flex-start; justify-content:center; --ovPad:12px; padding:var(--ovPad); z-index:100; overflow:hidden; overflow-x:hidden}
.modal{width:100%; max-width:min(860px, calc(100vw - (var(--ovPad) * 2))); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); border:1px solid var(--border); border-radius:16px; box-shadow:var(--glow); display:flex; flex-direction:column; overflow:hidden; max-height:calc(100dvh - (var(--ovPad) * 2)); overflow-x:hidden}
.scroll_area{flex:1; overflow:auto; -webkit-overflow-scrolling:touch; overflow-x:hidden}
.content{padding:0 0 0 0}
.content{ scrollbar-width: none; -ms-overflow-style: none }
.content::-webkit-scrollbar{ width:0; height:0 }
.modal_header{display:flex; align-items:center; justify-content:flex-start; gap:10px; padding:14px 16px; border-bottom:1px solid var(--border)}
.modal_title{margin:0}
.spacer{flex:1}
/* Header close button */
.close_btn{background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.04)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:6px 12px; cursor:pointer; font-size:20px; line-height:1; transition:.18s ease}
.close_btn:hover{filter:brightness(1.08)}

/* Edit icon button */
.icon_btn{background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:8px; padding:6px; cursor:pointer}
.icon_btn .icon{width:18px; height:18px; display:block; fill:currentColor}
.icon_btn:hover{color:var(--text)}

/* Stats cards */
.stats_row{display:grid; grid-template-columns:repeat(auto-fit, minmax(220px,1fr)); gap:14px; padding:16px}
.stat_card{position:relative; overflow:visible; background:rgba(255,255,255,.02); border:1px solid var(--border); border-radius:12px; padding:20px 14px 12px 14px}
.stat_icon{position:absolute; top:-16px; left:14px; width:46px; height:46px; border-radius:999px; display:flex; align-items:center; justify-content:center; box-shadow:var(--glow); border:1px solid rgba(215,180,58,.35)}
.stat_icon svg{width:24px; height:24px; display:block}
.crown_icon_bubble{background:linear-gradient(180deg, rgba(215,180,58,.68), rgba(185,147,34,.62)); color:#070e1c}
.users_icon_bubble{background:linear-gradient(180deg, rgba(20,130,150,.68), rgba(12,100,120,.62)); color:#0b1630}
.location_icon_bubble{background:linear-gradient(180deg, rgba(255,255,255,.68), rgba(245,245,245,.62)); color:#0b1630}
.active_icon_bubble{background:linear-gradient(180deg, rgba(243,156,18,.68), rgba(230,126,34,.62)); color:#0b1630}
.trophy_icon_bubble{background:linear-gradient(180deg, rgba(215,180,58,.68), rgba(185,147,34,.62)); color:#070e1c}
.trophy_icon_bubble svg{ transform: translateY(2px) }
.match_icon_bubble{background:linear-gradient(180deg, rgba(52,152,219,.68), rgba(52,152,219,.62)); color:#0b1630}
.stat_body{padding-top:10px}
.stat_label{color:var(--muted); font-weight:800; font-size:12px}
.stat_value{font-weight:900; font-size:18px}
.stat_divider{height:1px; background:var(--border); margin:10px -14px 8px -14px}
.stat_footer{font-weight:700; color:#c9d2ea; font-size:12px}
.stat_footer .accent{color:#12d1e6}

/* Join box */
.join_box{display:grid; grid-template-columns:320px 1fr; gap:14px; padding:0 16px 16px; align-items:center}
.join_img{border-radius:12px; height:210px; background-size:cover; background-position:center}
.join_body{display:flex; align-items:center; gap:12px; flex-wrap:wrap}
.join_text{font-weight:800}
.join_desc{color:var(--muted); font-weight:700}

/* Social buttons */
.social_btn{display:inline-flex; align-items:center; gap:8px; padding:10px 14px; border-radius:10px; font-weight:900; text-decoration:none; cursor:pointer; border:1px solid transparent}
.social_btn .social_icon{width:16px; height:16px; display:block}
.fb_btn{color:#fff; background:linear-gradient(180deg, #1877f2, #145db6); border-color:rgba(0,0,0,.12); box-shadow:0 4px 14px rgba(20,93,182,.28)}
.fb_btn:hover{filter:brightness(1.06)}
.fb_btn.disabled{opacity:.6; cursor:not-allowed; filter:none}
.ig_btn{color:#fff; background:linear-gradient(45deg, #f58529, #dd2a7b, #8134af, #515bd4); border:none; box-shadow:0 4px 14px rgba(221,42,123,.28)}
.ig_btn:hover{filter:brightness(1.06)}

.list_wrap{padding:0 16px 16px}
.edit_panel{padding:0 16px 16px}
.edit_grid{display:grid; grid-template-columns:1fr; gap:10px}
.edit_field{display:flex; flex-direction:column; gap:6px}
.edit_field.checkbox{flex-direction:row; align-items:center}
.edit_field.span2{grid-column:span 2}
.ef_label{color:var(--muted); font-weight:800; font-size:12px}
.ef_input{background:linear-gradient(180deg, rgba(215,180,58,.18), rgba(185,147,34,.16)); color:var(--text); border:1px solid rgba(215,180,58,.35); border-radius:10px; padding:10px 12px; font-weight:900; width:100%; max-width:100%; box-sizing:border-box; overflow-wrap:anywhere; word-break:break-word}
.ef_textarea{background:linear-gradient(180deg, rgba(215,180,58,.18), rgba(185,147,34,.16)); color:var(--text); border:1px solid rgba(215,180,58,.35); border-radius:10px; padding:10px 12px; min-height:80px; font-weight:900; width:100%; max-width:100%; box-sizing:border-box; overflow-wrap:anywhere; word-break:break-word}
.ef_input.is_good, .ef_textarea.is_good{ border:1px solid rgba(23,162,184,.55); background:linear-gradient(180deg,#20c997,#17a2b8); color:#061626 }
.auto_grow{resize:vertical; width:100%; overflow:auto}
.list_head{display:flex; align-items:center; justify-content:space-between; padding:10px 0}
.member_list{list-style:none; margin:0; padding:0; display:grid; grid-template-columns:1fr; gap:8px}
.member_item{display:flex; align-items:center; gap:10px; padding:8px 10px; border:1px solid var(--border); border-radius:10px; background:rgba(255,255,255,.02)}
.badge_wrap{display:flex; gap:6px; min-width:64px}
.leader_wrap{margin-left:auto; display:flex; align-items:center}
.rank_badge{display:inline-flex; align-items:center; justify-content:center; min-width:28px; height:28px; padding:0 8px; border-radius:999px; font-weight:900; font-size:12px; position:relative}
.rank_badge.top10_a{background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)); color:var(--accent); border:1px solid rgba(215,180,58,.35)}
.rank_badge.top10_b{background:rgba(255,255,255,.12); color:#9fb0d0; border:1px solid rgba(255,255,255,.18)}
.icon{width:18px; height:18px}
.crown{background:linear-gradient(180deg, rgba(215,180,58,.2), rgba(185,147,34,.18)); color:var(--accent); border:1px solid rgba(215,180,58,.45); width:28px; height:28px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center}
.crown_icon{fill:currentColor}
.badge_text{line-height:1}
.member_name{font-weight:800}
.bottom_row{padding-top:10px; display:flex; justify-content:flex-end}

/* Trophy SVG (same style as leaderboard) with number overlay */
.trophy{ position:relative; display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; transform: translateY(4px) }
.trophy svg{ width:30px; height:30px; display:block }
.trophy_1 svg{ fill: var(--accent) }
.trophy_2 svg{ fill: var(--silver) }
.trophy_3 svg{ fill: var(--bronze) }
.trophy_num{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:13px; color:#0b1630; text-shadow:0 1px 0 rgba(255,255,255,.45); transform: translateY(-6px); pointer-events:none }
.trophy_2 .trophy_num,
.trophy_3 .trophy_num{ transform: translate(-2px, -7px) }

/* Buttons styling to match app */
.primary_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:10px;border:1px solid rgba(215,180,58,.22);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16));color:var(--text);font-weight:800;text-decoration:none;cursor:pointer}
.primary_btn.disabled{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); color:var(--muted); cursor:not-allowed; pointer-events:none}
/* replaced above with improved ghost_btn */

/* Phone/ghost buttons */
.ghost_btn{display:inline-flex; align-items:center; gap:8px; padding:10px 14px; border-radius:10px; border:1px solid #eef2f7; color:#0b1630; background:#ffffff; cursor:pointer; box-shadow:0 4px 12px rgba(0,0,0,.08)}
.ghost_btn:hover{filter:none; box-shadow:0 6px 16px rgba(0,0,0,.12)}
.phone_icon{width:16px; height:16px; display:block; fill:currentColor}

/* Tooltip popover for badges */
.badge_btn{ position:relative; cursor:pointer }
.badge_btn .tip{ position:absolute; bottom:calc(100% + 8px); left:0; right:auto; transform:translateX(0) translateY(6px); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); color:var(--text); border:1px solid var(--border); border-radius:10px; padding:8px 10px; display:inline-block; min-width:0; width:max-content; max-width:min(78vw, 320px); white-space:normal; overflow-wrap:anywhere; word-break:normal; text-align:left; font-weight:800; font-size:12px; box-shadow:var(--glow); opacity:0; pointer-events:none; transition:opacity .16s ease, transform .16s ease; z-index:2 }
.badge_btn .tip::after{ content:""; position:absolute; top:100%; left:14px; transform:translateX(0); width:0; height:0; border-left:6px solid transparent; border-right:6px solid transparent; border-top:6px solid var(--border) }
/* Right-align crown tooltip to avoid viewport overflow */
.crown.badge_btn .tip{ right:0; left:auto; text-align:right; width:max-content; min-width:0; max-width:min(78vw, 320px) }
.crown.badge_btn .tip::after{ left:auto; right:14px }
.badge_btn:hover .tip, .badge_btn.show .tip{ opacity:1; transform:translateX(0) translateY(0); pointer-events:auto }

@media(max-width:900px){
  .join_box{grid-template-columns:1fr}
}
@media(min-width:760px){ .edit_grid{ grid-template-columns:repeat(2, 1fr) } }
@media(max-width:520px){ .overlay{ --ovPad:8px } }
.edit_grid{ grid-template-columns:1fr }
.label .muted_count{ color: var(--muted); font-weight:700 }

/* Toggle arrow like leaderboard */
.toggle_wrap{ display:flex; align-items:center; justify-content:center; padding:8px 0; background:linear-gradient(180deg, rgba(20,130,150,.10), rgba(12,100,120,.08)); border-top:1px solid var(--border); border-bottom:1px solid var(--border); cursor:pointer; -webkit-tap-highlight-color: transparent; margin-top:8px }
.show_more_button{ display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; border-radius:999px; transition:.18s ease; pointer-events:none }
.toggle_icon{ transition: transform .18s ease }
.show_more_button.is_open .toggle_icon{ transform: rotate(180deg) }

/* Sliding drawer for extra members */
.collapse_wrap{ max-height:0; overflow:hidden; transition:max-height .42s ease; will-change:max-height }
.collapse_wrap.open{ max-height:2000px }
.extra_item{ animation: fadeSlide .34s ease both }
@keyframes fadeSlide{ from{ opacity:0; transform:translateY(6px) } to{ opacity:1; transform:none } }

.actions_bottom{ display:flex; justify-content:flex-end; padding:12px 16px; border-top:1px solid var(--border) }
.edit_actions{margin-right:auto; display:flex; gap:8px}
.back_from_club{ margin-right:auto; display:inline-flex; align-items:center; gap:6px; padding:8px 12px; border-radius:999px; border:1px solid rgba(46,163,255,.35); background:linear-gradient(180deg, rgba(46,163,255,.20), rgba(46,163,255,.14)); color:#c9ebff; font-weight:900; cursor:pointer }
.back_from_club .back_icon{ width:16px; height:16px; display:block }

/* Bottom close button */
.close_action_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; cursor:pointer}

/* Tighten member row vertical padding further */
.member_item{ padding:5px 10px }
.badge_wrap{ min-width:56px }
.talent_icon_bubble{background:linear-gradient(180deg, rgba(46,204,113,.68), rgba(39,174,96,.62)); color:#ffffff; border-color: rgba(215,180,58,.45)}
.talent_icon_bubble svg{ width:32px; height:32px }
.oos_icon_bubble{background:linear-gradient(180deg, rgba(127,140,141,.68), rgba(99,110,114,.62)); color:#0b1630}
.oos_icon_bubble svg{ width:28px; height:28px }
.practice_icon_bubble{background:linear-gradient(180deg, rgba(52,73,94,.68), rgba(44,62,80,.62)); color:#e9eef6}
/* (Reverted) Use default padding/heights so these cards match others */
</style> 