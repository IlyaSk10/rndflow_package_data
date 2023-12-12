from pydantic_settings import BaseSettings
from typing import Optional, Union


class Settings(BaseSettings):
    api_server: Optional[str] = ""
    refresh_token: str = ""
    common_conn_retry_total: int = 5
    common_conn_retry_read: int = 5
    common_conn_retry_connect: int = 5
    common_conn_retry_redirect: int = 5
    common_conn_retry_status: int = 5
    common_conn_retry_other: int = 5
    common_conn_retry_backoff_factor: float = 0.3
    common_conn_timeout: Union[int, float] = 300

    spec_conn_retry_total: int = 10
    spec_conn_retry_read: int = 0
    spec_conn_retry_connect: int = 10
    spec_conn_retry_redirect: int = 5
    spec_conn_retry_status: int = 10
    spec_conn_retry_other: int = 0
    spec_conn_retry_backoff_factor: float = 0.1
    spec_conn_timeout: Union[int, float] = 300000
