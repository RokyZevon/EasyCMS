# coding=utf-8

from ..models import Meta, Postmeta


# 获得全部分类
def get_all_metas(page=1, num=5):

    if page == 0:
        metaList = Meta.query.all()
        return metaList

    pagination = Meta.query.paginate(
        page, per_page=num
    )

    return pagination


# 根据分类ID获得分类
def getMetaById(metaId):

    meta = Meta.query.filter_by(meta_id=metaId).first()

    return meta

# 根据分类缩写获得分类
def getMetaBySlug(slug):

    meta = Meta.query.filter_by(meta_slug=slug).first()

    return meta

# 获得文章的全部分组
def getPostMetas(postId):

    metaList = Postmeta.query.filter_by(post_id=postId).all()

    return metaList