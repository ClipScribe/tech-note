<template>
  <div>
    <q-btn
        unelevated
        label="노트 다운받기"
        icon="note_add"
        class="toggle-btn q-mr-sm q-pa-x-sm q-pa-y-xs bg-black-8 text-grey-9 border q-border-grey-3 text-bold no-ripple icon-spacing"
        :class="{'mobile-btn': isMobile}"
    />
  </div>
</template>

<script setup lang="ts">
import {useIsMobile} from "~/composables/useIsMobile";

const { isMobile } = useIsMobile();
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