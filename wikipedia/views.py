from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Tag
from django.contrib.auth.decorators import login_required
from .forms import NewForm, NewFormTag
from django.http import HttpResponseNotFound
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def news(request):
    news = News.objects.all()
    paginator = Paginator(news, 2)
    tags = Tag.objects.all() 
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'news/news.html', {'all_news': news, 'page': page, 'tag': tags})

def news_detail(request, pk):
    news_detail = get_object_or_404(News, pk=pk)
    comments = news_detail.comments.filter(active=True)
    if request.user.is_authenticated:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = news_detail
                new_comment.save()
        else:
            comment_form = CommentForm()

        return render(request,
                    'news/news_detail.html',
                    {'news_detail': news_detail,
                    'comments': comments,
                    'comment_form': comment_form})
    return render(request,
                    'news/news_detail.html',
                    {'news_detail': news_detail,})

def news_new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewForm()
    return render(request, 'news/news_edit.html', {'form': form})


def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        form = NewForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewForm(instance=news)
    return render(request, 'news/news_edit.html', {'form': form})


def news_delete(request, pk):
    try:
        news = News.objects.get(id=pk)
        news.delete()
        return redirect('all_news')

    except:
        return HttpResponseNotFound("<h2>Такой страницы нет</h2>")


def tag_detail_view(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    news_by_tag = tag.news_set.all()
    return render(request, 'news/news_by_tag.html', 
    {'news_by_tag': news_by_tag})


def create_tag(request):
    if request.method == "POST":
        form = NewFormTag(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('all_news')
    else:
        form = NewFormTag()
    return render(request, 'news/create_tag.html', {'form': form})
