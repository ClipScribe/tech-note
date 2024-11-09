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

const { startAutoDisplayCommentary, stopAutoDisplayCommentary } = useAutoDisplayCommentary();

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

const getVideoIdFromUrl = (url: string): string | null => {
  const match = url.match(
      /^https:\/\/www\.youtube\.com\/watch\?v=([\w-]{11})$/
  );
  return match ? match[1] : null;
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

const onPlayerReady = async (event: any) => {
  event.target.playVideo();
  // 해설 생성 시작
  await commentaryStore.generateCommentaries();
  // SSE 완료 후 실행해야 함
  startAutoDisplayCommentary();
};


onMounted(async () => {
  await loadYouTubeAPI();
  initializePlayer();
});

onBeforeUnmount(() => {
  stopAutoDisplayCommentary();
});

</script>

<style scoped>
.video-container {
  flex: 1;
  height: calc(100% - 90px);
  margin-right: 450px;
  padding-right: 450px;
  background-color: black;
  overflow-y: hidden;
  position: fixed;
  width:100%;

}

#player {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .video-container {
    flex: 1;
    width: 100%;
    position: inherit;
    height: 100%;
    margin-right: 0;
    padding-right: 0;
  }

  #player {
    height: 40vw;
    width: 100%;
  }
}
</style>
