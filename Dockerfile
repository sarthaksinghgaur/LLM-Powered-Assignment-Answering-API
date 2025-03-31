FROM python:3.12-slim-bookworm

# Install Java (for Tabula) and Node.js
RUN apt-get update && apt-get install -y \
    default-jdk \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set working directory
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm -rf /root/.cache/pip

# Install Prettier globally
RUN npm install -g prettier@3.4.2

# Copy the rest of the application
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
