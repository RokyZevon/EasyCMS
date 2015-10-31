# coding=utf-8
from app import db

from ..models import Post, Postlabel, Page, PostStatus
from .usercatch import get_user_by_id
from .metacatch import get_meta_by_id
import random


# 以ID获取文章
def get_post_by_id(postid):
    post = Post.query.filter_by(post_id=postid).first()
    return post


# 获取全部文章
def get_all_posts(page=1, num=5, type=0, userid=0):

    list = []
    postlist = 0
    if type == 0:
        postlist = Post.query.order_by(Post.post_date.desc()).filter(Post.post_status>PostStatus['DELETED'])
    elif type == 1:
        postlist = Post.query.order_by(Post.post_date.desc()).filter(Post.post_status>=PostStatus['RELEASED'])
    elif type == 2:
        postlist = Post.query.order_by(Post.post_date.desc()).filter(Post.post_status>=PostStatus['UNAUDITED'], Post.post_status<=PostStatus['DRAFT'])
    elif type == 3:
        postlist = Post.query.order_by(Post.post_date.desc()).filter_by(post_status=PostStatus['DELETED'])

    if userid != 0:
        postlist = postlist.filter_by(user_id=userid)

    postlist = postlist.paginate(
        page, per_page=num
    )

    rnt = {'pagination': postlist}
    postlist = postlist.items

    for post in postlist:
        tmp = {}
        tmp['id'] = post.post_id
        tmp['title'] = post.post_title
        tmp['userid'] = post.user_id
        tmp['auther'] = get_user_by_id(post.user_id).user_nicename
        tmp['metaid'] = post.post_meta
        tmp['meta'] = get_meta_by_id(post.post_meta).meta_name
        tmp['talk'] = 0
        tmp['datatime'] = post.post_date.strftime("%Y-%m-%d %H:%M:%S")

        if post.post_status == PostStatus['RELEASED']:
            tmp['status'] = u'已发布'
        elif post.post_status == PostStatus['DRAFT']:
            tmp['status'] = u'草稿'
        elif post.post_status == PostStatus['OVERHEAD']:
            tmp['status'] = u'置顶'
        elif post.post_status == PostStatus['DELETED']:
            tmp['status'] = u'回收站'
        elif post.post_status == PostStatus['UNAUDITED']:
            tmp['status'] = u'未审核'
        elif post.post_status == PostStatus['PRIVATE']:
            tmp['status'] = u'私有'
        else:
            tmp['status'] = u'ERROR'

        list.append(tmp)

    rnt['list'] = list

    return rnt

# 获取某人文章
def get_posts_by_user_id(page=1, num=5, type=0, userid=0):

    list = []
    postlist = Post.query.order_by(Post.post_date.desc()).filter_by(user_id=userid)

    if type == 0:
        postlist = postlist.filter(Post.post_status>=PostStatus['DELETED'])
    elif type == 1:
        postlist = postlist.filter(Post.post_status>=PostStatus['RELEASED'])
    elif type == 2:
        postlist = postlist.filter(Post.post_status>=PostStatus['UNAUDITED'], Post.post_status<=PostStatus['DRAFT'])
    elif type == 3:
        postlist = postlist.filter_by(post_status=PostStatus['DELETED'])

    postlist = postlist.paginate(
        page, per_page=num
    )

    rnt = {'pagination': postlist}
    postlist = postlist.items

    for post in postlist:
        tmp = {}
        tmp['id'] = post.post_id
        tmp['title'] = post.post_title
        tmp['userid'] = post.user_id
        tmp['auther'] = get_user_by_id(post.user_id).user_nicename
        tmp['metaid'] = post.post_meta
        tmp['meta'] = get_meta_by_id(post.post_meta).meta_name
        tmp['talk'] = 0
        tmp['datatime'] = post.post_date.strftime("%Y-%m-%d %H:%M:%S")

        if post.post_status == PostStatus['RELEASED']:
            tmp['status'] = u'已发布'
        elif post.post_status == PostStatus['DRAFT']:
            tmp['status'] = u'草稿'
        elif post.post_status == PostStatus['OVERHEAD']:
            tmp['status'] = u'置顶'
        elif post.post_status == PostStatus['DELETED']:
            tmp['status'] = u'回收站'
        elif post.post_status == PostStatus['UNAUDITED']:
            tmp['status'] = u'未审核'
        elif post.post_status == PostStatus['PRIVATE']:
            tmp['status'] = u'私有'
        else:
            tmp['status'] = u'ERROR'

        list.append(tmp)

    rnt['list'] = list

    return rnt

# 获取某个分类文章
def get_posts_by_meta_id(metaid=1, page=1, num=5, type=0, userid=0):

    list = []
    postlist = Post.query.order_by(Post.post_date.desc()).filter_by(post_meta=metaid)

    if type == 0:
        postlist = postlist.filter(Post.post_status>=PostStatus['DELETED'])
    elif type == 1:
        postlist = postlist.filter(Post.post_status>=PostStatus['RELEASED'])
    elif type == 2:
        postlist = postlist.filter(Post.post_status>=PostStatus['UNAUDITED'], Post.post_status<=PostStatus['DRAFT'])
    elif type == 3:
        postlist = postlist.filter_by(post_status=PostStatus['DELETED'])

    postlist = postlist.paginate(
        page, per_page=num
    )

    rnt = {'pagination': postlist}
    postlist = postlist.items

    for post in postlist:
        tmp = {}
        tmp['id'] = post.post_id
        tmp['title'] = post.post_title
        tmp['userid'] = post.user_id
        tmp['auther'] = get_user_by_id(post.user_id).user_nicename
        tmp['metaid'] = post.post_meta
        tmp['meta'] = get_meta_by_id(post.post_meta).meta_name
        tmp['talk'] = 0
        tmp['datatime'] = post.post_date.strftime("%Y-%m-%d %H:%M:%S")

        if post.post_status == PostStatus['RELEASED']:
            tmp['status'] = u'已发布'
        elif post.post_status == PostStatus['DRAFT']:
            tmp['status'] = u'草稿'
        elif post.post_status == PostStatus['OVERHEAD']:
            tmp['status'] = u'置顶'
        elif post.post_status == PostStatus['DELETED']:
            tmp['status'] = u'回收站'
        elif post.post_status == PostStatus['UNAUDITED']:
            tmp['status'] = u'未审核'
        elif post.post_status == PostStatus['PRIVATE']:
            tmp['status'] = u'私有'
        else:
            tmp['status'] = u'ERROR'

        list.append(tmp)

    rnt['list'] = list

    return rnt

