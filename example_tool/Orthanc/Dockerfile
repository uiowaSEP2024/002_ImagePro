# Use Ubuntu as the base image
FROM ubuntu:jammy-20240125

# Metadata as key/value label
LABEL maintainer="iejohnson"

# Avoid user interaction with tzdata when installing
ARG DEBIAN_FRONTEND="noninteractive"

# Argument to determine the Orthanc instance type
ARG ORTHANC_INSTANCE="internal_pacs"

# Timezone can be overridden during build if needed
ARG TZ="America/Chicago"
ENV TZ=${TZ}

# Ensure UTF-8 locale
ENV LANG C.UTF-8

# Add non-root user and group
# Note: The -S option is for Alpine. Use `adduser` and `addgroup` without -S for Ubuntu.
# https://stackoverflow.com/questions/27701930/how-to-add-users-to-docker-container
RUN groupadd nonroot \
    && useradd -m -s /bin/bash -g nonroot nonroot

# Working directory for the application
WORKDIR /usr/src/app

# Copy files as root user
COPY Linux /usr/src/app/Linux
COPY example_${ORTHANC_INSTANCE}.json.in /usr/src/app/example_${ORTHANC_INSTANCE}.json.in
COPY example_internal_pacs.lua /usr/src/app/example_internal_pacs.lua
COPY run_${ORTHANC_INSTANCE}.sh /usr/src/app/run_orthanc.sh

# Make the script executable
RUN chmod +x /usr/src/app/run_orthanc.sh

# Change ownership of the app directory to the nonroot user
RUN chown -R nonroot:nonroot /usr/src/app



# Install dependencies and clean up in one layer to keep the image size down
# Combine installation commands and clean up to reduce layer size and simplify.
# Install dependencies, avoiding recommended and suggested packages, then clean up
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    tzdata \
    net-tools \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# These IP's are hardcoded so that Orthanc's can communicate with each other
RUN if [ "$ENV" = "hospital" ] ; then ip addr add 192.168.1.100/24 dev eth0 ; else ip addr add 192.168.1.200/24 dev eth0 ; fi

# Use the nonroot userRUN if
USER nonroot
# Arguments to customize ports; these can be overridden during build
ARG DCMPORT
ARG HTTPPORT

# Expose ports based on ARGs to make it flexible
EXPOSE $DCMPORT $HTTPPORT

# Command to run the application
CMD ["/usr/src/app/run_orthanc.sh"]
