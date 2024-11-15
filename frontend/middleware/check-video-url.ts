import { useVideoStore } from '~/stores/videoStore';

export default defineNuxtRouteMiddleware((to, from) => {
    const videoStore = useVideoStore();

    if (videoStore.getVideoId() == '' && to.path === '/video') {
        return navigateTo('/');
    }
});