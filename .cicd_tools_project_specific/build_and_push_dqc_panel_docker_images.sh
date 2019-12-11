#! /bin/bash
# This script build and push the images for DQC_PANEL

DOCKER_REGISTRY=${1:?Error}
DOCKER_NAMESPACE=${2:?Error}
CI_COMMIT_SHA=${3:?Error}

build_and_push_dqc_panel_docker_images(){
    local DOCKER_REGISTRY=${1:?Error}
    local DOCKER_NAMESPACE=${2:?Error}
    local CI_COMMIT_SHA=${3:?Error}

    build_images_with_docker_compose
    push_all_the_images_with_panel_in_their_name "${DOCKER_REGISTRY}" "${DOCKER_NAMESPACE}" "${CI_COMMIT_SHA:0:8}"
}
		build_images_with_docker_compose(){
				docker-compose build --parallel
		}

		push_all_the_images_with_panel_in_their_name(){
				local DOCKER_REGISTRY=${1:?Error}
				local DOCKER_NAMESPACE=${2:?Error}
				local CI_COMMIT_SHA=${3:?Error}


				my_docker_images=($(docker image ls | grep panel | awk '{print $1}'))
				for i in "${my_docker_images[@]}"; do
						new_tag=$(echo "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${i}:${CI_COMMIT_SHA:0:8}")
						docker tag "${i}" "${new_tag}"
						docker push "${new_tag}"
				done
		}


build_and_push_dqc_panel_docker_images "${DOCKER_REGISTRY}" "${DOCKER_NAMESPACE}" "${CI_COMMIT_SHA:0:8}"

