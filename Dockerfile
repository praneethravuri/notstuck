FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build Next.js application
RUN npm run build

# Final image
FROM node:20-slim

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy frontend build
COPY --from=frontend-build /app/frontend/.next /app/frontend/.next
COPY --from=frontend-build /app/frontend/public /app/frontend/public
COPY --from=frontend-build /app/frontend/package*.json /app/frontend/
COPY --from=frontend-build /app/frontend/node_modules /app/frontend/node_modules

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Create a script to run both services
RUN echo '#!/bin/bash\n\
cd /app/backend\n\
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend\n\
npm run start' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000
EXPOSE 3000

CMD ["/bin/bash", "/app/start.sh"]