import importlib


def create(module_name, class_name):

    module = importlib.import_module(module_name)
    cls_inst = getattr(module, class_name)
    return cls_inst