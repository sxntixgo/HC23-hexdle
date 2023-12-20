# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.11-alpine AS builder
EXPOSE 8000
WORKDIR /hchexdle 
COPY requirements.txt /hchexdle/requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /hchexdle