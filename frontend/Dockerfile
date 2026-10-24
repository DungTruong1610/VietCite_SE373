# VietCite web (Vite dev server). Build context: repo root (needs packages/cnma-react-ui-*.tgz).
FROM node:22-slim

WORKDIR /app
COPY packages/cnma-react-ui-1.1.4.tgz ./packages/
COPY frontend/package.json frontend/package-lock.json frontend/.npmrc ./frontend/
WORKDIR /app/frontend
RUN npm ci
COPY frontend/ ./

ENV VITE_HOST=0.0.0.0
EXPOSE 5173
CMD ["npm", "run", "dev"]
