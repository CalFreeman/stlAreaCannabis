#!/bin/bash
sudo systemctl start docker
cd ../docker/
docker-compose up -d