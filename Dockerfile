FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build Next.js application
RUN npm run build

FROM python:3.13-slim

WORKDIR /app

# Copy frontend build
COPY --from=frontend-build /app/frontend/.next /app/frontend/.next
COPY --from=frontend-build /app/frontend/public /app/frontend/public
COPY --from=frontend-build /app/frontend/package*.json /app/frontend/
COPY --from=frontend-build /app/frontend/node_modules /app/frontend/node_modules

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Create a script to run both services
RUN echo '#!/bin/bash\n\
cd /app/backend\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend\n\
npm run start' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000
EXPOSE 3000

CMD ["/app/start.sh"]