import {useCommentaryStore} from "~/stores/commentaryStore";
import {useVideoStore} from "~/stores/videoStore";

export const useAutoDisplayCommentary = () => {
    const commentaryStore = useCommentaryStore();
    const videoStore = useVideoStore();

    const startAutoDisplay = async (): Promise<void> => {
        videoStore.startFollowVideo();

        if(videoStore.intervalId) return;
        videoStore.intervalId = setInterval(async () => {
            const currentTime = videoStore.getPlayer().getCurrentTime();
            console.log(`영상 재생 시간: ${currentTime}`)
            if(!currentTime) return;
            if (!commentaryStore.getIsGenerateCommentariesCompleted()) return;
            if (!videoStore.followVideo) return;
            await commentaryStore.setCommentaryContent(currentTime);
        }, 1000);
    };

    const stopAutoDisplay = () => {
        videoStore.stopFollowVideo();
    };

    return { startAutoDisplay, stopAutoDisplay };
};

