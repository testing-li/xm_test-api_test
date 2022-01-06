# -*- coding: utf-8 -*-
from api.core.utils import request
from api.core.utils.api_yaml import get_api
import sys


class Folders:
    def get_folders(self, token=None):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        return request.get(api, token=token)

    def put_folders(self, foldersList: list, token=None):
        api = get_api(f'$..{sys._getframe().f_code.co_name}')
        payload = {
            "foldersList": foldersList
        }
        return request.put(api, payload=payload, token=token)


