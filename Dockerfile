FROM python:3.9

WORKDIR /code

# Copy the file with the requirements to the /code directory.
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy script for app entry point
COPY ./.docker/app_start.sh /usr/local/bin/start

# update start script permissions
RUN chmod u+x /usr/local/bin/start

# Copy the ./app directory inside the /code directory
COPY ./app /code/app

# start with running start script
CMD ["/usr/local/bin/start"]


