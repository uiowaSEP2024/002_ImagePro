script_dir=$(dirname "$0")
cd "$script_dir"
export ENVIRONMENT='test'
pytest --cov