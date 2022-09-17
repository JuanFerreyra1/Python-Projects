This package shows Dockerfile used for developing and deploying image Challenge_two needed to execute second challenge required. Also, it contains requirements.txt file copied into the image to include needed packages for the python programme.
Otherwise, it's important to follow these steps in order to get the expected output:

1) Joining swarm:
 docker swarm join --token SWMTKN-1-5ab5umaj9x7926jug3ism2cvh3g1gfj0uy1vcv5gkdb5a1ntwe-clkc86xmqk2qd8rb7fqx9sdzr 192.168.1.39:2377

2) Run container attached to the image in dockerhub
docker run --network connection -p 3306:3306 juanferreyra/python_images:Challenge_two



Finally, following those steps it's going to be possible to run Challenge_two class and get the specific metrics.