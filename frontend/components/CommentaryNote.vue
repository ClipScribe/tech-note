<template>
  <aside class="commentary-container bl">
    <q-card class="no-shadow">
      <commentary-toolbar/>
      <scrollable-content/>
    </q-card>
  </aside>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
.commentary-container {
  flex:1;
  background-color: white;
  border-left: 1px solid #dddddd;
}

/*  모바일 */
@media (max-width: 768px) {
  .commentary-container {
    flex: 1;
    position: inherit;
    max-width: 100vw;
  }
}
</style>
