#! /bin/bash
set -u

test_type=${1:-"unit"}

pytest test
