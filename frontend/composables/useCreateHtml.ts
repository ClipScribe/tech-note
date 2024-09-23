import type {Commentary} from "~/types/CommentaryStore";
import {marked, Renderer} from "marked";
import hljs from "highlight.js";
import DOMPurify from "dompurify";
import "highlight.js/styles/github-dark.css";

export const useCreateHtml = () => {
    const createHtmlFromCommentary = async (commentary: Commentary): Promise<string> => {
        const renderer = new Renderer();
        renderer.code = ({ text, lang }: { text: string; lang?: string }): string => {
            const language = lang && hljs.getLanguage(lang) ? lang : "plaintext";
            const highlightedCode = hljs.highlight(text, { language }).value;
            return `<pre><code class="hljs ${language}">${highlightedCode}</code></pre>`;
        };

        const rawHtml = await marked(commentary.content, { renderer })
        const sanitizedHtml = DOMPurify.sanitize(rawHtml);
        console.log(commentary.startTime);
        const videoTime = formatTime(commentary.startTime);
        return `<div id="content-${commentary.startTime}" class="content-section q-shadow-xs"><div class="time-Badge-root"><span class="time-Badge-inner">${videoTime}</span></div>${sanitizedHtml}</div>`;
    }

    const createHtmlFromCommentaries = async (commentaries: Commentary[]): Promise<string> => {
        const htmlArray = await Promise.all(commentaries.map(createHtmlFromCommentary));
        return htmlArray.join("");
    }

    const formatTime = (floatSeconds: number): string => {
        const totalSeconds = Math.floor(floatSeconds); // 정수 초로 변환
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        if (hours > 0) {
            return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        } else {
            return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }
    }

    return {
        createHtmlFromCommentaries,
        createHtmlFromCommentary
    }
}
