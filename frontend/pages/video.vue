<template>
  <div class="video-page">
    <VideoPlayer/>
    <CommentarySidebar/>
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

@media (max-width: 600px) {
  .video-page {
    display: flex;

  }
}

@media (min-width: 601px) and (max-width: 1199px) {
  .video-page {
    display: flex;
  }
}
</style>
