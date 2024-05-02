# Use the official Python image as a base
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# [production] Copy the current directory contents into the container at /app
ADD . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["echo", "passing the main program to entrypoint.sh"]
