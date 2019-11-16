import os,sys
import pandas as pd
import json
import numpy as np
#读入之前获取的sorted rules
sorted_confidence=np.load("sorted_confidence.npy")
#d读入validation set
validate_folder="E:/pycharm/cs145project/data"

validate_filename = validate_folder+'/val_ratings_binary.csv'

validate = pd.read_csv(validate_filename)
#print(validate)
#读入原文件并存储进入favorable_reviews_by_users
#original_filename = validate_folder+"/train_ratings_binary.csv"
original_filename = validate_folder+"/train_ratings_binary.csv"

original = pd.read_csv(original_filename)

favorable_reviews_by_users = dict((k, frozenset(v.values)) for k,v in original.groupby("userId")["movieId"])

correct=0
total=0
print("start")

for index, row in validate.iterrows():
    #cnt标记prediction total为总数
    cnt=0

    total+=1
    for rules,confidence in sorted_confidence:
        #遍历已获取的规则，如果conclusion与当前需判断的电影相同，则判断premise是否在用户已经看过的电影中
        if rules[1]==row["movieId"]:
            if rules[0].issubset(favorable_reviews_by_users[row["userId"]]):
                cnt=1
    #如果不符合任何conclusion以及premise，暂时产生0，1随机数
    if(cnt==0):
        cnt=np.random.randint(0, 1)
    #与真实rating比对
    if cnt==row["rating"]:
        correct+=1
        #每出现100个正确的输出此时准确率
        if(correct%100==0):
            print(correct/total)