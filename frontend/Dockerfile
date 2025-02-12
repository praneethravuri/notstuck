# Stage 1: Build the frontend using Node.js
FROM node:20-alpine AS builder

WORKDIR /app

# Accept build argument for the backend URL and set production environment
ARG NEXT_PUBLIC_BACKEND_URL
ENV NODE_ENV=production
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . ./

# Build the Next.js application
RUN npm run build

# Stage 2: Serve the built frontend using a lightweight Node.js runtime
FROM node:20-slim

WORKDIR /app

# Copy the production build and node_modules from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

# Expose the port used by Next.js (default: 3000)
EXPOSE 3000

# Start the Next.js server
CMD ["npm", "run", "start"]
