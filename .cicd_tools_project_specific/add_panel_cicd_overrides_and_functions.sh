#! /bin/bash
# This script build and push the images for DQC_PANEL

replace_place_holder_values_in_docker_compose_file(){
 sed -i "s/DOCKER_REGISTRY/${DOCKER_REGISTRY}/g" "${DOCKER_COMPOSE_FILE_GIT_RELATIVE_PATH}" 
 sed -i "s/DOCKER_NAMESPACE/${DOCKER_NAMESPACE}/g" "${DOCKER_COMPOSE_FILE_GIT_RELATIVE_PATH}"
 sed -i "s/CI_COMMIT_SHA/${CI_COMMIT_SHA:0:8}/g" "${DOCKER_COMPOSE_FILE_GIT_RELATIVE_PATH}"
 sed -i "s/DWH_PRIVATE_IP/${DWH_PRIVATE_IP}/g" "${DOCKER_COMPOSE_FILE_GIT_RELATIVE_PATH}"
}

make_sure_bash_is_installed(){
 apk add bash
}

create_network_to_make_dwh_accessible(){
  NETWORK_RANGE_NOT_FILTERED_BY_DWH_FIREWALL="172.16.254.0/24"

  docker network create --driver=bridge --subnet=${NETWORK_RANGE_NOT_FILTERED_BY_DWH_FIREWALL} panel_elk || echo "Network already created" 
}
