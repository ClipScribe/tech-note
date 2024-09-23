<template>
  <aside class="summary-container">
    <q-card class="no-shadow">
      <header class="fixed-header flex justify-end mb-2">
        <TogglePositionButton/>
      </header>
      <div class="scrollable-content q-pa-md" @scroll="handleScroll">
        <div v-html="content" class="markdown-content" ></div>
      </div>
    </q-card>
  </aside>
</template>

<script setup lang="ts">
import {useCommentaryStore} from "~/stores/commentaryStore";
import {useVideoStore} from "~/stores/videoStore";
import {computed} from "vue";
import {useAutoDisplayCommentary} from "#imports";


const commentaryStore = useCommentaryStore();
const videoStore = useVideoStore();
const { stopAutoDisplay } = useAutoDisplayCommentary();
const content = computed(() => commentaryStore.commentaryContent);

// video 에서
// onMounted(() => {
//   commentaryStore.generateContentArray();
// });

// const handleScroll = () => {
//     if(!videoStore.getFollowVideo()) return;
//     stopAutoDisplay();
//     commentaryStore.setCommentaryContent();
// }
let debounceTimeout: any;
let isGoing = false;

const handleScroll = async () => {
  if (!videoStore.getFollowVideo() && isGoing) return;
  isGoing = true;
  await commentaryStore.setCommentaryContent();
  stopAutoDisplay();
  isGoing = false;
  // clearTimeout(debounceTimeout);
  // debounceTimeout = setTimeout(() => {
  //
  // }, 200); // 100ms 후에 실행
  // isGoing = false;
};
</script>

<style scoped>
.summary-container {
  width: 450px;
  overflow-y: auto;
  position: fixed;
  right:0;
  top: 70px;
}

/* 기본 스타일 설정 */
.markdown-content h1 {
  font-size: 2rem;
}

.markdown-content h2 {
  font-size: 1.75rem;
}

.markdown-content h3 {
  font-size: 1.5rem;
}

.markdown-content p {
  font-size: 1rem;
}

.markdown-content code,
.markdown-content pre {
  font-size: 0.9rem;
}

.fixed-header {
  background-color: white;
  z-index: 10;
  padding: 3rem 0 1rem 0;
  border-bottom: 1px solid #dcd9d9;
}

.scrollable-content {
  overflow-y: auto;
  max-height: calc(100vh - 100px);
}

/*  모바일 */
@media (max-width: 600px) {
  .markdown-content h1 {
    font-size: 1.5rem;
  }

  .markdown-content h2 {
    font-size: 1.3rem;
  }

  .markdown-content h3 {
    font-size: 1.2rem;
  }

  .markdown-content p {
    font-size: 0.9rem;
  }

  .markdown-content code,
  .markdown-content pre {
    font-size: 0.8rem;
  }
}

/* 데스크탑 */
@media (min-width: 1200px) {
  .markdown-content h1 {
    font-size: 2.5rem;
  }

  .markdown-content h2 {
    font-size: 2rem;
  }

  .markdown-content h3 {
    font-size: 1.75rem;
  }

  .markdown-content p {
    font-size: 1.1rem;
  }

  .markdown-content code,
  .markdown-content pre {
    font-size: 1rem;
  }
}
</style>
