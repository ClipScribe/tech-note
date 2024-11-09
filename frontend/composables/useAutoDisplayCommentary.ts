import {useCommentaryStore} from "~/stores/commentaryStore";
import {useVideoStore} from "~/stores/videoStore";

interface UseAutoDisplayCommentary {
    startAutoDisplayCommentary: () => void
    stopAutoDisplayCommentary: () => void
}

export const useAutoDisplayCommentary = (): UseAutoDisplayCommentary => {
    const commentaryStore = useCommentaryStore();
    const videoStore = useVideoStore();
    const INTERVAL_DURATION_MS = 1000;

    const displayCommentary = (): void => {
        const currentTime = videoStore.getPlayer().getCurrentTime();
        console.log(`영상 재생 시간: ${currentTime}`);
        commentaryStore.updateCommentaries(currentTime);
    };

    const startAutoDisplayCommentary = (): void => {
        commentaryStore.setIsCommentaryFollowingVideo(true);
        const executeDisplay = ():void => {
            const isCommentaryFollowingVideo: boolean = commentaryStore.getIsCommentaryFollowingVideo();
            if (isCommentaryFollowingVideo) {
                displayCommentary();
                setTimeout(executeDisplay, INTERVAL_DURATION_MS);
            }
        }
        executeDisplay();
    };

    const stopAutoDisplayCommentary = () => {
        commentaryStore.setIsCommentaryFollowingVideo(false);
        commentaryStore.setScrollableCommentaries();
    };

    return {startAutoDisplayCommentary, stopAutoDisplayCommentary};
};

