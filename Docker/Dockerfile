# Stage 1: Build the application
# Use the official Node.js 18 image as the base image for building the app
FROM node:18 AS build

# Enable BuildKit caching by specifying the cache directory
RUN --mount=type=cache,target=/root/.npm npm set cache /root/.npm

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies, utilizing caching
RUN npm install --cache /root/.npm

# Copy application source code
COPY . .

# Build the application (if necessary, e.g., transpiling TypeScript)
# RUN npm run build

# Stage 2: Create the runtime image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy the built app from the previous stage
COPY --from=build /app /app

# Expose the port the app runs on
EXPOSE 8080

# Run the Node.js app
CMD ["node", "main.js"]
