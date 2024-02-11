# Use the Python 3.8 slim base image
FROM python:3.8-slim

# Create app directory
WORKDIR /app

# Create a user and group with unique UID and GID
RUN groupadd -g 15001 mygroup && \
    useradd -u 150001 -g mygroup myuser

# Copy requirements.txt first for caching
COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy over the rest of the application logic
COPY . /app

# Expose Flask port
EXPOSE 5000

# Set up needed environment variables
ENV project_name="skipify-demo"
ENV surrogate_name="CC"

# Set container user uid/gid
USER myuser:mygroup

# Set max memory footprint for container process
# (Adjust the value according to your requirements)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app", "--limit-request-line", "0"]
