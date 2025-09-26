<template>
  <div class="min-h-screen bg-gradient-valentine">
    <AdminLayout>
      <div class="space-y-6">
        
        <!-- Header -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <div class="text-center">
            <h1 class="text-3xl font-bold text-valentine-800 flex items-center justify-center gap-3 mb-4">
              Base de datos
            </h1>
            <p class="text-valentine-600">
              Vaciar la base de datos para crear un nuevo sorteo
            </p>
          </div>
        </div>

        <!-- Database Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-200 text-center">
            <div class="text-4xl mb-3">👤</div>
            <p class="text-3xl font-bold text-blue-600">{{ dbStats.totalUsers }}</p>
            <p class="text-blue-600 font-semibold">Total usuarios</p>
            <p class="text-sm text-blue-500 mt-1">Incluye administradores</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-green-200 text-center">
            <div class="text-4xl mb-3">🎪</div>
            <p class="text-3xl font-bold text-green-600">{{ dbStats.contestants }}</p>
            <p class="text-green-600 font-semibold">Concursantes</p>
            <p class="text-sm text-green-500 mt-1">Solo participantes</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-purple-200 text-center">
            <div class="text-4xl mb-3">✅</div>
            <p class="text-3xl font-bold text-purple-600">{{ dbStats.confirmed }}</p>
            <p class="text-purple-600 font-semibold">Confirmados</p>
            <p class="text-sm text-purple-500 mt-1">Listos para sorteo</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-yellow-200 text-center">
            <div class="text-4xl mb-3">🏆</div>
            <p class="text-3xl font-bold text-yellow-600">{{ dbStats.winners }}</p>
            <p class="text-yellow-600 font-semibold">Ganadores</p>
            <p class="text-sm text-yellow-500 mt-1">Han sido premiados</p>
          </div>
        </div>

        <!-- Clear Database Section -->
        <div class="bg-white rounded-xl shadow-lg p-8 border-2 border-valentine-200">
          <h2 class="text-2xl font-bold text-valentine-800 mb-6 flex items-center gap-2">
            Ejecutar limpieza
          </h2>

          <div class="bg-red-50 border-2 border-red-200 rounded-xl p-6">
            <div class="text-center mb-6">
              <div class="text-5xl mb-4">🗑️</div>
              <h3 class="text-xl font-bold text-red-800 mb-2">
                Eliminar todos los participantes
              </h3>
              <p class="text-red-600 text-sm">
                Esta acción eliminará todos los usuarios excepto los administradores
              </p>
            </div>

            <!-- Warning -->
            <div class="bg-red-100 border border-red-300 rounded-lg p-4 mb-6">
              <div class="flex items-start gap-3">
                <span class="text-2xl">⚠️</span>
                <div>
                  <p class="font-semibold text-red-800 mb-2">¡Acción irreversible!</p>
                  <ul class="text-sm text-red-700 space-y-1">
                    <li>• Se eliminarán TODOS los participantes</li>
                    <li>• Se conservará el usuario administrador</li>
                    <li>• Los datos no se podrán recuperar</li>
                    <li>• El sistema quedará listo para un nuevo sorteo</li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Clear Button -->
            <div class="text-center">
              <button
                @click="showModal = true"
                :disabled="clearing"
                class="bg-red-600 hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed text-white font-bold py-4 px-8 rounded-lg transition-colors flex items-center justify-center gap-2 mx-auto"
              >
                <span v-if="clearing" class="animate-spin">🔄</span>
                <span v-else></span>
                {{ clearing ? 'Limpiando...' : 'VACIAR' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Refresh Button -->
        <div class="text-center">
          <button
            @click="refreshStats"
            :disabled="loading"
            class="bg-valentine-500 hover:bg-valentine-600 disabled:bg-valentine-300 text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2 mx-auto"
          >
            <span class="animate-spin" v-if="loading">🔄</span>
            <span v-else>🔄</span>
            {{ loading ? 'Actualizando...' : 'Actualizar estadísticas' }}
          </button>
        </div>
      </div>
    </AdminLayout>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 border-4 border-red-300">
        <div class="text-center mb-6">
          <div class="text-6xl mb-4">⚠️</div>
          <h3 class="text-2xl font-bold text-red-800 mb-2">
            ¿Estás absolutamente seguro?
          </h3>
          <p class="text-red-600">
            Esta acción NO se puede deshacer. Se eliminarán todos los participantes permanentemente.
          </p>
        </div>

        <!-- Confirmation Steps -->
        <div class="space-y-4 mb-6">
          <div class="flex items-center gap-3">
            <input
              id="confirm1"
              v-model="confirmationSteps.step1"
              type="checkbox"
              class="w-4 h-4 text-red-600 border-red-300 rounded focus:ring-red-500"
            />
            <label for="confirm1" class="text-sm text-red-700">
              Entiendo que se eliminarán todos los participantes
            </label>
          </div>
          
          <div class="flex items-center gap-3">
            <input
              id="confirm2"
              v-model="confirmationSteps.step2"
              type="checkbox"
              class="w-4 h-4 text-red-600 border-red-300 rounded focus:ring-red-500"
            />
            <label for="confirm2" class="text-sm text-red-700">
              He notificado a los ganadores si es necesario
            </label>
          </div>
          
          <div class="flex items-center gap-3">
            <input
              id="confirm3"
              v-model="confirmationSteps.step3"
              type="checkbox"
              class="w-4 h-4 text-red-600 border-red-300 rounded focus:ring-red-500"
            />
            <label for="confirm3" class="text-sm text-red-700">
              Confirmo que quiero proceder con la limpieza
            </label>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="flex gap-4">
          <button
            @click="showModal = false"
            class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="confirmClearDatabase"
            :disabled="!canClearDatabase"
            class="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg transition-colors"
          >
            Sí, eliminar todo
          </button>
        </div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="showSuccessMessage" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 border-4 border-green-300">
        <div class="text-center">
          <div class="text-6xl mb-4">✅</div>
          <h3 class="text-2xl font-bold text-green-800 mb-2">
            ¡Base de datos limpiada!
          </h3>
          <p class="text-green-600 mb-6">
            {{ successMessage }}
          </p>
          <button
            @click="closeSuccessMessage"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  definePageMeta({
    layout     : false,
    middleware : 'admin-auth'
  })

  useHead({
    title: 'Base de Datos - Admin Panel',
  })

  const dbStats = ref({
    totalUsers  : 0,
    contestants : 0,
    confirmed   : 0,
    winners     : 0
  })

  const confirmationSteps = reactive({
    step1: false,
    step2: false,
    step3: false
  })

  const showModal          = ref(false)
  const clearing           = ref(false)
  const loading            = ref(false)
  const showSuccessMessage = ref(false)
  const successMessage     = ref('')

  const { $toast } = useNuxtApp()
  const config     = useRuntimeConfig()

  const canClearDatabase = computed(() => {
    return confirmationSteps.step1 && confirmationSteps.step2 && confirmationSteps.step3
  })

  const fetchDatabaseStats = async () => {
    try {
      loading.value = true
    
      const adminToken = useCookie('adminToken')  
      const data       = await $fetch(`${config.public.apiBaseUrl}/admin/all-users/`, {
        method  : 'GET',
        headers : {
          'Authorization': `Bearer ${adminToken.value}`
        }
      })

      if (data.success) {
        const users = data.users || []
        
        dbStats.value = {
          totalUsers  : users.length + 1,
          contestants : users.length,
          confirmed   : users.filter(user => user.status === 'CONFIRMADO').length,
          winners     : users.filter(user => user.status === 'GANADOR').length
        }
      } else {
        throw new Error(data.message || 'Error al cargar estadísticas')
      }

    } catch (error) {
      console.error('Error fetching database stats:', error)
      
      if (error.status === 401 || error.status === 403) {
        $toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        navigateTo('/admin/login')
      } else {
        $toast.error('Error al cargar las estadísticas')
      }
    } finally {
      loading.value = false
    }
  }

  const confirmClearDatabase = async () => {
    if (!canClearDatabase.value) {
      $toast.error('Por favor, confirma todos los pasos')
      return
    }

    clearing.value = true

    try {
      const adminToken = useCookie('adminToken')
      const data       = await $fetch(`${config.public.apiBaseUrl}/admin/clear-db/`, {
        method  : 'DELETE',
        headers : {
          'Authorization': `Bearer ${adminToken.value}`
        }
      })

      if (data.success) {
        successMessage.value     = `${data.deleted_count} usuarios eliminados exitosamente`
        showModal.value          = false
        showSuccessMessage.value = true
        
        confirmationSteps.step1 = false
        confirmationSteps.step2 = false
        confirmationSteps.step3 = false
        
        await fetchDatabaseStats()
        
      } else {
        throw new Error(data.message || 'Error al limpiar la base de datos')
      }

    } catch (error) {
      console.error('Error clearing database:', error)
      
      if (error.status === 401 || error.status === 403) {
        $toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        navigateTo('/admin/login')
      } else {
        $toast.error(error.data?.message || 'Error al limpiar la base de datos')
      }
      
    } finally {
      clearing.value = false
    }
  }

  const closeSuccessMessage = () => {
    showSuccessMessage.value = false
    navigateTo('/admin/users')
  }

  const refreshStats = async () => {
    await fetchDatabaseStats()
    $toast.success('Estadísticas actualizadas')
  }

  onMounted(() => {
    fetchDatabaseStats()
})
</script>