def split_params(string):
    endpoint_list = string.split("-")
    params = []
    for endpoint in endpoint_list:
        params.append(endpoint.split(maxsplit=4))
    return params
