FROM ubuntu:jammy-20240125
LABEL authors="iejohnson"
ARG DEBIAN_FRONTEND="noninteractive"
ENV TZ="America/Chicago"
ENV LANG C.UTF-8

# Set the working directory
WORKDIR /usr/src/app

COPY Linux /usr/src/app/Linux
COPY example_hospital.json.in /usr/src/app
COPY run_hospital.sh /usr/src/app
RUN chmod +x /usr/src/app/run_hospital.sh

RUN apt-get update && \
    apt-get install -yq \
         build-essential \
         tzdata \
         python3 python3-pip \
         python3-venv \
         && apt-get upgrade -yq \
         && rm -rf /var/lib/apt/lists/*

EXPOSE 4030
EXPOSE 8030

CMD ["/usr/src/app/run_hospital.sh"]
# Install the necessary packages
