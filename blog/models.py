from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
import uuid
import os
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Article(models.Model):
    STATUS_CHOICES = (
        ("d", "草稿"),
        ("p", "发表"),
    )

    title = models.CharField("标题", max_length=200, unique=True)
    slug = models.SlugField("slug", max_length=60, unique=True)
    body = models.TextField("正文")
    pub_date = models.DateTimeField("发布时间", default=now, null=True)
    create_date = models.DateTimeField("创建时间", auto_now_add=True)
    mod_date = models.DateTimeField("修改时间", auto_now=True)
    status = models.CharField("文章状态", max_length=1, choices=STATUS_CHOICES, default="p")
    views = models.PositiveIntegerField("浏览量", default=0)
    author = models.ForeignKey(to=User, verbose_name="作者", on_delete=models.CASCADE)

    # tags = models.ManyToManyField("Tag", verbose_name="标签集合", blank=True)

    def __str__(self):
        return self.title  # 显示文章对象名字

    def viewed(self):
        self.views += 1
        self.save(update_fields=["views"])

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "article"  # 给模型命名

    # slug主要用来做url拼接，构建语义化的URL网址，且数据库中唯一
    def slug(self):
        slug = slugify(self.title)


def user_directory_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    # 动态定义文件上传的位置  个人id，头像，重命名的文件名称
    # 按照用户上传的不用的文件类型存放到对应文件夹里面
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(instance.user.id, sub_folder, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name="头像")


# 我们可以使用Person.objects.all()查询到所有人，
# 而Person.authors.all和Person.editors.all()只返回所authors和editors。


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")


class EditManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="E")


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=(("A", _("Author")), ('E', _('Editor'))))
    objects = models.Manager()
    authors = AuthorManager()
    editors = EditManager()


from django.db import models


# 菜谱配方
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


# 原料成分
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient')
    name = models.CharField(max_length=255)
