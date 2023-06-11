from address import inrange
import utils


def split_params(string):
    endpoint_list = string.split("-")
    params = []
    for endpoint in endpoint_list:
        params.append(endpoint.split(maxsplit=4))
    return params


def check_equal_list(list1, list2):
    if len(list1) != len(list2):
        return False
    for x in range(len(list1)):
        if not (list1[x].address_.ip == list2[x].address_.ip):
            return False
        if not (list1[x].address_.port == list2[x].address_.port):
            return False
    return True


def check_apis_inrange(data_json, node_id, id_pred):
    for key in data_json.keys():
        api_id = utils.hash(key)
        if not inrange(api_id, node_id, id_pred):
            data_json.pop(key)
    # testear


# def list_to_string(list):
#     print(list)
#     result = ""
#     for x in list:
#         for lis_string in x:
#             result += lis_string + " "
#         result += "-"
#     result = result[: len(result) - 1]
#     print(result, "*****************")
#     return result
