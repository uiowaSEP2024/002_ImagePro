script_dir=$(dirname "$0")
cd "$script_dir"
APP_ENV='test' pytest --cov