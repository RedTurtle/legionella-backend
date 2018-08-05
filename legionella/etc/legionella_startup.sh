#!/bin/bash
WORKING_DIR=/opt/legionella/legionella-backend/legionella
ACTIVATE_PATH=/opt/legionella/legionella-backend/bin/activate
cd ${WORKING_DIR}
source ${ACTIVATE_PATH}
exec $@

