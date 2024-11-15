import {navigateTo, useNuxtApp} from "#app";

export const useTabSync = () => {
    const syncTabs = () => {
        if(import.meta.browser) {
            window.addEventListener('storage', () => {
                if (localStorage.getItem('videoInProgress') === 'true') {
                    navigateTo('/');
                }
            })
        }
    }

    return {
        syncTabs
    }
}
