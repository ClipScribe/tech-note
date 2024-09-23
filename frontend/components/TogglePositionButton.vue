<template>
    <q-btn
        unelevated
        @click="startFollowVideo"
        label="재생위치로 이동"
        icon="adjust"
        class="q-mr-sm q-pa-x-sm q-pa-y-xs bg-grey-3 text-grey-9 border q-border-grey-3 text-bold no-ripple icon-spacing"
        :disable="followVideo"
    />
</template>

<script setup lang="ts">
import { useVideoStore } from "~/stores/videoStore";
import { useCommentaryStore } from "~/stores/commentaryStore"
import {useAutoDisplayCommentary} from "~/composables/useAutoDisplayCommentary";
import {computed} from "vue";


const videoStore = useVideoStore();
const commentaryStore = useCommentaryStore();
const followVideo = computed(() => videoStore.followVideo);

const { startAutoDisplay } = useAutoDisplayCommentary();

const startFollowVideo = () => {
  commentaryStore.clearCommentaryContent();
  startAutoDisplay();
};


</script>

<style scoped>
.q-btn>>>.q-icon {
  margin-right: .3em;
  font-size: 1.2rem;
  margin-top: .125rem;
}
</style>