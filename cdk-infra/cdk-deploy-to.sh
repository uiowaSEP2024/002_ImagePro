#!/bin/bash

function main() {
  cdk deploy "$@"
  exit $?
}

main "$@"
