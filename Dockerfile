# Use the official Python image as the base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN pip install .

# Compile and install dependencies
# RUN pip-compile pyproject.toml -o requirements.txt && pip install -r requirements.txt

# Set the command to run the application
CMD ["streamlit", "run", "src/react_agent/app.py"]
