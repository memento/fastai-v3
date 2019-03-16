# Author : Alexandre DIEUL
#
# Note : Remember that we build an image (named neural_marvel) and from that image, 
#	we can run multiple containers (here, just one named neural_marvel_instance_1)
#
#Remove static folder in the container neural_marvel_instance_1
sudo docker exec neural_marvel_instance_1 rm -Rf app/static
#Copy local static app folder into container neural_marvel_instance_1
sudo docker cp app/static neural_marvel_instance_1:/app/static
#Remove view app folder in the container neural_marvel_instance_1
sudo docker exec neural_marvel_instance_1 rm -Rf app/view
#Copy local view app folder into container neural_marvel_instance_1
sudo docker cp app/view neural_marvel_instance_1:/app/view
##Stop container
#sudo docker container stop neural_marvel_instance_1
##Launch container (detach process)
#sudo docker run -p 5042:5042 --name neural_marvel_instance_1 -d neural_marvel