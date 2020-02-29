# -*- coding: utf-8 -*-

def find_ingr(arr, name):
    for i in range(len(arr)):
        if name == arr[i][0]:
            return i
    return -1