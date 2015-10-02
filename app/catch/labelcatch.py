# coding=utf-8

from ..models import Label, Postlabel
from .postcatch import getPostsByLabelId

# 获得全部标签
def getAllLabel():

    labelList = Label.query.all()
    
    return labelList

# 根据标签ID获得标签
def getLabelById(labelId):

    label = Label.query.filter_by(label_id=labelId).first()

    return label

# 根据标签缩写获得标签
def getLabelBySlug(slug):

    label = Label.query.filter_by(label_slug=slug).first()

    return label

# 获得文章的全部标签
def getPostLabels(postId):

    labelList = Postlabel.query.filter_by(post_id=postId).all()

    return labelList

# 获得带文章数的标签（根据标签文章数，可做标签云）
def getLabelOrder():

    labelList = getAllLabel()

    list = []

    for label in labelList:
        list.append({'label': label, 'num': len(getPostsByLabelId(label.label_id))})

    return list


