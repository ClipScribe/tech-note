<template>
    <div class="video-container">
      <div id="player"></div>
    </div>
</template>

<script setup lang="ts">
import {onMounted} from "vue";
import {useVideoStore} from "~/stores/videoStore";
import {useCommentaryStore} from "~/stores/commentaryStore";

definePageMeta({
  middleware: "check-video-url",
});

const videoStore = useVideoStore();
const commentaryStore = useCommentaryStore();

const { startAutoDisplay, stopAutoDisplay } = useAutoDisplayCommentary();

const loadYouTubeAPI = () => {
  return new Promise<void>((resolve) => {
    if (window.YT && window.YT.Player) {
      resolve();
    } else {
      const tag = document.createElement("script");
      tag.src = "https://www.youtube.com/iframe_api";
      const firstScriptTag = document.getElementsByTagName("script")[0];
      firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag);

      window.onYouTubeIframeAPIReady = () => {
        resolve();
      };
    }
  });
};

const initializePlayer = () => {
  const videoId = getVideoIdFromUrl(videoStore.getVideoURL());
  if (!videoId) return;

  const videoPlayer = new window.YT.Player("player", {
    height: "100%",
    width: "100%",
    videoId: videoId,
    events: {
      onReady: onPlayerReady,
    },
  });
  videoStore.setPlayer(videoPlayer);
};

const onPlayerReady = (event: any) => {
  event.target.playVideo();
  // SSE 완료 후 실행해야 함
  commentaryStore.generateContentArray();
  startAutoDisplay();
};

// const beginAutoDisplayCommentary = () => {
//   videoStore.intervalId = window.setInterval(async () => {
//     const currentTime: number = player.value.getCurrentTime();
//     console.log("현재 재생 시간:", currentTime);
//     if (!commentaryStore.getIsGenerateCommentariesCompleted()) return;
//     console.log(isFollowingVideo.value);
//     if (!isFollowingVideo.value) return;
//     await commentaryStore.setCommentaryContent(currentTime);
//   }, 1000);
// };

const getVideoIdFromUrl = (url: string): string | null => {
  const match = url.match(
      /^https:\/\/www\.youtube\.com\/watch\?v=([\w-]{11})$/
  );
  return match ? match[1] : null;
};

onMounted(async () => {
  await loadYouTubeAPI();
  initializePlayer();
});
</script>

<style scoped>
.video-container {
  flex: 1;
  margin-right: 450px;
  background-color: black;
}

#player {
  width: 100%;
  height: 100%;
}
</style>
