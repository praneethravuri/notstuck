FROM node:20-alpine as frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim

WORKDIR /app

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

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
npm run preview' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000
EXPOSE 3000

CMD ["/app/start.sh"]