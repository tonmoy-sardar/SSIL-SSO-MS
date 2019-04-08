from django.conf import settings
#::::::::::: RESPONSE MODIFY DECORATOR FOR COMMON :::::::::::#
def response_modify_decorator(func):
    def inner(self, request, *args, **kwargs):
        #print("model", self.__module__)
        response = super(self.__class__, self).list(request, args, kwargs)
        #print("before Execution")
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
        # getting the returned value
        func(self, request, *args, **kwargs)
        #print("after Execution")
        # returning the value to the original frame
    return inner
#::::::::::: RESPONSE MODIFY DECORATOR FOR COMMON :::::::::::#