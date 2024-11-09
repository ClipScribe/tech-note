<template>
  <div :id="`c-ST-${commentary.startTime}`" class="c-CT-root content-section  q-shadow-xs">
    <div class="time-Badge-root">
      <span class="time-Badge-inner">{{ formatTime(commentary.startTime) }}</span>
    </div>
    <div v-html="commentary.htmlContent"></div>
  </div>
</template>

<script setup lang="ts">
import {type Commentary} from "~/types/commentary";
import type {PropType} from "vue";
import {useFormatTime} from "~/composables/useFormatTime";

const {formatTime} = useFormatTime();

const props = defineProps({
  commentary: {
    type: Object as PropType<Commentary>,
    required: true,
  },
});
</script>

<style scoped>

</style>