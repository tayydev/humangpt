@echo off
 docker run -d ^
   --name mongodb ^
   -p 27017:27017 ^
   -e MONGO_INITDB_ROOT_USERNAME=username ^
   -e MONGO_INITDB_ROOT_PASSWORD=password123 ^
   --mount type=tmpfs,destination=/data/db ^
   mongo:latest

 echo MongoDB container started on port 27017