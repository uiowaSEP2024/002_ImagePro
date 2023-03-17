function main() {
  cdk deploy "$@"
  exit $?
}

main "$@"
