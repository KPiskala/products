# parent image
FROM python:3.10

# set the working directory in the container
WORKDIR /app

# copy current directory contents into the container at /app
COPY . /app

# install pckages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r .requirements_dev.txt

# Command to run the main script
CMD ["python", "main.py"]
