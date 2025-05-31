# frontend/Dockerfile

# Estágio 1: Construir a aplicação React
FROM node:20-alpine AS build 

WORKDIR /app

# Copia package.json e o NOVO package-lock.json
COPY package.json package-lock.json ./

# Instala as dependências de forma limpa usando o lockfile
RUN npm ci

# Copia o restante do código da aplicação
COPY . .

# Garante que os binários instalados pelo npm estejam no PATH
ENV PATH /app/node_modules/.bin:$PATH

# Constrói a aplicação
RUN npm run build

# Estágio 2: Servir a aplicação construída usando Nginx
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]