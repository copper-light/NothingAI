from rest_framework.routers import BaseRouter, Route, DynamicRoute, SimpleRouter


class FileRouter(SimpleRouter):

    routes = [
        # Detail route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'post': 'create',
                'patch': 'partial_update'
                # 'put': 'update',
                # 'patch': 'partial_update',
                # 'delete': 'destroy'
            },
            name='{basename}',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),

        Route(
            url=r'^{prefix}/(?P<file_path>.*){trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),

        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        # DynamicRoute(
        #     url=r'^{prefix}/{url_path}{trailing_slash}$',
        #     name='{basename}-{url_name}',
        #
        #     detail=True,
        #     initkwargs={}
        # ),
    ]
