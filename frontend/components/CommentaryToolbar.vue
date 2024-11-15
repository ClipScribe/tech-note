<template>
  <header class="fixed-header flex justify-between mb-2">
    <video-controls/>
    <note-controls/>
  </header>
</template>

<script setup lang="ts">

import VideoControls from "~/components/VideoControls.vue";
</script>

<style scoped>
.fixed-header {
  background-color: white;
  z-index: 10;
  padding: 1.5rem 0 1rem 0;
  border-bottom: 1px solid #dcd9d9;
}

/*  모바일 */
@media (max-width: 768px) {
  .fixed-header {
    margin: 0;
    padding: .5rem 0 .8rem 0;
  }
}
</style>