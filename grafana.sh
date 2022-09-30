#!/bin/bash
echo go to http://localhost:3000/ once the tunnel is up
ssh -L 3000:localhost:3000 meerkat
