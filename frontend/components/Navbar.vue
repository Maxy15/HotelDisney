<template>
  <nav class="bg-gradient-to-r from-valentine-100 via-purple-100 to-valentine-100 border-b-2 border-valentine-300">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-3 group">
          <div class="text-4xl transform group-hover:scale-110 transition-transform">
            🏰
          </div>
          <div>
            <h1 class="text-2xl font-bold text-valentine-800 group-hover:text-valentine-900 transition-colors">
              CTS Turismo
            </h1>
            <p class="text-xs text-valentine-600">Sorteo San Valentín</p>
          </div>
        </NuxtLink>

        <!-- Admin Link -->
        <NuxtLink 
          to="/admin/login"
          class="flex items-center gap-2 bg-valentine-500 hover:bg-valentine-600 text-white px-4 py-2 rounded-lg transition-all transform hover:scale-105 shadow-md hover:shadow-lg"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span class="font-semibold">Admin</span>
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
</style>