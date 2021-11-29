from django.shortcuts import render
from markdown2 import markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    for page in util.list_entries():
        if title.lower() == page.lower():
            title = page
    if title.lower() in [page.lower() for page in util.list_entries()]:
        print(markdown(util.get_entry(title)))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown(util.get_entry(title))
            })
    else:
        return render(request, "encyclopedia/error.html")

def search(request):
    result = request.GET["q"]
    print(result)
    if result.lower() in [page.lower() for page in util.list_entries()]:
        return entry(request, result)
    search_results_list = []
    for page in util.list_entries():
        if result.lower() in page.lower():
            search_results_list.append(page)
    return render(request, "encyclopedia/search.html", {
        "results": search_results_list
    })

def new(request):
    return render(request, "encyclopedia/new.html")

def new_page(request):
    title = request.GET["title"]
    content = request.GET["content"]
    if title.lower() in [page.lower() for page in util.list_entries()]:
        return render(request, "encyclopedia/exists_error.html")
    else:
        util.save_entry(title, content)
        return entry(request, title)

def random(request):
    return entry(request, choice(util.list_entries()))
