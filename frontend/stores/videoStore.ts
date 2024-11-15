import {type Ref, ref} from "vue";

export interface VideoStore {
    videoPlayer: Ref<any>;
    videoId: Ref<string>;
    setPlayer: (player: any) => void;
    getPlayer: () => any;
    getVideoId: () => string;
    getCurrentVideoTime: () => number;
    setPlayerSize: (windowWidth: number) => void;
    setVideoId: (videoId: string) => void;
}

export const useVideoStore = defineStore('video', (): VideoStore => {
    const videoPlayer = ref<any> (null);
    const videoId = ref<string>('')

    const setPlayer = (player: any) => {
        videoPlayer.value = player;
    }

    const getPlayer = () => videoPlayer.value;

    const setVideoId = (vId: string) : void => {
        videoId.value = vId;
    }

    const getVideoId = (): string => videoId.value;

    const getCurrentVideoTime = () :number => {
        return videoPlayer.value.getCurrentTime();
    }

    const setPlayerSize = (windowWidth: number) => {
        const videoRatio: number = windowWidth > 768 ? 0.5 : 1;
        const width = windowWidth * videoRatio;
        const height = width * (9 / 16);
        videoPlayer.value.setSize(width, height);
    }

    return {
        videoPlayer,
        videoId,
        getVideoId,
        setPlayer,
        setVideoId,
        getPlayer,
        getCurrentVideoTime,
        setPlayerSize
    }
})