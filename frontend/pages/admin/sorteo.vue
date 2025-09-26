<template>
  <div class="min-h-screen bg-gradient-valentine">
    <AdminLayout>
      <div class="space-y-6">
        
        <!-- Header -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <div class="text-center">
            <h1 class="text-4xl font-bold text-valentine-800 flex items-center justify-center gap-3 mb-4">
              <span class="text-5xl animate-sparkle">🎪</span>
              Sorteo San Valentín
              <span class="text-5xl animate-sparkle">🎪</span>
            </h1>
            <p class="text-xl text-valentine-600">
              ¡Momento mágico para elegir a los ganadores de las 2 noches en Hotel Disney!
            </p>
          </div>
        </div>

        <!-- Eligible Participants Summary -->
        <div class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="text-center bg-valentine-50 rounded-lg p-6">
              <div class="text-4xl mb-3">👥</div>
              <p class="text-3xl font-bold text-valentine-800">{{ eligibleCount }}</p>
              <p class="text-valentine-600 font-semibold">Participantes elegibles</p>
              <p class="text-sm text-valentine-500 mt-2">
                Usuarios con estado CONFIRMADO
              </p>
            </div>
            
            <div class="text-center bg-disney-50 rounded-lg p-6">
              <div class="text-4xl mb-3">🏆</div>
              <p class="text-3xl font-bold text-disney-800">{{ winnersCount }}</p>
              <p class="text-disney-600 font-semibold">Ganadores anteriores</p>
              <p class="text-sm text-disney-500 mt-2">
                En sorteos previos
              </p>
            </div>
            
            <div class="text-center bg-rose-50 rounded-lg p-6">
              <div class="text-4xl mb-3">🎯</div>
              <p class="text-3xl font-bold text-rose-800">{{ eligibleCount > 0 ? '¡Sí!' : 'No' }}</p>
              <p class="text-rose-600 font-semibold">¿Listo para sortear?</p>
              <p class="text-sm text-rose-500 mt-2">
                {{ eligibleCount > 0 ? 'Hay participantes disponibles' : 'No hay participantes elegibles' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Draw Section -->
        <div class="bg-white rounded-xl shadow-lg p-8 border-2 border-valentine-200">
          
          <!-- No Eligible Participants -->
          <div v-if="eligibleCount === 0" class="text-center py-12">
            <div class="text-6xl mb-6">😔</div>
            <h3 class="text-2xl font-bold text-valentine-800 mb-4">
              No hay participantes elegibles
            </h3>
            <p class="text-valentine-600 mb-6">
              Para poder realizar un sorteo, necesitas al menos un participante con estado CONFIRMADO
            </p>
            <NuxtLink 
              to="/admin/users"
              class="inline-flex items-center gap-2 bg-valentine-500 hover:bg-valentine-600 text-white px-6 py-3 rounded-lg transition-colors"
            >
              Ver participantes
            </NuxtLink>
          </div>

          <!-- Draw Available -->
          <div v-else class="text-center">
            
            <!-- Pre-draw state -->
            <div v-if="!winner && !drawInProgress">
              <div class="mb-8">
                <div class="text-8xl mb-6 animate-float">🎁</div>
                <h2 class="text-3xl font-bold text-valentine-800 mb-4">
                  ¡Es hora del gran sorteo!
                </h2>
                <p class="text-lg text-valentine-600 mb-6">
                  {{ eligibleCount }} {{ eligibleCount === 1 ? 'participante está listo' : 'participantes están listos' }} para competir por el premio mágico
                </p>
                
                <!-- Prize Display -->
                <div class="bg-gradient-disney rounded-xl p-6 mb-8 max-w-md mx-auto">
                  <div class="text-5xl mb-3">🏰</div>
                  <h3 class="text-xl font-bold text-disney-800 mb-2">Premio Especial</h3>
                  <p class="text-disney-700 font-semibold">
                    2 noches con todo pagado en Hotel Disney
                  </p>
                  <p class="text-sm text-disney-600 mt-2">
                    Una experiencia mágica e inolvidable ✨
                  </p>
                </div>
              </div>

              <!-- Launch Button -->
              <button
                @click="startDraw"
                class="bg-gradient-magic text-white font-bold py-6 px-12 rounded-xl text-2xl hover:shadow-2xl transform hover:scale-105 transition-all duration-500 flex items-center justify-center gap-4 mx-auto"
              >
                <span class="text-4xl animate-bounce-slow">🚀</span>
                ¡LANZAR SORTEO!
                <span class="text-4xl animate-bounce-slow">🎪</span>
              </button>
            </div>

            <!-- Drawing in progress -->
            <div v-else-if="drawInProgress" class="py-12">
              <div class="text-8xl animate-spin mb-6">🎰</div>
              <h2 class="text-3xl font-bold text-valentine-800 mb-4">
                ¡Seleccionando ganador...!
              </h2>
              <p class="text-lg text-valentine-600 mb-6">
                La magia de Disney está decidiendo...
              </p>
              <div class="flex justify-center items-center gap-2">
                <div class="w-3 h-3 bg-valentine-500 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                <div class="w-3 h-3 bg-disney-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-3 h-3 bg-rose-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
              </div>
            </div>

            <!-- Winner announced -->
            <div v-else-if="winner" class="py-8">
              
              <!-- Celebration -->
              <div class="mb-8">
                <div class="text-8xl animate-bounce-slow mb-4">🎊</div>
                <h2 class="text-4xl font-bold text-valentine-800 mb-6">
                  ¡TENEMOS GANADORES!
                </h2>
              </div>

              <!-- Winner Card -->
              <div class="max-w-2xl mx-auto bg-gradient-magic text-white rounded-2xl p-8 mb-8 shadow-2xl">
                <div class="text-6xl mb-6">👑</div>
                
                <h3 class="text-3xl font-bold mb-4">
                  ¡Felicidades {{ winner.nombre }}!
                </h3>
                
                <div class="bg-white/20 rounded-xl p-6 mb-6">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                    <div>
                      <p class="font-semibold text-lg mb-2">Ganador Principal:</p>
                      <p class="text-xl">{{ winner.nombre }}</p>
                      <p class="text-lg opacity-90">{{ winner.email }}</p>
                    </div>
                    <div>
                      <p class="font-semibold text-lg mb-2">Su Pareja:</p>
                      <p class="text-xl">{{ winner.nombre_pareja }}</p>
                      <p class="text-lg opacity-90">{{ winner.telefono }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-white/20 rounded-xl p-4">
                  <p class="text-lg font-semibold mb-2">¡Han ganado:</p>
                  <p class="text-2xl">🏰 2 noches en Hotel Disney 🏰</p>
                  <p class="text-lg opacity-90 mt-2">
                    Con todo pagado para una experiencia mágica
                  </p>
                </div>
              </div>

              <!-- Winner Actions -->
              <div class="space-y-4">
                <div class="bg-green-50 border-2 border-green-200 rounded-xl p-4">
                  <div class="flex items-center justify-center gap-2 mb-2">
                    <span class="text-2xl">📧</span>
                    <p class="font-semibold text-green-800">Email de felicitación enviado</p>
                  </div>
                  <p class="text-green-600 text-sm">
                    Se ha enviado automáticamente un email con los detalles del premio
                  </p>
                </div>

                <div class="flex gap-4 justify-center">
                  <button
                    @click="newDraw"
                    class="bg-valentine-500 hover:bg-valentine-600 text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
                  >
                    <span>🎲</span>
                    Nuevo sorteo
                  </button>
                  
                  <NuxtLink 
                    to="/admin/users"
                    class="bg-disney-500 hover:bg-disney-600 text-white px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
                  >
                    <span>👥</span>
                    Ver todos los usuarios
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Winners -->
        <div v-if="recentWinners.length > 0" class="bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200">
          <h3 class="text-2xl font-bold text-valentine-800 mb-6 flex items-center gap-2">
            <span class="text-3xl">🏆</span>
            Ganadores Recientes
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="recentWinner in recentWinners" 
              :key="recentWinner.id_usuario"
              class="bg-purple-50 border-2 border-purple-200 rounded-lg p-4"
            >
              <div class="text-center mb-3">
                <div class="text-3xl mb-2">👑</div>
                <p class="font-bold text-purple-800">{{ recentWinner.nombre }}</p>
                <p class="text-sm text-purple-600">{{ recentWinner.email }}</p>
              </div>
              
              <div class="space-y-2 text-sm">
                <p class="text-purple-700">
                  <strong>Pareja:</strong> {{ recentWinner.nombre_pareja }}
                </p>
                <p class="text-purple-600">
                  <strong>Ganó el:</strong> {{ formatDate(recentWinner.last_time_winner) }}
                </p>
              </div>
            </div>
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
    title: 'Sorteo - Admin Panel',
  })

  const eligibleCount  = ref(0)
  const winnersCount   = ref(0)
  const recentWinners  = ref([])
  const winner         = ref(null)
  const drawInProgress = ref(false)

  const { $toast } = useNuxtApp()
  const config     = useRuntimeConfig()

  const fetchStats = async () => {
    try {
      const adminToken = useCookie('adminToken')
      const data       = await $fetch(`${config.public.apiBaseUrl}/admin/all-users/`, {
        method  : 'GET',
        headers : {
          'Authorization': `Bearer ${adminToken.value}`
        }
      })

      if (data.success) {
        const users         = data.users || []
        eligibleCount.value = users.filter(user => user.can_participate).length
        winnersCount.value  = users.filter(user => user.status === 'GANADOR').length
        
        recentWinners.value = users
          .filter(user => user.status === 'GANADOR' && user.last_time_winner)
          .sort((a, b) => new Date(b.last_time_winner) - new Date(a.last_time_winner))
          .slice(0, 6)
          
      } else {
        throw new Error(data.message || 'Error al cargar estadísticas')
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
      
      if (error.status === 401 || error.status === 403) {
        $toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        navigateTo('/admin/login')
      } else {
        $toast.error('Error al cargar las estadísticas')
      }
    }
  }

  const startDraw = async () => {
    if (eligibleCount.value === 0) {
      $toast.error('No hay participantes elegibles para el sorteo')
      return
    }

    drawInProgress.value = true
    winner.value         = null

    try {
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const adminToken = useCookie('adminToken')
      const data       = await $fetch(`${config.public.apiBaseUrl}/admin/winner/`, {
        method  : 'GET',
        headers : {
          'Authorization': `Bearer ${adminToken.value}`
        }
      })

      if (data.success) {
        winner.value = data.winner
        $toast.success(`¡${data.winner.nombre} ha ganado el sorteo!`)
        
        await fetchStats()
      } else {
        throw new Error(data.message || 'Error al realizar el sorteo')
      }
    } catch (error) {
      console.error('Error in draw:', error)
      
      if (error.status === 401 || error.status === 403) {
        $toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
        navigateTo('/admin/login')
      } else {
        $toast.error(error.data?.message || 'Error al realizar el sorteo')
      }
      
    } finally {
      drawInProgress.value = false
    }
  }

  const newDraw = () => {
    winner.value = null
    fetchStats()
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-CL', {
      day    : '2-digit',
      month  : '2-digit',
      year   : 'numeric',
      hour   : '2-digit',
      minute : '2-digit'
    })
  }

  onMounted(() => {
    fetchStats()
  })
</script>