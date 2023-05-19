# Start from a base image
FROM ubuntu:22.04

# Install Python and pip
RUN apt-get update && apt-get install -y python3.10 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the stockfish binary
COPY stockfish /usr/games/stockfish

# Make it executable
RUN chmod +x /usr/games/stockfish

# Copy the current directory contents into the container at /app
COPY . /app

# Expose any necessary ports (if your app serves HTTP, for example)
EXPOSE 5005

# Define the command to run your app using CMD which defines your runtime
# Here we use python command to run our python app
CMD [ "python3", "./main.py" ]
