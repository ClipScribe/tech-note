import {useCreateHtml} from '~/composables/useCreateHtml'
import type {Ref} from "vue";
import type {Commentary} from "~/types/commentary";
import {useVideoStore} from "~/stores/videoStore";
import {target} from "@vue/devtools-shared";

const MARKDOWN_TEXT = `
### Revisited: Dining Philosopher

![Untitled](data:image/jpeg;base64,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)

mutual exclusion 만족 - chopstick이라는 것은 mutual exclusion이 돼야 됨; chopstick 자원을 한 프로세스가 쓸 때 다른 프로세스는 사용할 수 없으므로 mutual exclusion이 만족됨

hold and wait 만족 - 젓가락 하나를 보유한 상태에서 다른 젓가락을 얻어야 밥을 먹을 수 있으므로 hold and wait 만족

no preemption 만족 - 한 번 wait 했으면 다 쓸 때까지 가지고 있다가 다 쓰고 나서 반납함; 젓가락을 가지고 있는 다른 프로세스의 젓가락을 뺏을 수 없음

circular wait 만족 - 삥 둘러가며 젓가락을 공유; 젓가락이라는 자원을 배고픈 프로세스들이 모두 얻으려고 함

위 예시는 네 가지 조건을 모두 만족하므로 deadlock에 빠질 가능성이 있음.
### JavaScript 코드 블록
\`\`\`javascript
// 간단한 JavaScript 코드 예시
const message = 'Hello, world!';
console.log(message);
\`\`\`

### Python 코드 블록
\`\`\`python
# 간단한 Python 코드 예시
def greet():
    return "Hello, Python!"

print(greet())
\`\`\`
`;

interface CommentaryStore {
    isGenerateCommentariesCompleted: Ref<boolean>;
    isCommentaryFollowingVideo: Ref<boolean>;
    commentaries: Ref<Commentary[]>
    getIsGenerateCommentariesCompleted: () => boolean;
    getIsCommentaryFollowingVideo: () => boolean;
    getCommentaries: () => Commentary[];
    generateCommentaries: () => Promise<void>;
    updateCommentaries: (currentTime: number) => void;
    setIsCommentaryFollowingVideo: (followingVideo: boolean) => void;
    setScrollableCommentaries: () => void;
    getCurrentCommentaryTime: () => number;
}

export const useCommentaryStore = defineStore('commentary', (): CommentaryStore => {
    const AUTO_DISPLAY_COMMENTARY_SIZE = 1;

    const {createHtmlFromCommentary} = useCreateHtml();
    const isGenerateCommentariesCompleted: Ref<boolean> = ref<boolean>(false);
    const isCommentaryFollowingVideo: Ref<boolean> = ref<boolean>(false);
    const commentaries: Ref<Commentary[]> = ref<Commentary[]>([]);
    const totalCommentaries: Commentary[] = [];
    // v-for 변경 해주기 위함
     /*
        SSE 로 해설을 받으면 totalCommentaries에 추가한다.
     */
    const addCommentary = async (startTime: number, content: string):Promise<void> => {
        const htmlContent = await createHtmlFromCommentary(startTime, content);
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

    /*
        임시 함수
     */
    const generateCommentaries = async () :Promise<void> => {
        // 데이터를 받아왔다 가정
        for (let i = 0; i <= 50; i += 1) {
            const startTime = i * 20;
            const content = `${i.toString()}번째 문맥 \n ${MARKDOWN_TEXT}`
            await addCommentary(startTime, content);
        }
        isGenerateCommentariesCompleted.value = true;
    };

    const setScrollableCommentaries = () => {
        if(commentaries.value.length == AUTO_DISPLAY_COMMENTARY_SIZE) {
            // Duplicate Key 해결
            commentaries.value = [];

            commentaries.value = totalCommentaries;
        }
    }

    // 재생위치로 이동
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
        getIsCommentaryFollowingVideo,
        generateCommentaries,
        getIsGenerateCommentariesCompleted,
        getCommentaries,
        updateCommentaries,
        setIsCommentaryFollowingVideo,
        setScrollableCommentaries,
        getCurrentCommentaryTime
    };
})