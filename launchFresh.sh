#Stop container
sudo docker container stop neural_marvel
#Remove container
sudo docker container rm neural_marvel
#Re-build container
sudo docker build . -t neural_marvel
#Launch container (detach process)
sudo docker run -p 5042:5042 -d neural_marvel
