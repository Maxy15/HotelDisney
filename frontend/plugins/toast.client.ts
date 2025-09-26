import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin(() => {
  // Simple toast implementation
  const toast = {
    success: (message: string) => {
      showToast(message, 'success')
    },
    error: (message: string) => {
      showToast(message, 'error')
    },
    info: (message: string) => {
      showToast(message, 'info')
    },
    warning: (message: string) => {
      showToast(message, 'warning')
    }
  }

  const showToast = (message: string, type: string = 'info') => {
    // Create toast element
    const toastElement = document.createElement('div')
    toastElement.className = getToastClasses(type)
    toastElement.textContent = message
    
    // Position and style
    toastElement.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      max-width: 400px;
      padding: 12px 16px;
      border-radius: 8px;
      font-weight: 500;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      transform: translateX(100%);
      transition: transform 0.3s ease-in-out;
    `
    
    // Add to DOM
    document.body.appendChild(toastElement)
    
    // Animate in
    setTimeout(() => {
      toastElement.style.transform = 'translateX(0)'
    }, 100)
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      toastElement.style.transform = 'translateX(100%)'
      setTimeout(() => {
        if (document.body.contains(toastElement)) {
          document.body.removeChild(toastElement)
        }
      }, 300)
    }, 5000)
    
    // Click to dismiss
    toastElement.addEventListener('click', () => {
      toastElement.style.transform = 'translateX(100%)'
      setTimeout(() => {
        if (document.body.contains(toastElement)) {
          document.body.removeChild(toastElement)
        }
      }, 300)
    })
  }

  const getToastClasses = (type: string): string => {
    const baseClasses = 'cursor-pointer text-white'
    
    switch (type) {
      case 'success':
        return `${baseClasses} bg-green-500`
      case 'error':
        return `${baseClasses} bg-red-500`
      case 'warning':
        return `${baseClasses} bg-yellow-500 text-black`
      case 'info':
      default:
        return `${baseClasses} bg-blue-500`
    }
  }

  return {
    provide: {
      toast
    }
  }
})