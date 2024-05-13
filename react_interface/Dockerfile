# Uso un'immagine node come base
FROM node:16-alpine

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di progetto
COPY package.json package-lock.json ./

# Installa le dipendenze usando npm
RUN npm install

# Copia il resto dei file
COPY . .

# Compila l'applicazione
RUN npm run build

# Installa serve per servire l'applicazione
RUN npm install -g serve

# Avvia il server
CMD ["serve", "-s", "build", "-l", "3001"]
