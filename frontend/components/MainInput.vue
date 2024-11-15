<template>
  <section class="column items-center full-width">
    <div class="q-gutter-md text-center q-pr-none full-width" style="max-width: 900px;">
      <q-input
          filled
          append
          v-model.trim="youtubeUrl"
          label="YouTube 영상 링크를 입력하세요"
          class="q-mt-md q-pr-none"
          color="black"
          :rules="[validateYoutubeUrl]"
          :error-message="'영상 링크가 올바르지 않아요'"
          no-error-icon
          bg-color="white"
      >
        <template v-slot:append>
          <q-btn class="bg-black text-white full-height " flat icon="arrow_forward" @click="handleSubmit"/>
        </template>
      </q-input>
    </div>
    <div class="q-mt-md text-center q-mt-md">
      <div class="q-gutter-sm flex justify-center">
        <q-checkbox
            v-for="level in knowledgeLevels"
            :key="level.value"
            v-model="checkboxStates[level.value]"
            :label="level.label"
            @update:model-value="selectCheckbox(level.value)"
            color="black"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useVideoStore} from "~/stores/videoStore";
import {useNoteStore} from "~/stores/noteStore";
import {KnowledgeLevel} from "~/types/commentary";
import {navigateTo} from "#app";

const youtubeUrl = ref("");
const videoStore = useVideoStore();
const noteStore = useNoteStore();

const selectedLevel = ref<KnowledgeLevel>(KnowledgeLevel.BEGINNER);
const checkboxStates = reactive({
  [KnowledgeLevel.BEGINNER]: true,
  [KnowledgeLevel.INTERMEDIATE]: false,
  [KnowledgeLevel.EXPERT]: false
});

const knowledgeLevels = [
  {value: KnowledgeLevel.BEGINNER, label: "전혀 몰라요"},
  {value: KnowledgeLevel.INTERMEDIATE, label: "어느정도 지식이 있어요"},
  {value: KnowledgeLevel.EXPERT, label: "전문가에요"}
];

const selectCheckbox = (checkedLevel: KnowledgeLevel): void => {
  selectedLevel.value = checkedLevel;
  for (let i = 0; i < knowledgeLevels.length; i++) {
    checkboxStates[knowledgeLevels[i].value] = knowledgeLevels[i].value == checkedLevel;
  }
};

const validateYoutubeUrl = (val: string): boolean => {
  const pattern = /^https:\/\/www\.youtube\.com\/watch\?v=/;
  return pattern.test(val);
};

const extractVideoId = (url: string): string | null => {
  const urlParams = new URLSearchParams(url.split('?')[1]);
  return urlParams.get('v');
}

const handleSubmit = async (): Promise<void> => {
  if (selectedLevel.value && validateYoutubeUrl(youtubeUrl.value)) {
    const trimmedUrl = youtubeUrl.value.split("&")[0];
    const videoId = extractVideoId(trimmedUrl) as string;
    const userLevel = selectedLevel.value;
    await noteStore.createNote(videoId, userLevel);
    videoStore.setVideoId(videoId);
    navigateTo("/video");
  }
};
</script>