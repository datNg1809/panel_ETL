#! /bin/bash

my_docker_images=($(docker image ls | grep panel | awk '{print $1}'))
for i in "${my_docker_images[@]}"; do new_tag=$(echo "${DOCKER_REGISTRY}/${DOCKER_NAMESPACE}/${i}:${CI_COMMIT_SHA:0:8}"); docker tag "${i}" "${new_tag}";  docker push "${new_tag}"; done
