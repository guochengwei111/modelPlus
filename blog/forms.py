from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from blog.models import Article, Recipe, Ingredient


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    body = forms.Textarea()


# 可以进行校验，也可以form.as_p到模版中使用上面的钩子生成表单

# 1.表单集由自定义表单类创建  模板中 {{ formset }}直接可以使用
# extra  页面想要显示空白单的数量
# max_num 表单显示的最大数量，可选参数，默认1000，max_num的优先权大于extra 下面只显示2个空表单
ArticleFormSet1 = formset_factory(ArticleForm, extra=3, max_num=2)

# 2.表单集由模型类直接创建
ArticleFormSet2 = modelformset_factory(Article, fields=("title", "body"), extra=3)


# 3.上面一和二结合使用会好一些，先创建ModelForm，然后添加单个表单验证
# 最后利用modelformset_factory创建FormSet  下面的这个要比上面的两个更灵活一些
class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body"]

    def clean_title(self):
        pass


ArticleFormSet3 = modelformset_factory(Article, form=ArticleModelForm)


# 4.但如果我们希望同一个页面上添加一个菜谱(Recipe)和多个原料(Ingredient)，
# 这时我们就需要用使用inlineformset了。
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description"]
    # 下面可以写校验


# 该方法的第一个参数和第二个参数都是模型，其中第一个参数必需是ForeignKey。
IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=["name"], extra=3, can_delete=False, max_num=5)
