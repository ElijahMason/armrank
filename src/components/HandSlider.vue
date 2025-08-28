<template>
  <div class="hand_slider_wrap">
    <div
      class="hand_slider"
      role="slider"
      tabindex="0"
      :aria-valuemin="0"
      :aria-valuemax="1"
      :aria-valuenow="isRight ? 1 : 0"
      :aria-valuetext="isRight ? 'Right' : 'Left'"
      @keydown.enter.prevent="toggle"
      @keydown.space.prevent="toggle"
    >
      <div class="track" ref="track" @click="onClick">
        <div class="hand_label left" :class="{ active: !isRight }">Left</div>
        <div class="hand_label right" :class="{ active: isRight }">Right</div>
        <div class="thumb" :class="{ right: isRight }"></div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'HandSlider',
  props: {
    modelValue: { type: String, default: 'RH' }
  },
  emits: ['update:modelValue'],
  computed:{
    isRight(){ return (this.modelValue || '') === 'RH' }
  },
  methods:{
    onClick(evt){
      try{
        const el = this.$refs.track
        const rect = (el && el.getBoundingClientRect) ? el.getBoundingClientRect() : evt.currentTarget.getBoundingClientRect()
        const clickX = evt.clientX - rect.left
        const isRightClick = clickX >= rect.width / 2
        const next = isRightClick ? 'RH' : 'LH'
        const cur = this.isRight ? 'RH' : 'LH'
        if(next !== cur){
          this.$emit('update:modelValue', next)
        }
      }catch{
        // fallback: toggle
        this.toggle()
      }
    },
    toggle(){
      const next = this.isRight ? 'LH' : 'RH'
      this.$emit('update:modelValue', next)
    }
  }
}
</script>
<style scoped>
.hand_slider_wrap{display:flex;justify-content:center}
.hand_slider{display:flex;justify-content:center;padding:2px 0;width:100%}
.track{position:relative;width:100%;max-width:100%;height:44px;border-radius:999px;overflow:hidden}
.track::before{content:'';position:absolute;inset:0;border-radius:999px;background:transparent;border:none}
.thumb{position:absolute;top:3px;left:3px;width:calc(50% - 6px);height:38px;border-radius:999px;background:linear-gradient(180deg,#20c997,#17a2b8);box-shadow:0 10px 24px rgba(23,162,184,.18);transition:transform .22s ease}
.thumb.right{transform:translateX(100%)}
.hand_label{position:absolute;z-index:2;top:50%;transform:translateY(-50%);width:50%;text-align:center;font-weight:900;letter-spacing:.3px;color:var(--muted);pointer-events:none;mix-blend-mode:normal}
.hand_label.left{left:0}
.hand_label.right{left:50%}
.hand_label.active{color:#061626}
</style>
