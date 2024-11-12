<template>
  <q-header
      bordered
      class="bg-white text-dark row items-center justify-center app-header shadow-none q-border"
  >
    <q-toolbar>
      <q-toolbar-title>
        <img src="#" alt="로고"/>
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

@media (max-width: 767px) {
  .app-header {
    height: 70px;
  }
}
</style>