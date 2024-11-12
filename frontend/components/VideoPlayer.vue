<template>
  <section class="video-container">
    <div v-if="loading" class="v-Loading q-pa-md full-width fixed-top">
      <q-card flat style="max-width: 100%;">
        <q-skeleton style="min-height: 33vh" square />

        <q-card-section>
          <q-skeleton type="text" height="35px"  class="text-subtitle1" />
          <q-skeleton type="text" height="35px"  width="80%" class="text-subtitle1" />
          <q-skeleton type="text" height="35px" class="text-caption" />
        </q-card-section>
      </q-card>
    </div>

    <div  id="player" class="v-Player"></div>
  </section>

</template>

<script setup lang="ts">
import {onBeforeUnmount, onMounted} from "vue";
import {useVideoStore} from "~/stores/videoStore";
import {useCommentaryStore} from "~/stores/commentaryStore";
import {v4 as uuidV4} from "uuid";

definePageMeta({
  middleware: "check-video-url",
});

const videoStore = useVideoStore();
const commentaryStore = useCommentaryStore();

// 로딩 상태를 추적하는 ref
const loading = ref<boolean>(true);

const {startAutoDisplayCommentary, stopAutoDisplayCommentary} = useAutoDisplayCommentary();

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
    videoId: videoId,
    events: {
      onReady: onPlayerReady,
    },
  });
  videoStore.setPlayer(videoPlayer);
  videoStore.setPlayerSize(window.innerWidth);
};

const onPlayerReady = async (event: any) => {
  event.target.playVideo();
  // 해설 생성 시작
  loading.value = false;
  await commentaryStore.generateCommentaries();
  // SSE 완료 후 실행해야 함
  // 비디오 로드가 끝났으므로 로딩 상태를 false로 설정
  startAutoDisplayCommentary();
};

// 서버와의 SSE 연결을 관리할 변수
let eventSource: EventSource;

onMounted(async () => {
  await loadYouTubeAPI();
  initializePlayer();

  const requestId: String = uuidV4();
  eventSource = new EventSource(`http://localhost:8080/sse/connect/${requestId}`);

  eventSource.onmessage = (event) => {
    console.log("Received message:", event.data);
  };

  eventSource.onerror = (error) => {
    console.error("Error receiving SSE:", error);
  };
});

onBeforeUnmount(() => {
  stopAutoDisplayCommentary();
  if (eventSource) {
    console.log("eventSource close");
    eventSource.close()
  }
});

window.addEventListener('resize', () => videoStore.setPlayerSize(window.innerWidth));

</script>

<style scoped>
.video-container {
  position: relative;
  height: 100%;
  min-width: 50%;
  border:1px solid red;
}
.v-Loading {
  width: 100%;
  background-color: white;
  height: 100%;
  position: absolute;
  z-index: 1001;
}

@media (max-width: 768px) {
  .video-container {
    display: flex;
    position: relative;
  }

  #player {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }
}
</style>
