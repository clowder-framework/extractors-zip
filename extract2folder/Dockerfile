# FROM clowder/python-base
FROM python:3.7-slim
MAINTAINER Max Burnette <mburnet2@illinois.edu>

ARG VERSION="unknown"
ARG BUILDNUMBER="unknown"
ARG GITSHA1="unknown"

# command to run when starting docker
COPY entrypoint.sh *.py extractor_info.json requirements.txt /home/clowder/
RUN pip install -r  /home/clowder/requirements.txt
ENTRYPOINT ["/home/clowder/entrypoint.sh"]
CMD ["extractor"]

# Setup environment variables. These are passed into the container. You can change
# these to your setup. If RABBITMQ_URI is not set, it will try and use the rabbitmq
# server that is linked into the container. MAIN_SCRIPT is set to the script to be
# executed by entrypoint.sh
ENV VERSION=${VERSION} \
    BUILDNUMBER=${BUILDNUMBER} \
    GITSHA1=${GITSHA1} \
    RABBITMQ_URI="" \
    RABBITMQ_EXCHANGE="clowder" \
    RABBITMQ_VHOST="%2F" \
    RABBITMQ_QUEUE="ncsa.zip.extract2folder" \
    MAIN_SCRIPT="ncsa.zip.extract2folder.py"
