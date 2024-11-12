<template>
  <div class="video-page">
    <video-player/>
    <commentary-note/>
  </div>
</template>

<script setup lang="ts">
import VideoPlayer from "~/components/VideoPlayer.vue";
import {useTabSync} from "~/composables/useTabSync";

const {syncTabs} = useTabSync();

definePageMeta({
  middleware: "check-video-url",
});

const handleBeforeUnload = () => {
  if (window.location.pathname.includes('/video')) {
    localStorage.setItem('videoInProgress', 'false');
  }
};

onMounted(() => {
  localStorage.setItem('videoInProgress', 'true');
  syncTabs();
  window.addEventListener('beforeunload', handleBeforeUnload);
});

onBeforeUnmount(() => {
  localStorage.setItem('videoInProgress', 'false');
  window.removeEventListener('beforeunload', handleBeforeUnload);
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
