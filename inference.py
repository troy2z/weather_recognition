# -*- coding:utf-8 -*-

import argparse
from flask_restful import Resource, Api
from infer import QDNetModel
from qdnet.conf.config import load_yaml

parser = argparse.ArgumentParser(description='Hyperparams')
parser.add_argument('--config_path', default="./conf/effb3_ns.yaml", help='config file path')
parser.add_argument('--fold', default="4", help='config file path')
args = parser.parse_args()
config = load_yaml(args.config_path, args)

qdnet_model = QDNetModel(config, args.fold)

def predict(imgfile):
    return qdnet_model.predict(imgfile)
