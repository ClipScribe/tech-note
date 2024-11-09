<template>
  <q-header
      elevated
      class="bg-indigo-2 text-dark row items-center justify-center app-header"
  >
    <q-toolbar>
      <q-toolbar-title>
          <img src="#" alt="로고" />
      </q-toolbar-title>
    </q-toolbar>
  </q-header>
</template>

<script setup lang="ts">

</script>

<style scoped>
.app-header {
  height: 90px;
}

@media (max-width: 767px) { /* 모바일 장치에 적용 */
  .app-header {
    height: 70px;
  }
}
</style>