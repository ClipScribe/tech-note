<template>
  <q-header
      bordered
      class="bg-white text-dark row items-center justify-center app-header shadow-none q-border"
  >
    <div class="img-wrapper" @click="toHome">
      <img src="/logo.png"/>
    </div>

  </q-header>
</template>

<script setup lang="ts">
import {navigateTo} from "#app";

const toHome = () => {
  navigateTo("/")
}
</script>
<style scoped>
.app-header {
  height: 90px;
  display: flex;
  justify-content: flex-start;
}

.img-wrapper {
  position: relative;
  height: 100%;
  width: 260px;
}

.img-wrapper img {
  position: absolute;
  height: 15rem;
  top: -4.8rem;
  left: -15px;
  pointer-events: none;
}

@media (max-width: 767px) {
  .app-header {
    height: 70px;
  }

  .img-wrapper {
    height: 100%;
    width: 160px;
  }

  .img-wrapper img {
    position: absolute;
    height: 10rem;
    top: -3rem;
    pointer-events: none;
  }
}
</style>