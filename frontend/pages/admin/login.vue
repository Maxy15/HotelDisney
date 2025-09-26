<template>
  <div class="min-h-screen flex flex-col bg-gradient-valentine">
    <Navbar />
    
    <main class="flex-1 flex items-center justify-center">
      <div class="container mx-auto px-4 py-8">
        <div class="max-w-md mx-auto">
          
          <!-- Admin Login Form -->
          <div class="bg-white rounded-2xl shadow-2xl p-8 border-4 border-valentine-200">
            
            <!-- Header -->
            <div class="text-center mb-8">
              <div class="text-6xl mb-4 animate-pulse-slow">🏰</div>
              <h1 class="text-3xl font-bold text-valentine-800 mb-2">Inicio de sesión</h1>
            </div>

            <!-- Admin Info -->
            <div class="bg-disney-50 border-2 border-disney-200 rounded-lg p-4 mb-6">
              <div class="flex items-center justify-center gap-2 mb-2">
                <span class="font-semibold text-disney-800">Administrador CTS</span>
              </div>
              <p class="text-sm text-disney-700 text-center">
                Acceso exclusivo para panel de administración
              </p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-6">
              
              <!-- Email -->
              <div>
                <label for="email" class="block text-sm font-semibold text-valentine-800 mb-2">
                  Correo electrónico
                </label>
                <div class="relative">
                  <input
                    id="email"
                    v-model="form.email"
                    type="email"
                    required
                    class="w-full px-4 py-3 pl-12 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                    :class="{ 'border-red-500': errors.email }"
                    placeholder="admin@cts.cl"
                  />
                  <div class="absolute left-3 top-3 text-valentine-400">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                    </svg>
                  </div>
                </div>
                <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
              </div>

              <!-- Password -->
              <div>
                <label for="password" class="block text-sm font-semibold text-valentine-800 mb-2">
                  Contraseña
                </label>
                <div class="relative">
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    class="w-full px-4 py-3 pl-12 pr-12 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                    :class="{ 'border-red-500': errors.password }"
                    placeholder="••••••••"
                  />
                  <div class="absolute left-3 top-3 text-valentine-400">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-3 text-valentine-400 hover:text-valentine-600 transition-colors"
                  >
                    <svg v-if="showPassword" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                :disabled="loading"
                class="w-full bg-gradient-magic text-white font-bold py-4 px-6 rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="loading" class="animate-spin">👑</span>
                <span v-else></span>
                {{ loading ? 'Iniciando sesión...' : 'Acceder al panel' }}
              </button>
            </form>

            <!-- Footer Info -->
            <div class="mt-8 text-center space-y-4">
              <div class="border-t border-valentine-100 pt-6">
                <p class="text-sm text-valentine-600 mb-4">
                  🛡️ Acceso seguro y cifrado
                </p>
              </div>
              
              <!-- Back to public site -->
              <div class="pt-4">
                <NuxtLink 
                  to="/"
                  class="text-valentine-600 hover:text-valentine-800 text-sm underline transition-colors"
                >
                  ← Volver al sorteo público
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
  definePageMeta({
    layout: false
  })

  useHead({
    title : 'Login Administrador - Sorteo San Valentín Disney',
    meta  : [
      { 
        name    : 'description', 
        content : 'Acceso al panel de administración del sorteo San Valentín Disney.' 
      }
    ]
  })

  const form = reactive({
    email    : '',
    password : ''
  })

  const errors = reactive({
    email    : '',
    password : ''
  })

  const loading      = ref(false)
  const showPassword = ref(false)
  const { $toast }   = useNuxtApp()
  const config       = useRuntimeConfig()

  const clearErrors = () => {
    errors.email    = ''
    errors.password = ''
  }

  onMounted(() => {
    const token = useCookie('adminToken')
    if (token.value) {
      navigateTo('/admin/users')
    }
  })

  const handleLogin = async () => {
    clearErrors()
    loading.value = true

    try {
      const data = await $fetch(`${config.public.apiBaseUrl}/admin/login/`, {
        method : 'POST',
        body   : form
      })

      if (data.success && data.token) {
        const adminToken = useCookie('adminToken', {
          maxAge: 60 * 60 * 24
        })
        adminToken.value = data.token

        const adminUser = useCookie('adminUser')
        adminUser.value = JSON.stringify(data.user)

        $toast.success('¡Bienvenido al panel de administración!')
        
        await navigateTo('/admin/users')
        
      } else {
        throw new Error(data.message || 'Error en el login')
      }

    } catch (error) {
      console.error('Login error:', error)
      
      if (error.data?.errors) {
        Object.keys(error.data.errors).forEach(field => {
          const fieldErrors = error.data.errors[field]
          if (Array.isArray(fieldErrors)) {
            errors[field] = fieldErrors.join(', ')
          } else if (typeof fieldErrors === 'string') {
            errors[field] = fieldErrors
          }
        })
      }
      
      $toast.error(error.data?.message || 'Credenciales inválidas')
      
    } finally {
      loading.value = false
    }
  }
</script>
