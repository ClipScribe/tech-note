import {marked, Renderer} from "marked";
import hljs from "highlight.js";
import DOMPurify from "dompurify";
import "highlight.js/styles/github-dark.css";

export const useCreateHtml = () => {
    const createHtmlFromCommentary = async (content: string): Promise<string> => {
        const renderer = new Renderer();
        renderer.code = highlightCode;
        const rawHtml = await marked(content, { renderer })
        const sanitizedHtml = DOMPurify.sanitize(rawHtml);
        return `<div class="c-CT-inner">${sanitizedHtml}</div>`;
    }

    const highlightCode = ({ text, lang } : { text: string, lang?: string }): string => {
        const language = lang && hljs.getLanguage(lang) ? lang : "plaintext";
        const highlightedCode = hljs.highlight(text, { language }).value;
        return `<pre><code class="hljs ${language}">${highlightedCode}</code></pre>`;
    }

    return {
        createHtmlFromCommentary
    }
}
