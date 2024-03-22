from rest_framework.routers import BaseRouter, Route, DynamicRoute, SimpleRouter


class FileRouter(SimpleRouter):

    file_routes = [
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}/files{trailing_slash}$',
            mapping={
                # 'get': 'retrieve_file',
                'post': 'create_file',
                'patch': 'create_file'
            },
            name='{basename}',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),

        Route(
            url=r'^{prefix}/{lookup}/files/(?P<file_path>.*){trailing_slash}$',
            mapping={
                'get': 'retrieve_file',
                'delete': 'remove_file'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        )
    ]

    routes = SimpleRouter.routes + file_routes
