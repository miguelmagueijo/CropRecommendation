# CropRecommendation API

Build the docker image using the Dockerfile, then run a container with it.

This command will build the image if ran with the API main directory as working directory (where this README is located):

`docker build --tag miguelmagueijo/crapi .`

The models need to be provided through a volume, into the container directory `/app/Models`, and the HTTP server will be exposed through port 8000

Example:

`docker run -p 8000:8000 -v ./Models:/app/Models miguelmagueijo/crapi`
