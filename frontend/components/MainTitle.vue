<template>
  <div
      class="text-center text-bold q-mb-xl"
      :class="{
        'text-h4': $q.screen.lt.sm,
        'text-h2': $q.screen.gt.xs
      }"
  >
    서비스 설명 ~
  </div>
</template>