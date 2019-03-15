# Author : Alexandre DIEUL
#
# Note : Remember that we build an image (named neural_marvel) and from that image, 
#	we can run multiple containers (here, just one named neural_marvel_instance_1)
#
#Remove app folder in the container neural_marvel_instance_1
sudo docker exec neural_marvel_instance_1 rm -Rf app
#Copy local app folder into container neural_marvel_instance_1
sudo docker cp app neural_marvel_instance_1:/app
#Stop container
sudo docker container stop neural_marvel_instance_1
#Launch container (detach process)
sudo docker run -p 5042:5042 --name neural_marvel_instance_1 -d neural_marvel