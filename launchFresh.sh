# Author : Alexandre DIEUL
#
# Note : Remember that we build an image (named neural_marvel) and from that image, 
#	we can run multiple containers (here, just one named neural_marvel_instance_1)
#
#Stop container
sudo docker container stop neural_marvel_instance_1
#Remove all containers (like neural_marvel_instance_1) based on the image neural_marvel
sudo docker ps -a | awk '{ print $1,$2 }' | grep neural_marvel | awk '{print $1 }' | sudo xargs -I {} docker rm {}
#Remove the image neural_marvel
sudo docker rmi neural_marvel
#Re-build the container
sudo docker build . -t neural_marvel
#Launch container (detach process)
sudo docker run -p 5042:5042 --name neural_marvel_instance_1 -d neural_marvel
