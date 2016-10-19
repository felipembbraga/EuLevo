from rest_framework.response import Response


def retreive_only_owner(func):
    def check_accepts():
        def new_f(self, request, *args, **kwds):
            instance = self.get_object()
            raise Exception(instance)
            if not hasattr(instance, 'user'):
                raise Exception('Object has not user field')
            if instance.user.pk != request.user.pk:
                return Response({'error': 'User is not owner to do this'})
            return func(self, request, *args, **kwds)
        new_f.func_name = func.func_name
        return new_f
    return check_accepts