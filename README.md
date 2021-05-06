# Asynchronous chat

## Description

Asynchronous chat based on FastAPI + Websockets + Redis pub/sub.

- Connect to the chat: `ws://localhost:8000/ws/{client_id}`
- Get last messages: `http://localhost:8000/messages`


## Run server
    make up

## Run console client
    make client

## Run tests:
    make test

## Create venv:
    make venv

## Run linters:
    make lint

## Run formatters:
    make format
