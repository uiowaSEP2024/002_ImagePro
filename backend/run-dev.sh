script_dir=$(dirname "$0")
cd "$script_dir"
APP_ENV='development' uvicorn app.main:app --reload