# frontend/Dockerfile
FROM node:20 as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20 as test
WORKDIR /app
COPY --from=builder /app /app
RUN npm test

FROM node:20 as production
WORKDIR /app
COPY --from=builder /app /app
CMD ["npm", "start"]
