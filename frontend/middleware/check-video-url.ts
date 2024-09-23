import { useVideoStore } from '~/stores/videoStore';

export default defineNuxtRouteMiddleware((to, from) => {
    const videoStore = useVideoStore();

    // videoURL이 없고, /video 경로로 접근하려는 경우
    if (!videoStore.getVideoURL() && to.path === '/video') {
        return navigateTo('/');
    }
});