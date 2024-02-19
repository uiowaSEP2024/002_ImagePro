# Use Ubuntu as the base image
FROM ubuntu:jammy-20240125

# Metadata as key/value label
LABEL maintainer="iejohnson"

# Avoid user interaction with tzdata when installing
ARG DEBIAN_FRONTEND="noninteractive"

# Argument to determine the Orthanc instance type
ARG ORTHANC_INSTANCE="default"

# Timezone can be overridden during build if needed
ARG TZ="America/Chicago"
ENV TZ=${TZ}

# Ensure UTF-8 locale
ENV LANG C.UTF-8

# Working directory for the application
WORKDIR /usr/src/app

# Conditional copy based on the ORTHANC_INSTANCE argument
COPY Linux /usr/src/app/Linux
COPY example_${ORTHANC_INSTANCE}.json.in /usr/src/app/example_${ORTHANC_INSTANCE}.json.in
COPY example_internal_pacs.lua /usr/src/app/example_internal_pacs.lua
COPY run_${ORTHANC_INSTANCE}.sh /usr/src/app/run_orthanc.sh

# Make the script executable
RUN chmod +x /usr/src/app/run_orthanc.sh

# Install dependencies and clean up in one layer to keep the image size down
RUN apt-get update && \
    apt-get install -yq \
         build-essential \
         tzdata \
         && apt-get upgrade -yq \
         && rm -rf /var/lib/apt/lists/*

# Arguments to customize ports; these can be overridden during build
ARG DCMPORT
ARG HTTPPORT

# Expose ports based on ARGs to make it flexible
EXPOSE $DCMPORT $HTTPPORT

# Command to run the application
CMD ["/usr/src/app/run_orthanc.sh"]
