<template>
  <div ref="scrollableContent" class="s-Scroller q-pa-sm" style="overflow-y: auto">
    <CommentaryItem
        v-for="commentary in commentaries"
        :key="commentary.startTime"
        :commentary="commentary"
    />
  </div>
</template>

<script setup lang="ts">
import {useCommentaryStore} from "~/stores/commentaryStore";

const commentaryStore = useCommentaryStore();

const commentaries = computed(()=> commentaryStore.getCommentaries());
</script>

<style lang="scss" scoped>
.s-Scroller {
  min-height: calc(100vh - 200px);
  max-height: calc(100vh - 200px);
}

@media (max-width: 768px) {
  /* 모바일 스타일 */
  .s-Scroller {
    max-height: 65vh;
    min-height: 65vh;
  }
}
</style>