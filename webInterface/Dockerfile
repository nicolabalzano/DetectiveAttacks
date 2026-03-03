# 1. Usa un'immagine leggera
FROM node:20-slim

WORKDIR /app

# 2. Copia SOLO i file dei pacchetti prima di tutto il resto
COPY package.json package-lock.json ./

# 3. Usa 'npm ci' invece di 'npm install'
# --frozen-lockfile assicura che non ci siano cambiamenti al lock
# --network-timeout aumenta la tolleranza per la tua rete
RUN npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-timeout 300000 && \
    npm ci --quiet

# 4. SOLO ORA copia il resto del codice
COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]