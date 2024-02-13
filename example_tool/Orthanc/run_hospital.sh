#!/bin/bash
orthanc_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

hospital_pacs_storage="${orthanc_dir}/OrthancStorage/hospital01_pacs_storage"
hospital_pacs_template="${orthanc_dir}/example_hospital.json.in"
hospital_pacs_json="${hospital_pacs_storage}/hospital01.json"
mkdir -p "${hospital_pacs_storage}"
orthanc_binary=${orthanc_dir}/$(uname -s)/Orthanc

# shellcheck disable=SC2002
cat "${hospital_pacs_template}" \
  | sed "s#__PLACE_LUA_SCRIPT_PATH_HERE__##g" \
  | sed "s#__ORTHANC_STORAGE_PATH_HERE__#${hospital_pacs_storage}#g" \
  | sed "s#__ORTHANC_NAME__#EXAMPLE_HOSPITAL_NAME#g" \
  | sed "s#__ORTHANC_HTTP_PORT__#8030#g" \
  | sed "s#__ORTHANC_DICOM_PORT__#4030#g" \
  | sed "s#__ORTHANC_AET__#EXAMPLE_HOSPITAL#g" \
  > "${hospital_pacs_json}"

# ========================
echo "${orthanc_binary}" "${hospital_pacs_json}"
${orthanc_binary} "${hospital_pacs_json}"
