<template>
  <div class="video-page">
    <video-player/>
    <commentary-note/>
  </div>
</template>

<script setup lang="ts">
import VideoPlayer from "~/components/VideoPlayer.vue";

definePageMeta({
  middleware: "check-video-url",
});

</script>

<style scoped>
.video-page {
  display: flex;
  height: calc(100vh - 90px);
}

@media (max-width: 768px) {
  /* 모바일 스타일 */
  .video-page {
    height: auto;
    align-content: flex-start;
    justify-content: flex-start;
    flex-direction: column;
    align-items: center;
  }
}

</style>
