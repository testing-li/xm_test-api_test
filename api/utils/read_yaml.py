#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from api.utils import getDir


def read_yaml(path):
    path = f'{getDir.proDir}{path}'
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f.read())


def write_yaml(data, path):
    path = f'{getDir.proDir}{path}'
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f)


def rewirte_yaml(path, data: dict):
    doc = read_yaml(path)
    for i in data.keys():
        for k, v in data[i].items():
            doc[i][k] = v
    with open(f'{getDir.proDir}{path}', 'w', encoding='utf-8') as f:
        yaml.safe_dump(doc, f)


if __name__ == '__main__':
    # data = read_yaml('/data/open_user_group.yaml')
    # print(data)
    import api.utils.method as method

    date1 = method.generate_group_organization(3, 2, 2)
    date2 = method.generate_group_organization(3, 2, 2)
    data = [date1, date2]

    write_yaml(data, "/data/open_user_group.yaml")
    # key = data['success']['individual']['members']['params']
    # rs = []
    # for i in data['success']['individual']['members']['value']:
    #     case = []
    #     for j in i:
    #         s = dict(zip(key, j))
    #         case.append(s)
    #     rs.append(case)
    # print(rs)
