function unquote(){
  echo "$1" | tr -d '"'
}

function create_image_repository(){
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

function publish_image(){
  local aws_account_id="$1"
  local image_name="$2"

  docker tag "$image_name":latest "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com/"$image_name":latest

  echo "===>Pushing docker image to ecr..."
  docker push "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com/"$image_name":latest
}

function build_image(){
  local image_name=$1
  local app_env=$2

  echo "===>Building docker image: app_env=$app_env, image_name=$image_name"
  docker build --build-arg APP_ENV="$app_env" -t "$image_name" .
}

function authenticate_docker_to_ecr(){
  local aws_account_id=$1

  echo "===>Authenticating Docker to ECR"
  aws ecr get-login-password --region us-east-1 | \
   docker login --username AWS --password-stdin "$aws_account_id".dkr.ecr.us-east-1.amazonaws.com
}


function create_lambda_function(){

  local aws_account_id=$1
  local image_name=$2
  local function_name=$3

  local role_name="Team8FunctionExecutionRole"

  local image_uri="$aws_account_id".dkr.ecr.us-east-1.amazonaws.com/"$image_name":latest

  # Create role for the function
  local existing_role
  existing_role=$(aws iam get-role --role-name "$role_name")

  if [ -z "$existing_role" ] || [ "$existing_role" == "null" ];
  then
    echo "===>Creating role lambda role: $role_name"
    result=$(aws iam create-role --role-name "$role_name" \
     --assume-role-policy-document \
     '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}')

    echo "$result"
  else
    echo "===>Role $role_name already exists. Skipping role creation"
  fi

  # Attach policy to the created role
  aws iam attach-role-policy --role-name "$role_name" --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  local existing_function
  existing_function=$(aws lambda list-functions --query "(Functions[?FunctionName=='$function_name'])[0]")

  echo "$existing_function"

  if [ -z "$existing_function" ] || [ "$existing_function" == "null" ];
  then
    echo "===>Creating lambda function.."
    result=$(aws lambda create-function --region us-east-1 --function-name "$function_name" \
      --package-type Image  \
      --code ImageUri="$image_uri"   \
      --role arn:aws:iam::"$aws_account_id":role/"$role_name")
    echo "$result"
  else
    echo "===>Function already exists, updating image instead.."
#    result=$(aws lambda update-function-code \
#    --function-name  "$function_name" \
#    --image-uri "$image_uri")
#    echo "$result"
  fi
}

function create_api_gateway(){
  local aws_account_id=$1
  local function_name=$2
  local gateway_name=$3

  local existing_rest_api_id
  existing_rest_api_id=$(aws apigateway get-rest-apis --query "(items[?name=='$gateway_name'].id)[0]")

  local rest_api_id

  if [ -z "$existing_rest_api_id" ] || [ "$existing_rest_api_id" == "null" ];
  then
    echo "===>Creating api gateway"
    rest_api_id=$(aws apigateway create-rest-api --name "$gateway_name" --description 'The Team 8 REST API' --query "id")
    echo "Created API Gateway Id: $rest_api_id"
  else
    echo "===>Found existing api gateway"
    rest_api_id=$existing_rest_api_id
    echo "Existing API Gateway Id: $rest_api_id"
  fi

  rest_api_id=$(unquote "$rest_api_id")

  echo "Rest api id: $rest_api_id"
  local root_resource_id


  root_resource_id=$(aws apigateway get-resources --rest-api-id $rest_api_id --query "(items[?path=='/'].id)[0]")
  root_resource_id=$(unquote "$root_resource_id")


  if [ -z "$root_resource_id" ] || [ "$root_resource_id" == "null" ];
  then
    echo "===>Missing root resource id"
    exit 1
  fi


  local root_resource_any_method

  root_resource_any_method=$(aws apigateway get-method --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method ANY)

  if [ -z "$root_resource_any_method" ] || [ "$root_resource_any_method" == "null" ];
  then
    echo "No ANY method on root resource. Will create one"
  else
    echo "Removing existing ANY method on root resource"
    result=$(aws apigateway delete-method --rest-api-id $rest_api_id --resource-id $root_resource_id --http-method ANY)
    echo "$result"
  fi

  echo "===>Creating root resource ANY method"
   result=$(aws apigateway put-method --rest-api-id "$rest_api_id" \
     --resource-id $root_resource_id \
     --http-method ANY \
     --authorization-type "NONE" \
     --no-api-key-required)
   echo "$result"

  echo "===>Creating root resource ANY method Lambda integration request"
  result=$(aws apigateway put-integration --rest-api-id $rest_api_id \
   --resource-id $root_resource_id --http-method ANY --type AWS_PROXY \
   --integration-http-method POST \
   --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:$aws_account_id:function:$function_name/invocations")
  echo "$result"

   echo "===> Creating root resource ANY method response"
   result=$(aws apigateway put-method-response --rest-api-id $rest_api_id \
     --resource-id "$root_resource_id" --http-method ANY \
     --status-code 200 \
     --response-models "application/json=Empty")
   echo "$result"


  # Doing the same thing as above but for the proxy method :)

  local proxy_resource_id
  proxy_resource_id=$(aws apigateway get-resources --rest-api-id $rest_api_id --query "(items[?path=='/{proxy+}'].id)[0]")
  proxy_resource_id=$(unquote "$proxy_resource_id")

  if [ -z "$proxy_resource_id" ] || [ "$proxy_resource_id" == "null" ];
  then
    echo "===>Creating proxy resource id"
    proxy_resource_id=$(aws apigateway create-resource --rest-api-id $rest_api_id --parent-id "$root_resource_id" --path-part '{proxy+}' --query "id" )
    proxy_resource_id=$(unquote "$proxy_resource_id")
  fi

  local proxy_resource_any_method
  proxy_resource_any_method=$(aws apigateway get-method --rest-api-id $rest_api_id --resource-id $proxy_resource_id --http-method ANY)

  if [ -z "$proxy_resource_any_method" ] || [ "$proxy_resource_any_method" == "null" ];
  then
    echo "No ANY method on proxy resource. Will create one"
  else
    echo "Removing existing ANY method on proxy resource"
    result=$(aws apigateway delete-method --rest-api-id $rest_api_id --resource-id $proxy_resource_id --http-method ANY)
    echo "$result"
  fi


  echo "===>Creating proxy resource ANY method"
  result=$(aws apigateway put-method --rest-api-id $rest_api_id \
     --resource-id $proxy_resource_id \
     --http-method ANY \
     --authorization-type "NONE" \
     --no-api-key-required)
  echo "$result"

  echo "===>Creating proxy resource ANY method Lambda integration request"
  result=$(aws apigateway put-integration --rest-api-id $rest_api_id \
   --resource-id $proxy_resource_id --http-method ANY --type AWS_PROXY \
   --integration-http-method POST \
   --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:$aws_account_id:function:$function_name/invocations")
  echo "$result"

   echo "===>Creating proxy resource ANY method response"
   result=$(aws apigateway put-method-response --rest-api-id $rest_api_id \
     --resource-id $proxy_resource_id --http-method ANY \
     --status-code 200 \
     --response-models "application/json=Empty")
   echo "$result"


   echo "===>Creating API deployment"
   result=$(aws apigateway create-deployment --rest-api-id $rest_api_id --stage-name dev --description "Created from CLI")
   echo "$result"
}

# rest-api-id: 6vf57iccme
# root-resource-id: qpjry3poug

function main(){
  local aws_account_id="$1"
  local image_name="team8-backend"
  local repository_name="team8-backend"
  local function_name="Team8Function"
  local gateway_name="Team8RestApi"
  local app_env="production"

  if [ -z "$aws_account_id" ] || [ "$aws_account_id" == "null" ]; then
    read -r -p 'Enter the AWS Account Id you would like to deploy to: ' aws_account_id
  fi

  build_image "$image_name" "$app_env"
  authenticate_docker_to_ecr "$aws_account_id"
  create_image_repository "$image_name"
#  publish_image "$aws_account_id" "$image_name"

  create_lambda_function "$aws_account_id" "$image_name" "$function_name"
  create_api_gateway "$aws_account_id" "$function_name" "$gateway_name"
}


main "$@"