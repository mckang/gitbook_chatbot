FROM node:20-alpine as build

WORKDIR /app

# Install dependencies
COPY package.json package-lock.* ./
RUN npm install

ARG NEXT_PUBLIC_CHAT_API
ARG NEXT_PUBLIC_GITBOOK_URL

RUN echo $NEXT_PUBLIC_CHAT_API
ENV NEXT_PUBLIC_CHAT_API=${NEXT_PUBLIC_CHAT_API}
ENV NEXT_PUBLIC_USE_LLAMACLOUD=false
ENV NEXT_PUBLIC_GITBOOK_URL=${NEXT_PUBLIC_GITBOOK_URL}


# Build the application
COPY . .
RUN npm run build

# ====================================
FROM build as release


CMD ["npm", "run", "start"]