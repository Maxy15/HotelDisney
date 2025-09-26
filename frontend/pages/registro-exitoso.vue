<template>
  <div class="min-h-screen flex flex-col bg-gradient-valentine">
    <Navbar />
    
    <main class="flex-1 flex items-center justify-center">
      <div class="container mx-auto px-4 py-8">
        <div class="max-w-lg mx-auto bg-white rounded-2xl shadow-2xl p-8 border-4 border-valentine-200 text-center">
          <!-- Success Message -->
          <div class="space-y-6">
            <h1 class="text-3xl md:text-4xl font-bold text-valentine-800">
              ¡Gracias por registrarte!
            </h1>
            
            <div class="bg-valentine-50 border-2 border-valentine-200 rounded-lg p-6">
              <div class="text-6xl mb-4">📧</div>
              <p class="text-lg text-valentine-700 leading-relaxed">
                <strong>Revisa tu correo electrónico</strong>
              </p>
              <p class="text-valentine-600 mt-3">
                Te hemos enviado un enlace para verificar tu email
              </p>
            </div>

            <!-- Steps -->
            <div class="bg-gradient-disney rounded-lg p-6">
              <h3 class="text-xl font-semibold text-disney-800 mb-4 flex items-center justify-center gap-2">
                Próximos pasos
              </h3>

              <ol class="ol-steps space-y-3 text-left text-disney-700">
                <li>Busca nuestro email en tu bandeja de entrada</li>
                <li>Haz clic en el enlace de verificación</li>
                <li>Crea tu contraseña</li>
              </ol>

              <div class="mt-3 flex items-start gap-3">
                <span class="text-2xl">🎊</span>
                <p class="text-disney-700 font-semibold">¡Ya estarás participando en el sorteo!</p>
              </div>
            </div>

            <!-- Important Notes -->
            <div class="bg-rose-50 border-2 border-rose-200 rounded-lg p-4">
              <h3 class="font-semibold text-rose-800 mb-2 flex items-center justify-center gap-2">
                <span>⚠️</span>
                Importante
              </h3>
              <div class="text-sm text-rose-700 space-y-2">
                <p>• El enlace expira en 10 minutos por seguridad</p>
                <p>• Revisa también tu carpeta de spam/correo no deseado</p>
                <p>• Si no recibes el email, contáctanos</p>
              </div>
            </div>

            <!-- Prize Reminder -->
            <div class="bg-gradient-magic text-white rounded-lg p-6">
              <div class="text-4xl mb-3">🏆</div>
              <h3 class="text-xl font-bold mb-2">¡Tu premio te espera!</h3>
              <p class="text-lg">2 noches mágicas en Hotel Disney 🏰</p>
              <p class="text-sm opacity-90 mt-2">
                Una experiencia inolvidable para ti y tu pareja
              </p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-8 space-y-4">
            <button 
              @click="goToHome"
              class="w-full bg-valentine-500 hover:bg-valentine-600 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-300 flex items-center justify-center gap-2"
            >
              <span></span>
              Volver al inicio
            </button>
          </div>

          <!-- Contact Info -->
          <div class="mt-8 pt-6 border-t-2 border-valentine-100">
            <p class="text-sm text-valentine-600">
              ¿Problemas con el registro? 
              <a href="mailto:soporte@ctsturismo.cl" class="underline hover:text-valentine-800">
                Contáctanos aquí
              </a>
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
    title : 'Registro Exitoso - Sorteo San Valentín Disney',
    meta  : [
      { 
        name    : 'description', 
        content : 'Tu registro ha sido exitoso. Revisa tu correo electrónico para completar la verificación.' 
      }
    ]
  })

  const goToHome = () => {
    navigateTo('/')
  }

  const checkEmail = () => {
    window.location.href = 'mailto:'
  }
</script>

<style>
  .ol-steps { counter-reset: step; }
  .ol-steps li { counter-increment: step; }
  .ol-steps li::before {
    content: counter(step);
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; margin-right: 12px;
    border-radius: 9999px; font-weight: 700;
    background: #F1F5FF; color: #1F2A69; /* ajusta a tu paleta */
  }
</style>