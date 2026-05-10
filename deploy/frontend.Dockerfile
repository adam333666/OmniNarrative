FROM node:22-bookworm

WORKDIR /app/frontend
COPY frontend/package.json ./package.json
COPY frontend/package-lock.json ./package-lock.json
RUN npm install
CMD ["npm", "run", "dev"]
