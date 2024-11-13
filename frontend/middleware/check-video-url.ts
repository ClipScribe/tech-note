import { useVideoStore } from '~/stores/videoStore';

export default defineNuxtRouteMiddleware((to, from) => {
    const videoStore = useVideoStore();

    if (!videoStore.getVideoURL() && to.path === '/note') {
        return navigateTo('/');
    }
});