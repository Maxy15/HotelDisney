export default defineNuxtConfig({
  typescript: { strict: false },
  devtools : { enabled: true },
  modules  : [
    '@nuxtjs/tailwindcss',
    '@vueuse/nuxt'
  ],
  css      : ['~/assets/css/main.css'],
  app      : {
    head: {
      title: 'Sorteo San Valentín Disney - CTS Turismo',
      meta: [
        { charset: 'utf-8' },
        { 
          name    : 'viewport', 
          content : 'width=device-width, initial-scale=1' 
        },
        { 
          hid     : 'description', 
          name    : 'description', 
          content : 'Participa en nuestro sorteo especial de San Valentín y gana 2 noches mágicas en Hotel Disney' 
        }
      ],
      link: [
        { 
          rel  : 'icon', 
          type : 'image/x-icon', 
          href : '/favicon.ico' 
        },
        {
          rel  : 'preconnect',
          href : 'https://fonts.googleapis.com'
        },
        {
          rel         : 'preconnect',
          href        : 'https://fonts.gstatic.com',
          crossorigin : 'anonymous'
        },
        {
          rel  : 'stylesheet',
          href : 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
        }
      ]
    }
  },
  runtimeConfig : {
    public: {
      apiBaseUrl  : process.env.API_BASE_URL || 'http://localhost:8000/api',
      frontendUrl : process.env.FRONTEND_URL || 'http://localhost:3000'
    }
  },
  plugins       : [
    '~/plugins/toast.client.ts'
  ]
})