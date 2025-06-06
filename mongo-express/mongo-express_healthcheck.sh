#!/bin/bash
wget --quiet --tries=1 --spider --header "Authorization: Basic $(echo -n admin:admin | base64)" http://localhost:8081 || exit 1
