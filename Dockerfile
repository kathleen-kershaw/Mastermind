FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements to the container's working directory and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your python modules to the container's working directory
COPY Mastermind_Engine.py .
COPY Mastermind_Web.py .

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the Streamlit web app
CMD ["streamlit", "run", "Mastermind_Web.py", "--server.port=8501", "--server.address=0.0.0.0"]
