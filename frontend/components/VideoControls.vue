<template>
  <div class="q-ml-sm">
    <q-btn v-if="isCommentaryFollowingVideo"
           unelevated
           @click="debouncedStopAutoDisplayCommentary"
           label="영상 따라가기"
           icon="adjust"
           class="toggle-btn q-mr-sm q-pa-x-sm q-pa-y-xs bg-grey-3 text-grey-9 border q-border-grey-3 text-bold no-ripple icon-spacing"
           :class="{'mobile-btn': isMobile}"
    />
    <q-btn v-else
           unelevated
           @click="debouncedStartAutoDisplayCommentary"
           label="자유롭게 보기"
           icon="sticky_note_2"
           class="toggle-btn q-mr-sm q-pa-x-sm q-pa-y-xs bg-grey-3 text-grey-9 border q-border-grey-3 text-bold no-ripple icon-spacing"
           :class="{'mobile-btn': isMobile}"
    />
    <q-btn
        unelevated
        @click="scrollTo"
        label="재생위치로 이동"
        icon="filter_center_focus"
        class="toggle-btn q-mr-sm q-pa-x-sm q-pa-y-xs bg-grey-3 text-grey-9 border q-border-grey-3 text-bold no-ripple icon-spacing"
        :disable="isCommentaryFollowingVideo"
        :class="{'mobile-btn': isMobile}"
    />
  </div>
</template>

<script setup lang="ts">
import {useCommentaryStore} from "~/stores/commentaryStore"
import {useAutoDisplayCommentary} from "~/composables/useAutoDisplayCommentary";
import {useDebounce} from "~/composables/useDebounce";
import {useIsMobile} from "~/composables/useIsMobile";

const { isMobile } = useIsMobile();

const commentaryStore = useCommentaryStore();
const {startAutoDisplayCommentary, stopAutoDisplayCommentary} = useAutoDisplayCommentary();

const {debounce} = useDebounce();
const debouncedStartAutoDisplayCommentary = debounce(startAutoDisplayCommentary, 100);
const debouncedStopAutoDisplayCommentary = debounce(stopAutoDisplayCommentary, 100);
const isCommentaryFollowingVideo = computed(() => commentaryStore.getIsCommentaryFollowingVideo());

const scrollTo = () => {
  const startTime = commentaryStore.getCurrentCommentaryTime();
  const elementId = `c-ST-${startTime}`; // 이동할 요소의 ID 생성
  const element = document.getElementById(elementId); // 요소 선택

  if (element) {
    element.scrollIntoView({ behavior: 'smooth' }); // 부드러운 스크롤로 이동
  }
}
</script>

<style scoped>
.q-btn :deep(.q-icon) {
  margin-right: .3em;
  font-size: 1.2rem;
  margin-top: .125rem;
}

.mobile-btn {
  font-size: 12px;
  padding: 5px 10px;
}
</style>