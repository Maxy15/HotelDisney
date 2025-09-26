// Opción 1: Con imports explícitos (recomendado para evitar errores TS)
export default defineNuxtRouteMiddleware((to, from) => {
  // Check if admin token exists
  const adminToken = useCookie('adminToken')
  
  if (!adminToken.value) {
    // No token found, redirect to admin login
    return navigateTo('/admin/login')
  }
  
  // Token exists, allow access
  return true
})