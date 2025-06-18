# 1. Base Image
FROM python:3.9-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# 3. Install OS Dependencies for Pygame and X11 Forwarding
RUN apt-get update && apt-get install -y --no-install-recommends     libsdl2-2.0-0     libsdl2-image-2.0-0     libsdl2-mixer-2.0-0     libsdl2-ttf-2.0-0     libx11-6     # Add any other X11 client libraries that might be needed by Pygame's SDL backend
    # For example: libxext6 libxrender1 libxfixes3 libxi6
    libxext6 libxrender1 libxfixes3 libxi6     && rm -rf /var/lib/apt/lists/*

# 4. Set Work Directory
WORKDIR /app

# 5. Install Python Dependencies
# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN python -m pip install --upgrade pip &&     pip install -r requirements.txt

# 6. Copy Application Code
# Copy assets, config, and src directory
COPY assets ./assets
COPY config.json ./config.json
COPY src ./src

# 7. Set the default command to run the application
# Assumes your main game logic is runnable via 'python -m src.main'
CMD ["python", "-m", "src.main"]
