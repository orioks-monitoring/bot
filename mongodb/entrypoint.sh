#!/bin/bash
set -e

mongod --replSet rs0 --bind_ip_all &
MONGOD_PID=$!

until mongosh --host localhost --eval "print(\"waited for connection\")"
do
    sleep 2
done

mongosh --host localhost <<EOF
rs.initiate({
  _id: 'rs0',
  members: [{ _id: 0, host: 'mongodb:27017' }]
})
EOF

wait $MONGOD_PID
