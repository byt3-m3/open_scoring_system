#!/usr/bin/env bash

docker build . -f dev.dockerfile -t cbaxter1988/scoring_server:build2

docker push cbaxter1988/scoring_server:build2