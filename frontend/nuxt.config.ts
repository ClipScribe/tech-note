export default defineNuxtConfig({
    app: {
        head: {
            title: "정확한 영상해설 | TechNote"
        }
    },
    compatibilityDate: '2024-04-03',
    devtools: { enabled: true },
    modules: [
        'nuxt-quasar-ui',
        '@pinia/nuxt',
        '@nuxtjs/google-fonts',
    ],
    css: [
        '@/assets/global.css',
        '@/assets/styles/variables.scss'
    ],
    quasar: {
        cssAddon: true
    },
    googleFonts: {
        families: {
            'Noto+Sans': [400], // 필요한 스타일 추가
        }
    },
})
