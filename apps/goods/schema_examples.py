from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

PRODUCT_PARAM_EXAMPLE = [
    OpenApiParameter(
        name="title",
        description="Search products by title",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="max_price",
        description="Get products with price lte max_price",
        required=False,
        type=OpenApiTypes.INT,
    ),
    OpenApiParameter(
        name="min_price",
        description="Get products with price gte min_price",
        required=False,
        type=OpenApiTypes.INT,
    ),
]
