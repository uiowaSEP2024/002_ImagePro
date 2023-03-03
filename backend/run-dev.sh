script_dir=$(dirname "$0")
cd "$script_dir"
export ENVIRONMENT='development'
uvicorn app.main:app --reload