function unquote() {
  echo "$1" | tr -d '"'
}

function create_image_repository() {
  local repository_name=$1
  local existing_repository

  existing_repository=$(aws ecr describe-repositories --repository-names "$repository_name")

  if [ -z "$existing_repository" ] || [ "$existing_repository" == "null" ]; then
    echo "===>Creating ECR repository..."
    aws ecr create-repository --repository-name "$repository_name" \
      --image-scanning-configuration scanOnPush=true \
      --image-tag-mutability MUTABLE
  else
    echo "Repository already exists. Skipping creation."
  fi
}

function publish_image() {
  local aws_account_id="$1"
  local image_name="$2"

  docker tag "$image_name":latest "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com/"$image_name":latest

  echo "===>Pushing docker image to ecr..."
  docker push "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com/"$image_name":latest
}

function build_image() {
  local image_name=$1
  local app_env=$2

  echo "===>Building docker image: app_env=$app_env, image_name=$image_name"
  docker build --build-arg APP_ENV="$app_env" -t "$image_name" ../backend
}

function authenticate_docker_to_ecr() {
  local aws_account_id=$1

  echo "===>Authenticating Docker to ECR"
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com
}

function main() {
  local profile
  profile=$1

  if [ -z "$profile" ] || [ "$profile" == "null" ]; then
    profile="default"
  fi

  local aws_account_id
  aws_account_id=$(aws sts get-caller-identity --query 'Account' --output text --profile $profile)
  aws_account_id=$(unquote $aws_account_id)

  local image_name="team8-backend"
  local repository_name="team8-backend"
  local app_env="production"

  build_image "$image_name" "$app_env"
  authenticate_docker_to_ecr "$aws_account_id"

  create_image_repository "$image_name"
#  publish_image "$aws_account_id" "$image_name"

  cdk deploy --profile $profile "$@"
  exit $?
}

main "$@"
