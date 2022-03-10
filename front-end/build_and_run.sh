docker stop easytweet_frontend
docker rm easytweet_frontend
docker rmi $(docker images -f dangling=true -q)
docker rmi $(docker images -q datalabs/easytweet-frontend)
docker build . --tag=datalabs/easytweet-frontend
docker run -it -d -p 3000:3000 --env-file .env --restart always --name easytweet_frontend datalabs/easytweet-frontend:latest