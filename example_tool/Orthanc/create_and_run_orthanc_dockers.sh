#!/bin/bash

echo "Select the Orthanc instance to configure:"
echo "1) Internal PACS"
echo "2) Hospital PACS"
read -r -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        ORTHANC_INSTANCE="internal_pacs"
        DCMPORT="4026" # Example DICOM port for Internal PACS
        HTTPPORT="8026" # Example HTTP port for Internal PACS
        ;;
    2)
        ORTHANC_INSTANCE="hospital"
        DCMPORT="4030" # Example DICOM port for Hospital PACS
        HTTPPORT="8030" # Example HTTP port for Hospital PACS
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
docker stop orthanc_${ORTHANC_INSTANCE} || echo "No Orthanc processes were found running."
docker rm orthanc_${ORTHANC_INSTANCE} || echo "No Orthanc processes were found running."


# Example command to run Docker build with the chosen configuration
echo "Building Docker image for ${ORTHANC_INSTANCE} PACS with DICOM port ${DCMPORT} and HTTP port ${HTTPPORT}..."
docker build --build-arg ORTHANC_INSTANCE=${ORTHANC_INSTANCE} --build-arg DCMPORT=${DCMPORT} --build-arg HTTPPORT=${HTTPPORT} -t orthanc_${ORTHANC_INSTANCE} .

docker run -d -p ${DCMPORT}:${DCMPORT} -p ${HTTPPORT}:${HTTPPORT} --name orthanc_${ORTHANC_INSTANCE} orthanc_${ORTHANC_INSTANCE}

echo "Docker image for ${ORTHANC_INSTANCE} PACS has been built successfully."
