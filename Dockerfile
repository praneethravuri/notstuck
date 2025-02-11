# Frontend build stage
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Set production environment and accept build arg for the backend URL.
ENV NODE_ENV=production
ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend source (including .env.production if needed)
COPY frontend/ ./

# Build Next.js application (this build will pick up NEXT_PUBLIC_BACKEND_URL)
RUN npm run build

# Final image
FROM node:20-slim

# Install Python and required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy frontend build output
COPY --from=frontend-build /app/frontend/.next /app/frontend/.next
COPY --from=frontend-build /app/frontend/public /app/frontend/public
COPY --from=frontend-build /app/frontend/package*.json /app/frontend/
COPY --from=frontend-build /app/frontend/node_modules /app/frontend/node_modules

# Set up Python virtual environment and install dependencies
RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Install Python dependencies in virtual environment
COPY backend/requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Create a script to run both services
RUN echo '#!/bin/bash\n\
source /opt/venv/bin/activate\n\
cd /app/backend\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend\n\
npm run start' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000
EXPOSE 3000

CMD ["/bin/bash", "/app/start.sh"]
