NAME="monster-hunter-armor-build-tool"
docker build -f Dockerfile -t $NAME . 
docker run -it -v ./:/home --net=host $NAME 
