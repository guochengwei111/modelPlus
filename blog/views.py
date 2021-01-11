from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from blog.models import Article


class ArticleListAPIView(APIView):
    def get(self, request):
        article = Article.objects.select_related("author")


class ArticleDetailAPIView(APIView):
    def get(self, request, pk):
        article = Article.objects.select_related("author").get(pk=pk)
        # article = Article.objects.select_related("author","其他外键字段可以反向__").get(pk=pk)
        # article = Article.objects.select_related("author","其他外键字段可以反向__").filter(条件)

        # article = Article.objects.prefetch_related("多对多字段名_属性").get(pk=pk)

        # 按条件查询到的数据集放在下面命名的列表中
        # Article.objects.all().prefetch_related(Prefetch("多对多字段名", queryset="数据集查询条件"), to_attr="article_p_tag")


from django.http import HttpResponse


def index(request):
    # return HttpResponse("Hello world")
    # ip = request.META["REMOTE_ADDR"]
    # ua = request.META["HTTP_USER_AGENT"]
    # return HttpResponse(f"请求的路径：{request.path},当前ip:{ip},当前ua:{ua}")
    # values = request.META.items()
    # html = []
    # for k, v in values:
    #     print(k, v)
    #     html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    #     print(html)
    #     return HttpResponse("<table>%s</table>" % '\n'.join(html))
    user = request.user
    user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if x_forwarded_for:
        ip = str(x_forwarded_for).split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    context = {'user': user, 'user_agent': user_agent, 'ip': ip, }
    return HttpResponse(content=context)
