<template>
  <div class="athlete_select" ref="root">
    <div class="input_wrap">
      <input
        ref="input"
        :value="modelValue"
        @input="onInput"
        @focus="open = true"
        @blur="onBlur"
        @keydown.down.prevent="move(1)"
        @keydown.up.prevent="move(-1)"
        @keydown.enter.prevent="onEnter"
        @keydown.esc.stop.prevent="close"
        type="text"
        inputmode="text"
        :placeholder="placeholder || 'Full name'"
        class="input"
        :class="{ valid: blurred && hasValue }"
        autocomplete="off"
        role="combobox"
        aria-autocomplete="list"
        :aria-expanded="String(open)"
        :aria-controls="listId"
        :aria-activedescendant="activeDescId"
      />
      <button v-if="isNewCandidate" type="button" class="add_btn" @mousedown.prevent @click="commitNew">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14m-7-7h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>

    <ul
      v-show="open && (filtered.length > 0 || isNewCandidate)"
      :id="listId"
      class="dropdown"
      role="listbox"
    >
      <li
        v-if="isNewCandidate"
        class="opt add_opt"
        :class="{ active: activeIndex === 0 }"
        role="option"
        :id="optionId(0)"
        @mousedown.prevent
        @click="commitNew"
        @mousemove="setActive(0)"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14m-7-7h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Add "{{ (modelValue || '').trim() }}"
      </li>
      <li
        v-for="(opt, i) in filtered"
        :key="opt"
        class="opt"
        :class="{ active: i + newOffset === activeIndex }"
        role="option"
        :id="optionId(i + newOffset)"
        @mousedown.prevent
        @click="select(opt)"
        @mousemove="setActive(i + newOffset)"
      >
        {{ opt }}
      </li>
    </ul>

    <div v-if="isNewCandidate" class="new_hint">Adding new athlete named {{ (modelValue || '').trim() }}</div>
  </div>
  
</template>

<script>
export default {
  name: 'AthleteSelect',
  props: {
    modelValue: { type: String, default: '' },
    options: { type: Array, default: () => [] },
    placeholder: { type: String, default: 'Full name' },
    blurred: { type: Boolean, default: false },
    idBase: { type: String, default: 'athlete' },
  },
  emits: ['update:modelValue', 'blur'],
  data(){
    return {
      open: false,
      activeIndex: -1,
    }
  },
  computed:{
    normOptions(){
      const seen = new Set()
      return this.options
        .map(s => String(s || '').trim())
        .filter(s => {
          const k = s.toLowerCase()
          if(!s || seen.has(k)) return false
          seen.add(k)
          return true
        })
        .sort((a,b)=>a.localeCompare(b))
    },
    query(){ return String(this.modelValue || '') },
    hasValue(){ return !!this.query.trim() },
    isNewCandidate(){
      const q = this.query.trim()
      if(!q) return false
      const lower = q.toLowerCase()
      return !this.normOptions.some(o => o.toLowerCase() === lower)
    },
    filtered(){
      const q = this.query.trim().toLowerCase()
      if(!q) return this.normOptions.slice(0, 20)
      const contains = []
      const starts = []
      for(const o of this.normOptions){
        const ol = o.toLowerCase()
        if(ol.startsWith(q)) starts.push(o)
        else if(ol.includes(q)) contains.push(o)
      }
      return starts.concat(contains).slice(0, 20)
    },
    newOffset(){ return this.isNewCandidate ? 1 : 0 },
    listId(){ return `${this.idBase}-list` },
    activeDescId(){ return this.activeIndex >= 0 ? this.optionId(this.activeIndex) : null },
  },
  methods:{
    optionId(i){ return `${this.idBase}-opt-${i}` },
    onInput(evt){
      const v = String(evt?.target?.value ?? '')
      this.$emit('update:modelValue', v)
      this.open = true
      // reset active index on manual input
      this.activeIndex = this.isNewCandidate ? 0 : (this.filtered.length > 0 ? this.newOffset : -1)
    },
    onBlur(){
      // allow click selection before blur closes
      setTimeout(()=>{ this.open = false }, 0)
      this.$emit('blur')
    },
    close(){ this.open = false; this.activeIndex = -1 },
    select(opt){ this.$emit('update:modelValue', opt); this.close() },
    commitNew(){
      const q = this.query.trim()
      if(!q) return
      this.$emit('update:modelValue', q)
      this.close()
    },
    move(delta){
      const total = this.filtered.length + (this.isNewCandidate ? 1 : 0)
      if(total === 0){ this.activeIndex = -1; return }
      if(this.activeIndex < 0){ this.activeIndex = this.isNewCandidate ? 0 : this.newOffset; return }
      const next = (this.activeIndex + delta + total) % total
      this.activeIndex = next
    },
    onEnter(){
      if(this.activeIndex === 0 && this.isNewCandidate){ this.commitNew(); return }
      const i = this.activeIndex - this.newOffset
      if(i >= 0 && i < this.filtered.length){ this.select(this.filtered[i]); return }
      // no selection highlighted; commit as new if not exact match
      if(this.isNewCandidate){ this.commitNew(); return }
      // else close
      this.close()
    },
    setActive(i){ this.activeIndex = i },
  },
}
</script>

<style scoped>
.athlete_select{ position:relative }
.input_wrap{ position:relative }
.add_btn{ position:absolute; right:6px; top:50%; transform:translateY(-50%); display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:8px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer }
.add_btn svg{ width:18px; height:18px }

.dropdown{ position:absolute; z-index:20; left:0; right:0; max-height:220px; overflow:auto; margin-top:6px; padding:6px; list-style:none; background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.98)); border:1px solid var(--border); border-radius:10px; box-shadow:0 14px 40px rgba(0,0,0,.28) }
.opt{ display:flex; align-items:center; gap:8px; padding:8px 10px; border-radius:8px; cursor:pointer }
.opt:hover, .opt.active{ background:rgba(255,255,255,.06) }
.add_opt{ color:#d7b43a }
.add_opt svg{ width:16px; height:16px }

.new_hint{ margin-top:6px; color:#d7b43a; font-weight:700; font-size:12px }
</style>

