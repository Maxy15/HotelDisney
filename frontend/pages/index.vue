<template>
  <div class="min-h-screen flex flex-col bg-gradient-valentine">
    <Navbar />
    
    <main class="flex-1">
      <div class="container mx-auto px-4 py-8">
        <div class="text-center mb-12">
          <h1 class="text-4xl md:text-6xl font-bold text-valentine-800 mb-4 animate-pulse-slow">
            Sorteo San Valentín 
          </h1>
          <div class="text-xl md:text-2xl text-valentine-700 mb-6">
            <p class="flex items-center justify-center gap-2">
              ¡Gana 2 noches mágicas en Hotel Disney!
            </p>
          </div>
          <div class="flex justify-center items-center gap-4 text-6xl animate-float">
            <span>🏰</span>
            <span>💖</span>
            <span>🎪</span>
          </div>
        </div>

        <!-- Registration Form -->
        <div class="max-w-md mx-auto bg-white rounded-2xl shadow-2xl p-8 border-4 border-valentine-200">
          <div class="text-center mb-6">
            <h2 class="text-2xl font-bold text-valentine-800">¡Regístrate aquí!</h2>
            <p class="text-valentine-600 mt-2">Completa tus datos para participar</p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Nombre -->
            <div>
              <label for="nombre" class="block text-sm font-semibold text-valentine-800 mb-2">
                Tu nombre completo
              </label>
              <input
                id="nombre"
                v-model="form.nombre"
                type="text"
                required
                class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                :class="{ 'border-red-500': errors.nombre }"
                placeholder="Ej: María González"
              />
              <p v-if="errors.nombre" class="text-red-500 text-sm mt-1">{{ errors.nombre }}</p>
            </div>

            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-semibold text-valentine-800 mb-2">
                Correo electrónico
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                :class="{ 'border-red-500': errors.email }"
                placeholder="tu-email@ejemplo.com"
              />
              <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
            </div>

            <!-- Teléfono -->
            <div>
              <label for="telefono" class="block text-sm font-semibold text-valentine-800 mb-2">
                Número de teléfono
              </label>
              <input
                id="telefono"
                v-model="form.telefono"
                type="tel"
                required
                class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                :class="{ 'border-red-500': errors.telefono }"
                placeholder="+56 9 1234 5678"
              />
              <p v-if="errors.telefono" class="text-red-500 text-sm mt-1">{{ errors.telefono }}</p>
            </div>

            <!-- Nombre de pareja -->
            <div>
              <label for="nombre_pareja" class="block text-sm font-semibold text-valentine-800 mb-2">
                Nombre de tu pareja
              </label>
              <input
                id="nombre_pareja"
                v-model="form.nombre_pareja"
                type="text"
                required
                class="w-full px-4 py-3 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500 focus:ring-2 focus:ring-valentine-200 transition-all"
                :class="{ 'border-red-500': errors.nombre_pareja }"
                placeholder="Ej: Juan Pérez"
              />
              <p v-if="errors.nombre_pareja" class="text-red-500 text-sm mt-1">{{ errors.nombre_pareja }}</p>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-gradient-magic text-white font-bold py-4 px-6 rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <span v-if="loading" class="animate-spin">🎪</span>
              <span v-else></span>
              {{ loading ? 'Registrando...' : '¡Participar en el sorteo!' }}
            </button>
          </form>

          <!-- Info Footer -->
          <div class="mt-8 text-center text-sm text-valentine-600">
            <p class="mb-2">🎁 Premio: 2 noches en Hotel Disney</p>
            <p class="mb-2">📧 Recibirás un email para confirmar tu participación</p>
            <p class="flex items-center justify-center gap-1">
              <span>🔒</span>
              Tus datos están seguros con nosotros
            </p>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
  useHead({
    title : 'Inscripción - Sorteo San Valentín Disney',
    meta  : [
      { 
        name    : 'description', 
        content : 'Inscríbete en nuestro sorteo especial de San Valentín y gana 2 noches mágicas en Hotel Disney con tu pareja.' 
      }
    ]
  })

  const form = reactive({
    nombre        : '',
    email         : '',
    telefono      : '',
    nombre_pareja : ''
  })

  const errors = reactive({
    nombre        : '',
    email         : '',
    telefono      :  '',
    nombre_pareja : ''
  })

  const loading    = ref(false)
  const { $toast } = useNuxtApp()
  const config     = useRuntimeConfig()

  const clearErrors = () => {
    errors.nombre        = ''
    errors.email         = ''
    errors.telefono      = ''
    errors.nombre_pareja = ''
  }

  const handleSubmit = async () => {
    clearErrors()
    loading.value = true
    
    try {
      const response = await $fetch(`${config.public.apiBaseUrl}/users/register/`, {
        method: 'POST',
        body: form
      })
      
      if (response.success) {
        $toast.success(response.message)
        await navigateTo('/registro-exitoso')
      } else {
        throw new Error(response.message || 'Error en el registro')
      }
      
    } catch (error) {
      console.error('Registration error:', error)
      
      if (error.data?.message) {
        $toast.error(error.data.message)
      }
      
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
      
    } finally {
      loading.value = false
    }
  }
</script>