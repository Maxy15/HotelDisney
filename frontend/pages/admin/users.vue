<template>
  <div class="min-h-screen bg-gradient-valentine">
    <AdminLayout>
      <div class="space-y-6">
        
        <!-- Header -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <div class="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 class="text-3xl font-bold text-valentine-800 flex items-center gap-3">
                Lista de usuarios
              </h1>
            </div>
            
            <div class="flex items-center gap-4">
              <div class="bg-valentine-50 px-4 py-2 rounded-lg">
                <p class="text-sm text-valentine-700">
                  <span class="font-semibold">Total:</span> {{ totalUsers }}
                </p>
              </div>
              <button
                @click="refreshUsers"
                :disabled="loading"
                class="bg-valentine-500 hover:bg-valentine-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
              >
                <span class="animate-spin" v-if="loading">🔄</span>
                <span v-else>🔄</span>
                Actualizar
              </button>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- Search -->
            <div>
              <label class="block text-sm font-semibold text-valentine-800 mb-2">
                Buscar participante
              </label>
              <input
                v-model="filters.search"
                @input="applyFilters"
                type="text"
                placeholder="Nombre, email o pareja..."
                class="w-full px-4 py-2 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500"
              />
            </div>

            <!-- Status Filter -->
            <div>
              <label class="block text-sm font-semibold text-valentine-800 mb-2">
                Estado
              </label>
              <select
                v-model="filters.status"
                @change="applyFilters"
                class="w-full px-4 py-2 border-2 border-valentine-200 rounded-lg focus:outline-none focus:border-valentine-500"
              >
                <option value="">Todos los estados</option>
                <option value="REGISTRADO">Registrado</option>
                <option value="CONFIRMADO">Confirmado</option>
                <option value="GANADOR">Ganador</option>
              </select>
            </div>

            <!-- Clear Filters -->
            <div class="flex items-end">
              <button
                @click="clearFilters"
                class="w-full border-2 border-valentine-300 text-valentine-600 hover:bg-valentine-50 px-4 py-2 rounded-lg transition-colors"
              >
                Limpiar filtros
              </button>
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden border-2 border-valentine-200">
          
          <!-- Loading State -->
          <div v-if="loading" class="p-12 text-center">
            <div class="text-6xl animate-spin mb-4">🎪</div>
            <p class="text-valentine-700 text-lg">Cargando participantes...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="!filteredUsers.length" class="p-12 text-center">
            <div class="text-6xl mb-4">🔭</div>
            <h3 class="text-xl font-semibold text-valentine-800 mb-2">
              No se encontraron participantes
            </h3>
            <p class="text-valentine-600">
              {{ filters.search || filters.status ? 'Prueba con otros filtros' : 'Aún no hay usuarios registrados' }}
            </p>
          </div>

          <!-- Users Table -->
          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-valentine-50">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">ID</th>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">Participante</th>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">Pareja</th>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">Contacto</th>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">Estado</th>
                  <th class="px-6 py-4 text-left text-sm font-semibold text-valentine-800">Puede participar</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-valentine-100">
                <tr 
                  v-for="user in paginatedUsers" 
                  :key="user.id_usuario"
                  class="hover:bg-valentine-25 transition-colors"
                >
                  <td class="px-6 py-4 text-sm font-mono text-valentine-700">
                    #{{ user.id_usuario }}
                  </td>

                  <td class="px-6 py-4">
                    <div>
                      <p class="font-semibold text-valentine-800">{{ user.nombre }}</p>
                      <p class="text-sm text-valentine-600">{{ user.email }}</p>
                    </div>
                  </td>

                  <td class="px-6 py-4">
                    <p class="text-valentine-700">{{ user.nombre_pareja }}</p>
                  </td>

                  <td class="px-6 py-4">
                    <p class="text-sm text-valentine-600">{{ user.telefono }}</p>
                  </td>

                  <td class="px-6 py-4">
                    <span 
                      :class="{
                        'bg-yellow-100 text-yellow-800': user.status === 'REGISTRADO',
                        'bg-green-100 text-green-800': user.status === 'CONFIRMADO',
                        'bg-purple-100 text-purple-800': user.status === 'GANADOR'
                      }"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium gap-1"
                    >
                      <span v-if="user.status === 'REGISTRADO'">⏳</span>
                      <span v-else-if="user.status === 'CONFIRMADO'">✅</span>
                      <span v-else-if="user.status === 'GANADOR'">🏆</span>
                      {{ user.status }}
                    </span>
                  </td>

                  <td class="px-6 py-4 text-center">
                    <span 
                      :class="user.can_participate ? 'text-green-600' : 'text-red-600'"
                      class="text-2xl"
                    >
                      {{ user.can_participate ? '✅' : '❌' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="bg-valentine-50 px-6 py-4 border-t border-valentine-100">
            <div class="flex items-center justify-between">
              <p class="text-sm text-valentine-700">
                Mostrando {{ ((currentPage - 1) * itemsPerPage) + 1 }} - 
                {{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }} 
                de {{ filteredUsers.length }} participantes
              </p>
              
              <div class="flex items-center gap-2">
                <button
                  @click="currentPage--"
                  :disabled="currentPage === 1"
                  class="px-3 py-1 border border-valentine-300 text-valentine-600 rounded hover:bg-valentine-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  ← Anterior
                </button>
                
                <span class="px-3 py-1 bg-valentine-500 text-white rounded">
                  {{ currentPage }} / {{ totalPages }}
                </span>
                
                <button
                  @click="currentPage++"
                  :disabled="currentPage === totalPages"
                  class="px-3 py-1 border border-valentine-300 text-valentine-600 rounded hover:bg-valentine-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Siguiente →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200 text-center">
            <div class="text-3xl mb-2">📝</div>
            <p class="text-2xl font-bold text-yellow-600">{{ stats.registrados }}</p>
            <p class="text-sm text-valentine-600">Registrados</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200 text-center">
            <div class="text-3xl mb-2">✅</div>
            <p class="text-2xl font-bold text-green-600">{{ stats.confirmados }}</p>
            <p class="text-sm text-valentine-600">Confirmados</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200 text-center">
            <div class="text-3xl mb-2">🏆</div>
            <p class="text-2xl font-bold text-purple-600">{{ stats.ganadores }}</p>
            <p class="text-sm text-valentine-600">Ganadores</p>
          </div>
          
          <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200 text-center">
            <div class="text-3xl mb-2">🎯</div>
            <p class="text-2xl font-bold text-valentine-600">{{ stats.elegibles }}</p>
            <p class="text-sm text-valentine-600">Elegibles</p>
          </div>
        </div>
      </div>
    </AdminLayout>
  </div>
</template>

<script setup>
  definePageMeta({
    layout     : false,
    middleware : 'admin-auth'
  })

  useHead({
    title: 'Participantes - Admin Panel',
  })

  const users        = ref([])
  const loading      = ref(true)
  const currentPage  = ref(1)
  const itemsPerPage = 10

  const filters = reactive({
    search : '',
    status : ''
  })

  const { $toast } = useNuxtApp()
  const config     = useRuntimeConfig()

  const filteredUsers = computed(() => {
    let filtered = users.value

    if (filters.search) {
      const searchTerm = filters.search.toLowerCase()
      filtered = filtered.filter(user => 
        user.nombre.toLowerCase().includes(searchTerm) ||
        user.email.toLowerCase().includes(searchTerm) ||
        user.nombre_pareja.toLowerCase().includes(searchTerm)
      )
    }

    if (filters.status) {
      filtered = filtered.filter(user => user.status === filters.status)
    }

    return filtered
  })

  const totalUsers = computed(() => filteredUsers.value.length)
  const totalPages = computed(() => Math.ceil(totalUsers.value / itemsPerPage))

  const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end   = start + itemsPerPage
    return filteredUsers.value.slice(start, end)
  })

  const stats = computed(() => {
    return {
      registrados : users.value.filter(u => u.status === 'REGISTRADO').length,
      confirmados : users.value.filter(u => u.status === 'CONFIRMADO').length,
      ganadores   : users.value.filter(u => u.status === 'GANADOR').length,
      elegibles   : users.value.filter(u => u.can_participate).length,
    }
  })

  const fetchUsers = async () => {
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
        users.value = data.users || []
      } else {
        throw new Error(data.message || 'Error al cargar usuarios')
      }

    } catch (error) {
      console.error('Error fetching users:', error)
      
      if (error.status === 401 || error.status === 403) {
        $toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        navigateTo('/admin/login')
      } else {
        $toast.error('Error al cargar la lista de usuarios')
      }
    } finally {
      loading.value = false
    }
  }

  const refreshUsers = async () => {
    await fetchUsers()
    $toast.success('Lista actualizada correctamente')
  }

  const applyFilters = () => {
    currentPage.value = 1
  }

  const clearFilters = () => {
    filters.search    = ''
    filters.status    = ''
    currentPage.value = 1
  }

  onMounted(() => {
    fetchUsers()
  })
</script>

<style scoped>
  .valentine-25 {
    background-color: rgb(253 242 248 / 0.3);
  }
</style>