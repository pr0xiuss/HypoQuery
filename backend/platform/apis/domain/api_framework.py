from enum import Enum


class ApiFramework(
    str,
    Enum,
):
    FASTAPI = "FASTAPI"
    DJANGO = "DJANGO"
    FLASK = "FLASK"
    EXPRESS = "EXPRESS"
    SPRING_BOOT = "SPRING_BOOT"
    ASP_NET = "ASP_NET"
    GO = "GO"
    LARAVEL = "LARAVEL"
    OTHER = "OTHER"