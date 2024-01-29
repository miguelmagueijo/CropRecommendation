# Crop Recommendation Prototype UI

Website (prototype) that allows to interact with the API of this repository.

Developed with **SvelteKit**.

## Docker
Build the docker image using the Dockerfile, then run a container with it.

This command will build the image if ran with the UI main directory as working directory (where this README is located):

`docker build --tag miguelmagueijo/crui .`

Example:

`docker run -p 9501:3000 miguelmagueijo/crui`
