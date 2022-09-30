#!/bin/bash
PORT=7777
echo tunneling to $1 port $PORT
ssh -L $PORT:localhost:$PORT $1
