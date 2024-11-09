<template>
  <aside class="summary-container">
    <q-card class="no-shadow">
      <header class="fixed-header flex justify-end mb-2">
        <TogglePositionButton/>
      </header>
      <ScrollableContent/>
    </q-card>
  </aside>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
.summary-container {
  width: 450px;
  position: fixed;
  right:0;
  top: 90px;
  background-color: white;
}

.markdown-content h1 {
  font-size: 2rem;
}

.markdown-content h2 {
  font-size: 1.75rem;
}

.markdown-content h3 {
  font-size: 1.5rem;
}

.markdown-content p {
  font-size: 1rem;
}

.markdown-content code,
.markdown-content pre {
  font-size: 0.9rem;
}

.fixed-header {
  background-color: white;
  z-index: 10;
  padding: 3rem 0 1rem 0;
  border-bottom: 1px solid #dcd9d9;
}

/*  모바일 */
@media (max-width: 768px) {
  .summary-container {
    flex: 1;
    position: inherit;
    max-width: 100vw;
  }

  .fixed-header {
    margin: 0;
    padding: .5rem 0 .8rem 0;
  }

  .markdown-content h1 {
    font-size: 1.5rem;
  }

  .markdown-content h2 {
    font-size: 1.3rem;
  }

  .markdown-content h3 {
    font-size: 1.2rem;
  }

  .markdown-content p {
    font-size: 0.9rem;
  }

  .markdown-content code,
  .markdown-content pre {
    font-size: 0.8rem;
  }
}
</style>
