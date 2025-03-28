from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

SHOP_PARAM_EXAMPLE = [
    OpenApiParameter(
        name="title",
        description="Filtering shops by title",
        required=False,
        type=OpenApiTypes.STR,
    )
]
