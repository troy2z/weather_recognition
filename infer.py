# -*- coding:utf-8 -*-

import os
import time
import random
import cv2
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.utils.data.sampler import RandomSampler
from torch.utils.data import DataLoader, SequentialSampler
from torch.optim.lr_scheduler import CosineAnnealingLR

from qdnet.conf.config import load_yaml
from qdnet.optimizer.optimizer import GradualWarmupSchedulerV2
from qdnet.dataset.dataset import get_df, QDDataset
from qdnet.dataaug.dataaug import get_transforms
from qdnet.models.effnet import Effnet
from qdnet.models.resnest import Resnest
from qdnet.models.se_resnext import SeResnext
from qdnet.conf.constant import Constant

device = torch.device('cpu')

parser = argparse.ArgumentParser(description='Hyperparams')
parser.add_argument('--config_path', default="./conf/effb3_ns.yaml", help='config file path')
parser.add_argument('--img_path', help='config file path')
parser.add_argument('--fold', default="0", help='config file path')
args = parser.parse_args()
config = load_yaml(args.config_path, args)

classmaps = pd.read_json(config["class_mapping"], orient="index", typ="series", encoding="utf-8")


class QDNetModel():

    def __init__(self, config, fold):

        if config["enet_type"] in Constant.GEFFNET_LIST:
            ModelClass = Effnet
        else:
            raise NotImplementedError()

        model_file = ''
        if config["eval"] == 'best':
            model_file = os.path.join(config["model_dir"], f'best_fold{fold}.pth')
        if config["eval"] == 'final':
            model_file = os.path.join(config["model_dir"], f'final_fold{fold}.pth')
        self.model = ModelClass(
            enet_type=config["enet_type"],
            out_dim=int(config["out_dim"]),
            drop_nums=int(config["drop_nums"]),
            metric_strategy=config["metric_strategy"]
        )
        self.model = self.model.to(device)

        try:  # single GPU model_file
            self.model.load_state_dict(torch.load(model_file), strict=True)
        except:  # multi GPU model_file
            state_dict = torch.load(model_file)
            state_dict = {k[7:] if k.startswith('module.') else k: state_dict[k] for k in state_dict.keys()}
            self.model.load_state_dict(state_dict, strict=True)
        self.model.eval()

        _, self.transforms_val = get_transforms(config["image_size"])

    def predict(self, data):
        if os.path.isfile(data):
            image = cv2.imread(data)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        res = self.transforms_val(image=image)
        image = res['image'].astype(np.float32)

        image = image.transpose(2, 0, 1)
        data = torch.tensor([image]).float()
        probs = self.model(data.to(device))
        probs = F.softmax(probs, dim=1)
        probs = probs.cpu().detach().numpy()
        # return probs.argmax(1)
        return self.predictResult(probs[0])

    def predictResult(self, probs):
        prelist = []
        for index in range(int(config["out_dim"])):
            prelist.append({
                'weather': classmaps[index],
                'score': str(probs[index])
            })

        prelist_sort = sorted(prelist, key=lambda x: x['score'], reverse=True)
        print('predictResult=', prelist_sort)

        return prelist_sort


if __name__ == '__main__':
    qd_model = QDNetModel(config, args.fold)
    pre = qd_model.predict(args.img_path)
    print("predict -->", pre)
