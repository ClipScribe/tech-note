import {useCreateHtml} from '~/composables/useCreateHtml'
import type {Ref} from "vue";
import type {Commentary} from "~/types/commentary";
import {useVideoStore} from "~/stores/videoStore";

interface CommentaryStore {
    isGenerateCommentariesCompleted: Ref<boolean>;
    isCommentaryFollowingVideo: Ref<boolean>;
    commentaries: Ref<Commentary[]>
    getIsGenerateCommentariesCompleted: () => boolean;
    getIsCommentaryFollowingVideo: () => boolean;
    getCommentaries: () => Commentary[];
    updateCommentaries: (currentTime: number) => void;
    setIsCommentaryFollowingVideo: (followingVideo: boolean) => void;
    setScrollableCommentaries: () => void;
    getCurrentCommentaryTime: () => number;
    addCommentary: (startTime: number, content: string) => Promise<void>
}

export const useCommentaryStore = defineStore('commentary', (): CommentaryStore => {
    const AUTO_DISPLAY_COMMENTARY_SIZE = 1;

    const {createHtmlFromCommentary} = useCreateHtml();
    const isGenerateCommentariesCompleted: Ref<boolean> = ref<boolean>(false);
    const isCommentaryFollowingVideo: Ref<boolean> = ref<boolean>(false);
    const commentaries: Ref<Commentary[]> = ref<Commentary[]>([]);
    const totalCommentaries: Commentary[] = [];

    const addCommentary = async (startTime: number, content: string):Promise<void> => {
        const htmlContent = await createHtmlFromCommentary(content);
        const commentary = createCommentary(startTime, htmlContent);
        totalCommentaries.push(commentary);
        commentaries.value.push(commentary);
    }

    const createCommentary = (startTime:number, htmlContent: string) : Commentary => {
        return {
            startTime,
            htmlContent
        }
    }

    const setScrollableCommentaries = () => {
        if(commentaries.value.length == AUTO_DISPLAY_COMMENTARY_SIZE) {
            commentaries.value = [];
            commentaries.value = totalCommentaries;
        }
    }

    const updateCommentaries = (currentTime: number): void => {
        const startIndex = getTargetCommentaryIndex(currentTime);
        const commentary: Commentary = totalCommentaries[startIndex];
        commentaries.value = [commentary]
    }

    const getTargetCommentaryIndex = (currentTime: number): number => {
        let start: number = 0;
        let end: number = totalCommentaries.length - 1;
        let index: number = -1;
        while (start <= end) {
            const mid = (start + end) >> 1;
            if (totalCommentaries[mid].startTime <= currentTime) {
                index = mid;
                start = mid + 1
            } else {
                end = mid - 1;
            }
        }
        return index;
    }

    const setIsCommentaryFollowingVideo = (isFollowing: boolean) => {
        isCommentaryFollowingVideo.value = isFollowing;
    }

    const getIsCommentaryFollowingVideo = () => isCommentaryFollowingVideo.value;

    const getIsGenerateCommentariesCompleted = () => isGenerateCommentariesCompleted.value;

    const getCommentaries = () => commentaries.value;

    const getCurrentCommentaryTime = () : number=> {
        const videoStore = useVideoStore();
        const currentTime = videoStore.getCurrentVideoTime();
        const targetCommentaryIndex = getTargetCommentaryIndex(currentTime);
        return totalCommentaries[targetCommentaryIndex].startTime
    }

    return {
        isCommentaryFollowingVideo,
        isGenerateCommentariesCompleted,
        commentaries,
        addCommentary,
        getIsCommentaryFollowingVideo,
        getIsGenerateCommentariesCompleted,
        getCommentaries,
        updateCommentaries,
        setIsCommentaryFollowingVideo,
        setScrollableCommentaries,
        getCurrentCommentaryTime
    };
})