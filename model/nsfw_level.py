"""
创建学生信息表模型
"""
from django.db import models

"""
 该类是用来生成数据库的 必须要继承models.Model
"""


class NsfwLevel(models.Model):
    """
    创建如下几个表的字段
    """
    id = models.IntegerField(primary_key=True)
    url = models.CharField('url', max_length=100)
    drawings = models.FloatField('drawings')
    hentai = models.FloatField('hentai')
    neutral = models.FloatField('neutral')
    porn = models.FloatField('porn')
    sexy = models.FloatField('sexy')
    classify = models.CharField('classify', max_length=100)

    # 指定表名 不指定默认APP名字——类名(app_demo_Student)
    class Meta:
        db_table = 'nsfw_level'
