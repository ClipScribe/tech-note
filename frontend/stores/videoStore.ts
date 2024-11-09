import {type Ref, ref} from "vue";
import type {ReturnType} from "birpc";

export interface VideoStore {
    videoPlayer: Ref<any>;
    videoURL: Ref<string | undefined>; // 비디오 URL
    setVideoURL: (url: string) => void; // 비디오 URL 설정 메서드
    getVideoURL: () => string; // 비디오 URL 반환 메서드
    setPlayer: (player: any) => void;
    getPlayer: () => any;
    getCurrentVideoTime: () => number;
}

export const useVideoStore = defineStore('video', (): VideoStore => {
    const videoPlayer = ref<any> (null);
    const videoURL = ref<string>();
    const currentVideoTime = ref<number>(0);

    const setPlayer = (player: any) => {
        videoPlayer.value = player;
    }

    const getPlayer = () => videoPlayer.value;

    const setVideoURL = (url: string) : void => {
        videoURL.value = url;
    }
    const getVideoURL = (): string => videoURL.value as string

    const getCurrentVideoTime = () :number => {
        return videoPlayer.value.getCurrentTime();
    }

    return {
        videoPlayer,
        videoURL,
        setVideoURL,
        getVideoURL,
        setPlayer,
        getPlayer,
        getCurrentVideoTime,
    }
})