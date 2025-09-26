<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-lg border-b-2 border-valentine-200">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          
          <!-- Logo -->
          <div class="flex items-center gap-4">
            <div class="text-3xl">🏰</div>
            <div>
              <h1 class="text-xl font-bold text-valentine-800">
                Panel del administrador
              </h1>
              <p class="text-sm text-valentine-600">
                Sorteo San Valentín Disney
              </p>
            </div>
          </div>

          <!-- Info & Logout -->
          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="font-semibold text-valentine-800">{{ adminUser?.nombre || 'Administrador CTS' }}</p>
              <p class="text-sm text-valentine-600">{{ adminUser?.email }}</p>
            </div>
            <button
              @click="logout"
              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="container mx-auto px-4 py-6">
      <div class="flex gap-6">
        
        <!-- Sidebar -->
        <aside class="w-64 bg-white rounded-xl shadow-lg p-6 border-2 border-valentine-200 h-fit">
          <nav class="space-y-2">
            
            <!-- Users -->
            <NuxtLink
              to="/admin/users"
              class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-valentine-700 hover:bg-valentine-50 hover:text-valentine-800"
              :class="{ 'bg-valentine-100 text-valentine-800 font-semibold': $route.path === '/admin/users' }"
            >
              <span class="text-xl">👥</span>
              <span>Ver usuarios</span>
            </NuxtLink>

            <!-- Draw -->
            <NuxtLink
              to="/admin/sorteo"
              class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-valentine-700 hover:bg-valentine-50 hover:text-valentine-800"
              :class="{ 'bg-valentine-100 text-valentine-800 font-semibold': $route.path === '/admin/sorteo' }"
            >
              <span class="text-xl">🎪</span>
              <span>Sorteo</span>
            </NuxtLink>

            <!-- Database -->
            <NuxtLink
              to="/admin/db"
              class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-valentine-700 hover:bg-valentine-50 hover:text-valentine-800"
              :class="{ 'bg-valentine-100 text-valentine-800 font-semibold': $route.path === '/admin/db' }"
            >
              <span class="text-xl">🗑️</span>
              <span>Limpieza</span>
            </NuxtLink>

            <!-- Divider -->
            <div class="border-t border-valentine-200 my-4"></div>

            <!-- Public Site -->
            <NuxtLink
              to="/"
              class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-valentine-700 hover:bg-valentine-50 hover:text-valentine-800"
            >
              <span class="text-xl">🌐</span>
              <span>Form de inscripción</span>
            </NuxtLink>
          </nav>

          <!-- System Status -->
          <div class="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              <span class="text-sm font-semibold text-green-800">Health Check API</span>
            </div>
            <p class="text-xs text-green-600">
              Todos los servicios funcionando correctamente
            </p>
          </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1">
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
  const adminUser  = ref(null)
  const { $toast } = useNuxtApp()

  onMounted(() => {
    try {
      const adminUserCookie = useCookie('adminUser')
      if (adminUserCookie.value) {
        adminUser.value = JSON.parse(adminUserCookie.value)
      }
    } catch (error) {
      console.error('Error parseando JSON del admin', error)
    }
  })

  const logout = () => {
    const adminToken      = useCookie('adminToken')
    const adminUserCookie = useCookie('adminUser')
    
    adminToken.value      = null
    adminUserCookie.value = null

    $toast.success('Sesión cerrada correctamente')    
    navigateTo('/admin/login')
  }
</script>