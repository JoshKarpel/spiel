set -xeu

TAG="spiel:test"

docker build -f docker/Dockerfile -t "$TAG" .
docker run -it --rm "$TAG" spiel version
