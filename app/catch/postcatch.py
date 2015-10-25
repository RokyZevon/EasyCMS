# coding=utf-8

from ..models import Post, Postmeta, Postlabel, Page
from .usercatch import get_user_by_id
from .metacatch import get_meta_by_id
import random

# 以ID获取文章
def getPostById(postId):
    postinfo = {}
    post = Post.query.filter_by(post_id=postId).first()
    return post

# 获取全部文章
def get_all_posts(page=1,num=5,type='ALL'):

    list = {}
    postlist = Post.query.all()

    for post in postlist:
        tmp = {}
        tmp['id'] = post.post_id
        tmp['title'] = post.post_title
        tmp['auther'] = get_user_by_id(post.user_id).user_nicename
        tmp['meta'] = post.post_meta
        tmp['label'] = ''
        tmp['talk'] = ''
        tmp['datatime'] = ''
        tmp['status'] = ''

        list.append(tmp)

    return list

# 获取某人文章
def getPostsByUserId(userId):

    post = Post.query.filter_by(user_id=userId).first()
    return post

# 获取某个分类文章
def getPostsByMetaId(metaId):

    postMetaList = Postmeta.query.filter_by(meta_id=metaId).all()
    postList = []
    for postMeta in postMetaList:
        postList.append(getPostById(postMeta.post_id))

    return postList

# 获取某个标签文章
def getPostsByLabelId(labelId):

    postLabelList = Postlabel.query.filter_by(label_id=labelId).all()
    postList = []
    for postLabel in postLabelList:
        postList.append(getPostById(postLabel.post_id))

    return postList

# 随机获得文章
def getPostsRand():

    postList = Post.query.all()
    random.shuffle(postList)

    return postList

# 相关文章推荐（猜你喜欢）
def maybeYouLike(postId):

    postLabelList = Postlabel.query.filter_by(post_id=postId).all()
    postList = []

    # 获得同标签的文章列表
    for postLabel in postLabelList:
        if postLabel.post_id is not postId:
            postList.append(getPostById(postLabel.post_id))

    return postList

# 以ID获取页面
def getPageById(postId):

    postinfo = {}
    post = Page.query.filter_by(post_id=postId).first()
    return post

# 获取全部页面
def getAllPages():

    postlist = {}
    postList = Page.query.all()
    return postList

# 获取某人发表的页面
def getPagesByUserId(userId):

    post = Page.query.filter_by(user_id=userId).first()
    return post
