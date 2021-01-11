import uuid

# print(uuid.uuid4().hex[:10])

"""
django的缓存
缓存主要解决的问题是降低服务器压力，提高系统性能，提升用户体验
Django原生支持的内存缓存库 memcached 
1.需要在settings.py里面进行缓存的配置backends，可以实现全局缓存
2.也可使用数据库和文件系统缓存 本地内存缓存

当做好cache设置后，可以用三种方式使用cache
# 在路由中使用     path('foo/<int:code>/', cache_page(60 * 15)(my_view))

# 在views中使用
from django.views.decorators.cache import cache_page
@cache_page(60 * 15)
def my_view(request):
    ...
    
# 在模版中使用
{% load cache %}
{% cache 500 sidebar request.user.username %}
    .. sidebar for logged in user ..
{% endcache %}

还可以在视图中用装饰器对缓存进行控制
from django.views.decorators.cache import cache_control
# 用户自己的浏览器缓存是私有缓存
# 用户的提供者缓存是公有缓存
#               私有缓存     无更新是传递缓存内容    缓存时间
@cache_control(private=True，must_revalidate=True, max_age=3600)
def my_view(request):
# ...

设置Django读取缓存的时候要考虑ua头和cookie
from django.views.decorators.vary import vary_on_headers
@vary_on_headers('User-Agent', 'Cookie')
def my_view(request):
    ...
    
禁用缓存
from django.views.decorators.cache import never_cache
 
@never_cache
def myview(request):
# ...
"""
"""
设置cookies
response.set_cookie(key,value,expires)
response.set_cookie("username","John",60*60*24)
# 获取cookies
request.COOKIES["username"]
# 检测cookies是否已经存在，通常在非登录页时使用
reqeust.COOKIES.has_key("username")
# 删除
response.delete_cookie("username")
"""
"""
from django.shortcuts import redirect
from django.urls import reverse
 
# 案例1
def my_view(request):
 ...
 return redirect('/index/')
 
# 案例2
def my_view(request):
 ...
    return redirect('https://www.baidu.com/')
 
# 案例3
def my_view(request):
 ...
 return redirect(reverse('blog:article_list' , kwargs={'app_label': 'auth'}))
 
 # 案例4 直接重定向到模型对象，需要在模型里面定义get_absolute_url方法
from django.shortcuts import redirect
 
def my_view(request):
 ...
 obj = MyModel.objects.get(...)
 return redirect(obj)
 
 def get_absolute_url(self):
    return reverse('blog:article_detail', args=[str(self.pk), self.slug])
"""
"""
select_related  主要在一对一或一对多，请求数据时指定同时加载外键关联数据
prefetch_related  主要针对多对多关系，还可以设置Prefetch方法来设置条件和属性

当你查询单个主对象或主对象列表并需要在模板或其它地方中使用到每个对象的关联对象信息时，
请一定记住使用select_related和prefetch_related一次性获取所有对象信息，从而提升数据库查询效率，避免重复查询。
如果不确定是否有重复查询，可使用django-debug-toolbar查看。

对与单对单或单对多外键ForeignKey字段，使用select_related方法
对于多对多字段和反向外键关系，使用prefetch_related方法
两种方法均支持双下划线指定需要查询的关联对象的字段名
使用Prefetch方法可以给prefetch_related方法额外添加额外条件和属性。
"""
