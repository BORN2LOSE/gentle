import urllib.parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DeleteView


from .forms import CreateForm
from .models import Post


class IndexView(View):
    """Simple page pagination."""
    @staticmethod
    def get(request, template='blog/index.html'):
        queryset_list = Post.objects.active()
        paginator = Paginator(queryset_list, 3)
        page_var = "p"
        page = request.GET.get(page_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context = {'page_var': page_var, 'object_list': queryset}
        return render(request, template, context)


class CreateView(View):
    success_url = 'blog/index.html'
    template = 'blog/create.html'
    form_class = CreateForm

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        context = {'form': form}
        return render(request, self.template, context)


class DetailView(View):
    @staticmethod
    def get(request, template='blog/detail.html', id=None):
        obj = get_object_or_404(Post, id=id)
        share_string = urllib.parse.quote_plus(obj.text)
        context = {'obj': obj, 'share_string': share_string}
        return render(request, template, context)


#Пока не доходит, как сделать с get_abs_url :)
# class EditView(View):
#     template = 'blog/create.html'
#     form_class = CreateForm
#
#     def get(self, request):
#         form = self.form_class
#         context = {'form': form}
#         return redner(request, self.template, context)
#
#     def post(self, request, id=None):
#         instance = get_object_or_404(Post, id=id)
#         form = self.form_class(instance)
#         if form.is_valid():
#             instance = form.save()
#             instance.save()
#             return redirect(self.template)
#         context = {'instance': instance, 'form': form}
#         return render(request, template, context)

def edit(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = CreateForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(instance.get_absolute_url())
    context = {'title': instance.title, 'instance': instance, 'form': form}
    return render(request, "blog/create.html", context)

# class PostDelete(DeleteView):
#     model = Post
#     id=None
#     success_url = 'blog:index'
#     def delete(self, request):
#         obj = get_object_or_404(self.model, self.id)
#         obj.delete()
#         return redirect(self.success_url)


def delete(request, id=None):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    return redirect('blog:index')
