import {type Ref, ref} from "vue";
import type {ReturnType} from "birpc";

export interface VideoStore {
    videoPlayer: Ref<any>;
    videoURL: Ref<string | undefined>; // 비디오 URL
    followVideo: Ref<boolean>; // 비디오를 따르는지 여부
    intervalId: Ref<ReturnType<typeof setInterval> | null>; // setInterval의 ID
    setVideoURL: (url: string) => void; // 비디오 URL 설정 메서드
    getVideoURL: () => string; // 비디오 URL 반환 메서드
    startFollowVideo: () => void; // 비디오 따라가기 시작 메서드
    stopFollowVideo: () => void; // 자동 해설 표시 중지 메서드
    getFollowVideo: () => boolean; // 비디오 따라가기 여부 반환 메서드
    setPlayer: (player: any) => void;
    getPlayer: () => any;
}

export const useVideoStore = defineStore('video', (): VideoStore => {
    const videoPlayer = ref<any> (null);
    const videoURL = ref<string>();
    const followVideo = ref<boolean>(true);
    const intervalId = ref<ReturnType<typeof setInterval> | null>(null);

    const setPlayer = (player: any) => {
        videoPlayer.value = player;
    }

    const getPlayer = () => videoPlayer.value;

    const setVideoURL = (url: string) : void => {
        videoURL.value = url;
    }
    const getVideoURL = (): string => videoURL.value as string

    const startFollowVideo = () : void => {
        followVideo.value = true;
    }

    const stopFollowVideo = () => {
        followVideo.value = false;
    };

    const getFollowVideo = (): boolean => followVideo.value;
    return {
        videoPlayer,
        videoURL,
        followVideo,
        intervalId,
        setVideoURL,
        getVideoURL,
        startFollowVideo,
        getFollowVideo,
        stopFollowVideo,
        setPlayer,
        getPlayer
    }
})