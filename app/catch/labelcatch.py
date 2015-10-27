# coding=utf-8

from ..models import Label, Postlabel
from .postcatch import get_posts_by_label_id


# 获得全部标签
def get_all_label(page=1, num=5):

    if page == 0:
        labelList = Label.query.all()
        return labelList

    pagination = Label.query.paginate(
        page, per_page=num
    )
    return pagination


# 根据标签ID获得标签
def get_label_by_id(labelid):

    label = Label.query.filter_by(label_id=labelid).first()

    return label

# 根据标签缩写获得标签
def getLabelBySlug(slug):

    label = Label.query.filter_by(label_slug=slug).first()

    return label

# 根据标签缩写获得标签
def getLabelByName(name):

    label = Label.query.filter_by(label_name=name).first()

    return label

# 获得文章的全部标签
def getPostLabels(postId):

    labelList = Postlabel.query.filter_by(post_id=postId).all()

    return labelList

# 获得带文章数的标签（根据标签文章数，可做标签云）
def getLabelOrder():

    labelList = get_all_label()

    list = []

    for label in labelList:
        list.append({'label': label, 'num': len(get_posts_by_label_id(label.label_id))})

    return list


