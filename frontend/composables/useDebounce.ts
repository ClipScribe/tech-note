export const useDebounce = () => {
    const debounce = <T extends (...args: any[]) => void>(func: T, wait: number) => {
        let timeout: ReturnType<typeof setTimeout> | null;

        return (...args: Parameters<T>): void => {
            if (timeout) {
                clearTimeout(timeout);
            }
            timeout = setTimeout(() => {
                func(...args);
            }, wait);
        };
    };

    return {
        debounce
    }
}
