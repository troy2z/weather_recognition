# 灾害天气图像识别

## CV 训练/测试/部署分类任务

|      ***       |   具体     |    样例   |
| :-----------------: | :---------:| :---------:|
|  模型方面  |   (efficientnet等)       |  [1](./qdnet/conf/constant.py)  |
|  metric方面  |   (Swish/ArcMarginProduct_subcenter/ArcFaceLossAdaptiveMargin等)       |  [2](./qdnet/models/metric_strategy.py)  |
|  数据增强  |   (旋转/镜像/对比度等、mixup/cutmix)         |  [3](./qdnet/dataaug/) |
|  损失函数  |   (ce_loss/ce_smothing_loss/focal_loss/bce_loss等)                     |  [4](./qdnet/loss/)    |


## 支持的全部模型：

> GEFFNET_LIST = ['efficientnet_b0', 'efficientnet_b1', 'efficientnet_b2',  'efficientnet_b3', 'efficientnet_b4', 'efficientnet_b5', 'efficientnet_b6', 'efficientnet_b7', 'efficientnet_b8', 'efficientnet_l2', 'efficientnet_es', 'efficientnet_em', 'efficientnet_el', 'efficientnet_cc_b0_4e', 'efficientnet_cc_b0_8e', 'efficientnet_cc_b1_8e', 'efficientnet_lite0', 'efficientnet_lite1', 'efficientnet_lite2', 'efficientnet_lite3', 'efficientnet_lite4', 'tf_efficientnet_b0', 'tf_efficientnet_b1', 'tf_efficientnet_b2', 'tf_efficientnet_b3', 'tf_efficientnet_b4', 'tf_efficientnet_b5', 'tf_efficientnet_b6', 'tf_efficientnet_b7', 'tf_efficientnet_b8', 'tf_efficientnet_b0_ap', 'tf_efficientnet_b1_ap', 'tf_efficientnet_b2_ap', 'tf_efficientnet_b3_ap', 'tf_efficientnet_b4_ap', 'tf_efficientnet_b5_ap', 'tf_efficientnet_b6_ap', 'tf_efficientnet_b7_ap', 'tf_efficientnet_b8_ap', 'tf_efficientnet_b0_ns', 'tf_efficientnet_b1_ns', 'tf_efficientnet_b2_ns', 'tf_efficientnet_b3_ns', 'tf_efficientnet_b4_ns', 'tf_efficientnet_b5_ns', 'tf_efficientnet_b6_ns', 'tf_efficientnet_b7_ns', 'tf_efficientnet_l2_ns', 'tf_efficientnet_l2_ns_475', 'tf_efficientnet_es', 'tf_efficientnet_em', 'tf_efficientnet_el', 'tf_efficientnet_cc_b0_4e', 'tf_efficientnet_cc_b0_8e', 'tf_efficientnet_cc_b1_8e', 'tf_efficientnet_lite0', 'tf_efficientnet_lite1', 'tf_efficientnet_lite2', 'tf_efficientnet_lite3', 'tf_efficientnet_lite4']

### 预模型下载：
> https://github.com/huggingface/pytorch-image-models 

## 数据集准备
```
1、灾害天气图片样本：data/img
2、灾害天气分类映射：data/class_maps.json
```

## 训练/测试/部署流程：
0、转为训练需要的数据格式
```
python tools/data_preprocess.py --data_dir "./data/data.csv" --n_splits 5 --output_dir "./data/train.csv" --random_state 2020
```

1、修改配置文件，选择需要的模型 以及 模型参数：vi conf/test.yaml
```
cp conf/test.yaml conf/effb3_ns.yaml
vim conf/effb3_ns.yaml
```

2、训练模型: （根据需求选取合适的模型） 
```
python train.py --config_path "conf/effb3_ns.yaml"
```

3、测试
```
python test.py --config_path "conf/effb3_ns.yaml" --n_splits 5
```

4、推理
```
python infer.py --config_path "conf/effb3_ns.yaml" --img_path "./data/img/rainstorm/01.jpg" --fold "0"
predict --> [{'weather': '暴雨', 'score': '0.53469974'}, {'weather': '雪害', 'score': '0.30571106'}, {'weather': '风害', 'score': '0.112732135'}, {'weather': '浓雾', 'score': '0.046857048'}]

python infer.py --config_path "conf/effb3_ns.yaml" --img_path "./data/img/waterlogging/02.jpg" --fold "1"
predict --> [{'weather': '风害', 'score': '0.5515153'}, {'weather': '浓雾', 'score': '0.19872001'}, {'weather': '雪害', 'score': '0.13002536'}, {'weather': '暴雨', 'score': '0.11973937'}]
```


## 服务部署
1、启动服务
```
python main.py

服务配置见conf/app.conf
```
2、服务接口
```
1、图片上传识别接口：/api/v1/uploadinfer，通过此接口上传图片并返回识别结果
2、灾害天气识别接口：/api/v1/infer，通过此接口远程识别远程图片并返回识别结果
```


## 气象灾害有20余种,主要有以下种类：
```
（0）暴雨-rainstorm：山洪暴发、河水泛滥、城市积水；
（1）雨涝-waterlogging：内涝、渍水；
（2）干旱-aridity：农业、林业、草原的旱灾,工业、城市、农村缺水；
（3）干热风-hotwind：干旱风、焚风；
（4）高温、热浪-hotwave：酷暑高温、人体疾病、灼伤、作物逼熟；
（5）热带气旋-tropical-cyclone：狂风、暴雨、洪水；
（6）冷害-colddamage：由于强降温和气温低造成作物、牲畜、果树受害；
（7）冻害-frost：霜冻,作物、牲畜冻害,水管、油管冻坏；
（8）冻雨-sleet：电线、树枝、路面结冰；
（9）结冰-frozen：河面、湖面、海面封冻,雨雪后路面结冰；
（10）雪害-snowstorm：暴风雪、积雪；
（11）雹害-hail：毁坏庄稼、破坏房屋、冰雹；
（12）风害-typhoon：倒树、倒房、翻车、翻船；
（13）龙卷风-tornado：局部毁灭性灾害；
（14）雷电-thunder：雷击伤亡；
（15）连阴雨（梅雨）-plumrains：对作物生长发育不利、粮食霉变等；
（16）浓雾-smog：人体疾病、交通受阻；
（17）低空风切变：（飞机）航空失事；
（18）酸雨-acidrain：作物等受害.`
```

## 常见问题
1、安装apex:
```
git clone https://www.github.com/nvidia/apex
cd apex
python setup.py install
```

2、ImportError: cannot import name 'container_abcs' from 'torch._six'
```
修改apex-0.1-py3.7.egg\apex\amp\_amp_state.py：
修改前：
if TORCH_MAJOR == 0:
    import collections.abc as container_abcs
else:
    from torch._six import container_abcs
    
修改后：
if TORCH_MAJOR == 1:
    import collections.abc as container_abcs
else:
    from torch._six import container_abcs
```

## 服务与支持
### 承接数据采集业务（手机微信同号:18172360816）
![](./images/wxpay.png)