# 获取某个标签文章
def get_posts_by_label_id(labelid=1, page=1, num=5, type=0, userid=0):

    postlist = Post.query.order_by(Post.post_date.desc()).join(Postlabel).filter(Postlabel.label_id==labelid)
    list = []

    if type == 0:
        postlist = postlist.filter(Post.post_status>=PostStatus['DELETED'])
    elif type == 1:
        postlist = postlist.filter(Post.post_status>=PostStatus['RELEASED'])
    elif type == 2:
        postlist = postlist.filter(Post.post_status>=PostStatus['UNAUDITED'], Post.post_status<=PostStatus['DRAFT'])
    elif type == 3:
        postlist = postlist.filter_by(post_status=PostStatus['DELETED'])

    postlist = postlist.paginate(
        page, per_page=num
    )

    rnt = {'pagination': postlist}
    postlist = postlist.items

    for post in postlist:
        tmp = {}
        tmp['id'] = post.post_id
        tmp['title'] = post.post_title
        tmp['userid'] = post.user_id
        tmp['auther'] = get_user_by_id(post.user_id).user_nicename
        tmp['metaid'] = post.post_meta
        tmp['meta'] = get_meta_by_id(post.post_meta).meta_name
        tmp['talk'] = 0
        tmp['datatime'] = post.post_date.strftime("%Y-%m-%d %H:%M:%S")

        if post.post_status == PostStatus['RELEASED']:
            tmp['status'] = u'已发布'
        elif post.post_status == PostStatus['DRAFT']:
            tmp['status'] = u'草稿'
        elif post.post_status == PostStatus['OVERHEAD']:
            tmp['status'] = u'置顶'
        elif post.post_status == PostStatus['DELETED']:
            tmp['status'] = u'回收站'
        elif post.post_status == PostStatus['UNAUDITED']:
            tmp['status'] = u'未审核'
        elif post.post_status == PostStatus['PRIVATE']:
            tmp['status'] = u'私有'
        else:
            tmp['status'] = u'ERROR'

        list.append(tmp)

    rnt['list'] = list

    return rnt


# 随机获得文章
def get_posts_rand():

    postList = Post.query.all()
    random.shuffle(postList)

    return postList

# 相关文章推荐（猜你喜欢）
def maybe_you_like(postId):

    postLabelList = Postlabel.query.filter_by(post_id=postId).all()
    postList = []

    # 获得同标签的文章列表
    for postLabel in postLabelList:
        if postLabel.post_id is not postId:
            postList.append(get_post_by_id(postLabel.post_id))

    return postList


# 以ID获取页面
def get_page_by_id(pageid):

    page = Page.query.filter_by(page_id=pageid).first()
    return page

# 获取全部页面
def get_all_pages(page=1, type=0, num=5, userid=0):

    list = []
    pagelist = 0
    if type == 0:
        pagelist = Page.query.order_by(Page.page_date.desc()).filter(Page.page_status>PostStatus['DELETED'])
    elif type == 1:
        pagelist = Page.query.order_by(Page.page_date.desc()).filter(Page.page_status>=PostStatus['RELEASED'])
    elif type == 2:
        pagelist = Page.query.order_by(Page.page_date.desc()).filter(Page.page_status>=PostStatus['UNAUDITED'], Page.page_status<=PostStatus['DRAFT'])
    elif type == 3:
        pagelist = Page.query.order_by(Page.page_date.desc()).filter_by(page_status=PostStatus['DELETED'])

    if userid != 0:
        pagelist = pagelist.filter_by(user_id=userid)

    pagelist = pagelist.paginate(
        page, per_page=num
    )

    rnt = {'pagination': pagelist}
    pagelist = pagelist.items

    for page in pagelist:
        tmp = {}
        tmp['id'] = page.page_id
        tmp['title'] = page.page_title
        tmp['userid'] = page.user_id
        tmp['auther'] = get_user_by_id(page.user_id).user_nicename
        tmp['slug'] = page.page_slug
        tmp['talk'] = 0
        tmp['datatime'] = page.page_date.strftime("%Y-%m-%d %H:%M:%S")

        if page.page_status == PostStatus['RELEASED']:
            tmp['status'] = u'已发布'
        elif page.page_status == PostStatus['DRAFT']:
            tmp['status'] = u'草稿'
        elif page.page_status == PostStatus['DELETED']:
            tmp['status'] = u'回收站'
        elif page.page_status == PostStatus['UNAUDITED']:
            tmp['status'] = u'未审核'
        elif page.page_status == PostStatus['PRIVATE']:
            tmp['status'] = u'私有'
        else:
            tmp['status'] = u'ERROR'

        list.append(tmp)

    rnt['list'] = list

    return rnt

# 获取某人发表的页面
def get_pages_by_user_id(userId):

    post = Page.query.filter_by(user_id=userId).first()
    return post
