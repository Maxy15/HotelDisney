<template>
  <div class="min-h-screen flex flex-col bg-gradient-valentine">
    <Navbar />
    
    <main class="flex-1">
      <div class="container mx-auto px-4 py-8">
        
        <!-- Loading State -->
        <div v-if="validatingToken" class="flex items-center justify-center min-h-[60vh]">
          <div class="bg-white rounded-2xl shadow-2xl p-8 text-center border-4 border-valentine-200">
            <div class="text-6xl animate-spin mb-4">🎪</div>
            <p class="text-valentine-700 text-lg">Validando tu enlace mágico...</p>
          </div>
        </div>

        <!-- Invalid Token -->
        <div v-else-if="tokenError" class="max-w-md mx-auto">
          <div class="bg-white rounded-2xl shadow-2xl p-8 text-center border-4 border-red-200">
            <div class="text-6xl mb-4">🔒</div>
            <h1 class="text-2xl font-bold text-red-800 mb-4">Enlace inválido o expirado</h1>
            <p class="text-red-600 mb-6">{{ tokenError }}</p>
            
            <div class="space-y-4">
              <button 
                @click="goToHome"
                class="w-full bg-valentine-500 hover:bg-valentine-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
              >
                Volver al inicio
              </button>
              <p class="text-sm text-gray-600">
                ¿Necesitas un nuevo enlace? 
                <a href="mailto:soporte@ctsturismo.cl" class="underline text-valentine-600">
                  Contáctanos aquí
                </a>
              </p>
            </div>
          </div>
        </div>

        <!-- Valid Token - Password Form -->
        <div v-else-if="!passwordCreated" class="max-w-md mx-auto">
          <div class="bg-white rounded-2xl shadow-2xl p-8 border-4 border-valentine-200">
            
            <!-- Success Animation -->
            <div class="text-center mb-8">
              <div class="text-6xl mb-4 animate-bounce-slow">✅</div>
              <h1 class="text-2xl font-bold text-valentine-800 mb-2">¡Verificación exitosa!</h1>
              <p class="text-valentine-600">Hola {{ userInfo?.nombre || 'participante' }} 👋</p>
            </div>

            <!-- User Info -->
            <div class="bg-valentine-50 rounded-lg p-4 mb-6">
              <p class="text-sm text-valentine-700">
                <strong>Email:</strong> {{ userInfo?.email }}
              </p>
            </div>

            <!-- Password Form -->
            <form @submit.prevent="handlePasswordSubmit" class="space-y-6">
              <div class="text-center mb-6">
                <h2 class="text-xl font-semibold text-valentine-800 mb-2">
                  Crea tu contraseña
                </h2>
                <p class="text-valentine-600 text-sm">
                  Una vez creada, ya estarás participando en el sorteo
                </p>
              </div>

              <!-- Password -->
              <div>
                <label for="password" class="block text-sm font-semibold text-valentine-800 mb-2">
                  Contraseña nueva
                </label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                  :class="{ 'border-red-500': errors.password }"
                  placeholder="Mínimo 6 caracteres"
                />
                <p v-if="errors.password" class="text-red-500 text-sm mt-1">{{ errors.password }}</p>
              </div>

              <!-- Confirm Password -->
              <div>
                <label for="confirm_password" class="block text-sm font-semibold text-valentine-800 mb-2">
                  Confirmar contraseña
                </label>
                <input
                  id="confirm_password"
                  v-model="form.confirm_password"
                  type="password"
                  required
                  minlength="6"
                  class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                  :class="{ 'border-red-500': errors.confirm_password }"
                  placeholder="Repite tu contraseña"
                />
                <p v-if="errors.confirm_password" class="text-red-500 text-sm mt-1">{{ errors.confirm_password }}</p>
              </div>

              <!-- Password Match Indicator -->
              <div v-if="form.password && form.confirm_password" class="text-sm">
                <p v-if="form.password === form.confirm_password" class="text-green-600 flex items-center gap-1">
                  ✅ Las contraseñas coinciden
                </p>
                <p v-else class="text-red-600 flex items-center gap-1">
                  ❌ Las contraseñas no coinciden
                </p>
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                :disabled="loading || !isFormValid"
                class="w-full bg-gradient-magic text-white font-bold py-4 px-6 rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="loading" class="animate-spin">🎪</span>
                <span v-else></span>
                {{ loading ? 'Creando cuenta...' : '¡Completar registro!' }}
              </button>
            </form>

            <!-- Success Message -->
            <div class="mt-6 bg-gradient-disney rounded-lg p-4 text-center">
              <div class="text-3xl mb-2">🏰</div>
              <p class="text-disney-800 font-semibold">
                Participa por
              </p>
              <p class="text-disney-700 text-lg mt-2">
                2 noches mágicas en Hotel Disney
              </p>
            </div>
          </div>
        </div>

        <!-- Password Created Successfully -->
        <div v-else class="max-w-2xl mx-auto">
          <div class="bg-white rounded-2xl shadow-2xl p-8 text-center border-4 border-green-200">
            <div class="text-6xl mb-6 animate-bounce-slow">🎉</div>
            <h1 class="text-3xl font-bold text-green-800 mb-4">
              ¡Cuenta activada exitosamente!
            </h1>
            <p class="text-lg text-green-700 mb-8">
              Ya estás participando en el sorteo por 2 noches mágicas en Hotel Disney
            </p>

            <!-- Disney Castle Polaroid -->
            <div class="max-w-md mx-auto mb-8">
              <div class="bg-white p-4 shadow-2xl transform rotate-2 hover:rotate-0 transition-transform duration-300">
                <img 
                  src="https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop&q=80" 
                  alt="Castillo Disney"
                  class="w-full h-64 object-cover rounded"
                />
                <p class="text-center mt-3 font-handwriting text-lg text-gray-700">
                  ¡Tu premio te espera! 🏰✨
                </p>
              </div>
            </div>

            <div class="space-y-4">
              <div class="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                <p class="text-green-800 font-semibold mb-2">
                  ¿Qué sigue?
                </p>
                <ul class="text-left text-green-700 space-y-2">
                  <li>✅ Tu cuenta está activa</li>
                  <li>✅ Estás participando en el sorteo</li>
                  <li>✅ Te notificaremos si resultas ganador</li>
                </ul>
              </div>

              <button
                @click="goToHome"
                class="w-full bg-valentine-500 hover:bg-valentine-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
              >
                Volver al inicio
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
  useHead({
    title : 'Verificación de cuenta - Sorteo San Valentín Disney',
    meta  : [
      { 
        name    : 'description', 
        content : 'Verifica tu cuenta y crea tu contraseña para completar tu participación en el sorteo.' 
      }
    ]
  })

  const route      = useRoute()
  const { $toast } = useNuxtApp()
  const config     = useRuntimeConfig()

  const validatingToken = ref(true)
  const tokenError      = ref('')
  const userInfo        = ref(null)
  const loading         = ref(false)
  const passwordCreated = ref(false)

  const form = reactive({
    password         : '',
    confirm_password : '',
    token            : ''
  })

  const errors = reactive({
    password         : '',
    confirm_password : ''
  })

  const isFormValid = computed(() => {
    return form.password.length >= 6 && 
          form.confirm_password.length >= 6 && 
          form.password === form.confirm_password
  })

  const clearErrors = () => {
    errors.password         = ''
    errors.confirm_password = ''
  }

  onMounted(async () => {
    const token = route.query.token
    
    if (!token) {
      tokenError.value      = 'Token de verificación no encontrado'
      validatingToken.value = false
      return
    }

    form.token = token

    try {
      // Encode the token for the URL
      const encodedToken = encodeURIComponent(token)
      const data         = await $fetch(`${config.public.apiBaseUrl}/users/token/?token=${encodedToken}`)

      if (data.success) {
        userInfo.value = data.user
        $toast.success('¡Token válido! Ahora crea tu contraseña')
      } else {
        throw new Error(data.message || 'Token inválido')
      }

    } catch (error) {
      console.error('Token validation error:', error)
      tokenError.value = error.data?.message || 'El enlace ha expirado o es inválido'
    } finally {
      validatingToken.value = false
    }
  })

  const handlePasswordSubmit = async () => {
    clearErrors()
    
    if (!isFormValid.value) {
      $toast.error('Por favor, verifica que las contraseñas coincidan')
      return
    }

    loading.value = true

    try {
      const data = await $fetch(`${config.public.apiBaseUrl}/users/set-password/`, {
        method: 'POST',
        body: {
          token: form.token,
          password: form.password,
          confirm_password: form.confirm_password
        }
      })

      if (data.success) {
        passwordCreated.value = true
        $toast.success(data.message)
      } else {
        throw new Error(data.message || 'Error al crear contraseña')
      }

    } catch (error) {
      console.error('Password creation error:', error)
      
      if (error.data?.errors) {
        Object.keys(error.data.errors).forEach(field => {
          const fieldErrors = error.data.errors[field]
          if (Array.isArray(fieldErrors)) {
            errors[field] = fieldErrors.join(', ')
          } else if (typeof fieldErrors === 'string') {
            errors[field] = fieldErrors
          } else {
            $toast.error(JSON.stringify(fieldErrors))
          }
        })
      } else {
        $toast.error(error.data?.message || 'Error al crear la contraseña')
      }
      
    } finally {
      loading.value = false
    }
  }

  const goToHome = () => {
    navigateTo('/')
  }
</script>

<style scoped>
  .font-handwriting {
    font-family: 'Brush Script MT', cursive;
  }
</style>