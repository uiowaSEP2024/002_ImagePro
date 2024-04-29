#!/bin/bash
orthanc_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

internal_pacs_storage="${orthanc_dir}/OrthancStorage"
internal_pacs_template="${orthanc_dir}/example_internal_pacs_for_aws.json.in"
internal_pacs_json="${internal_pacs_storage}/internal_pacs.json"
lua_script_path="${orthanc_dir}/example_internal_pacs.lua"

mkdir -p "${internal_pacs_storage}"
orthanc_binary=${orthanc_dir}/$(uname -s)/Orthanc

# shellcheck disable=SC2002
cat "${internal_pacs_template}" \
  | sed "s#__PLACE_LUA_SCRIPT_PATH_HERE__#${lua_script_path}#g" \
  | sed "s#__ORTHANC_STORAGE_PATH_HERE__#${internal_pacs_storage}#g" \
  | sed "s#__ORTHANC_NAME__#EXAMPLE_INTERNAL_TOOL#g" \
  | sed "s#__ORTHANC_HTTP_PORT__#8026#g" \
  | sed "s#__ORTHANC_DICOM_PORT__#4026#g" \
  | sed "s#__ORTHANC_AET__#EXAMPLE_TOOL#g" \
  > "${internal_pacs_json}"

# ========================
echo "${orthanc_binary}" "${internal_pacs_json}"
${orthanc_binary} "${internal_pacs_json}"
