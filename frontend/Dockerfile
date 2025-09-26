FROM node:18-alpine

# Crear directorio de la app
WORKDIR /app

# Copiar packages
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Preparar Nuxt
RUN npx nuxt prepare

# Construir aplicación
RUN npm run build

# Exponer puerto
EXPOSE 3000

# Empezar aplicación
CMD ["npm", "run", "dev"]