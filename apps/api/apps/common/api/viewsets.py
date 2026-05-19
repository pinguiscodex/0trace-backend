from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class EnvelopeMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if (
            isinstance(response, Response)
            and response.status_code != 204
            and response.data is not None
            and not response.exception
            and not (isinstance(response.data, dict) and ("data" in response.data or "error" in response.data))
        ):
            response.data = {"data": response.data}
        return response


class EnvelopeModelViewSet(EnvelopeMixin, ModelViewSet):
    pass


class EnvelopeReadOnlyModelViewSet(EnvelopeMixin, ReadOnlyModelViewSet):
    pass

