from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

task_params = [
    openapi.Parameter(
        'experiment',
        openapi.IN_QUERY,
        description='Retrieve tasks within the experiment ID.',
        type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        'status',
        openapi.IN_QUERY,
        description='Retrieve tasks within the status.',
        type=openapi.TYPE_STRING
    )
]

search_params = [
    openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description='This is a keyword for searching resources.',
        type=openapi.TYPE_STRING
    )
]

file_path_params = [
    openapi.Parameter(
        'file_path',
        openapi.IN_PATH,
        description='The path to retrieve files. (ex: /, /models, /datasets ..)',
        type=openapi.TYPE_STRING,
        default='/'
    )
]

# ------------------
# model schemas
# ------------------
delete_model_files = swagger_auto_schema(
    operation_id='model_files_delete',
    operation_description="List files.",
    manual_parameters=file_path_params
)

retrieve_model_files = swagger_auto_schema(
    operation_id='model_files_read',
    operation_description="List files.",
    manual_parameters=file_path_params
)

# --------------------
# dataset schemas
# --------------------
delete_dataset_files = swagger_auto_schema(
    operation_id='dataset_files_delete',
    operation_description="List files.",
    manual_parameters=file_path_params
)

retrieve_dataset_files = swagger_auto_schema(
    operation_id='dataset_files_read',
    operation_description="List files.",
    manual_parameters=file_path_params
)

# --------------------
# task schemas
# --------------------
list_tasks = swagger_auto_schema(
    manual_parameters=task_params+search_params
)

# --------------------
# common schemas
# --------------------
list_resources = swagger_auto_schema(
    operation_description="List resources.",
    manual_parameters=search_params
)

retrieve_resource = swagger_auto_schema(
    operation_description="Retrieve resource details."
)
