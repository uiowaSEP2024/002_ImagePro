from typing import Optional

from pydantic import BaseModel


class BuildConfig(BaseModel):
    AppEnv: str
    ApiGatewayStage: str
    AppName: str
    JwtAlgorithm: str

    RepositoryName: str
    RepositoryOwner: str
    AmplifyMonoRepoAppRoot: str

    GitHubAccessTokenSecretName: str

    DatabaseAccessSecretName: str
    DatabaseName: Optional[str]

    SecretKeySecretName: str
