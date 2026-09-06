FROM node:24-slim

LABEL maintainer="Ahmed Sami <ahmed.sami@yahoo.com>"
LABEL org.opencontainers.image.title="Unified Big Data Engineering Control Hub"
LABEL org.opencontainers.image.description="Modern glassmorphic control hub and monitor for Apache Hadoop and Spark"
LABEL org.opencontainers.image.version="1.0.0"

WORKDIR /app

# Copy application files
COPY package.json ./
COPY server.js ./
COPY public ./public

ENV PORT=3000
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/status', (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["node", "server.js"]
