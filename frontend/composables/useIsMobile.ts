import { computed } from 'vue';
import { useQuasar } from 'quasar';

export function useIsMobile() {
    const $q = useQuasar();
    const isMobile = computed(() => $q.screen.lt.sm);
    return { isMobile };
}