import {$fetch } from "ofetch";


export interface NoteStore {
    createNote: (videoId: string, userLevel: string) => Promise<void>
}

export const useNoteStore = defineStore('note', (): NoteStore => {
    const config = useRuntimeConfig();

    const createNote = async (videoId: string, userLevel: string): Promise<void> => {
        return $fetch<void>('/notes',{
            method: 'POST',
            baseURL: config.public.apiBaseUrl,
            body: {
                videoId,
                userLevel
            },
            onResponse: ({ request, response, options }) => {
                const statusCode = response.status;
                console.log(statusCode);
            }
        })
    }
    return {
        createNote
    }
});

