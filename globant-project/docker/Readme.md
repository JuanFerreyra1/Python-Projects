This package shows Dockerfile used for developing and deploying image Challenge_two needed to execute second challenge required. Also, it contains requirements.txt file copied into the image to include needed packages for the python programme.
Otherwise, it's important to follow these steps in order to get the expected output:

1) Joining swarm:
docker swarm join --token SWMTKN-1-5zvvby3lm9v71kyydcjqzkwt1s2wh9z4gjyw5vb4wrbp2yzbwm-ahnplv7uu09s2qc6kna68dkl4 192.168.1.47:2377

2) Run container attached to the image in dockerhub
docker run --network challenge -p 3306:3306 juanferreyra/python_images:Challenge_two



Finally, following those steps it's going to be possible to run Challenge_two class and get the specific metrics.