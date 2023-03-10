from django.shortcuts import render, HttpResponse
from markdown2 import Markdown
from django import forms
from random import randint
from . import util

def markdownToHtml(entryItem):
    entry_list = util.list_entries()
    for item in entry_list:
        if entryItem.upper() == item.upper():
            content = util.get_entry(item)
            markdowner = Markdown()
            if content == None:
                return None
            else:
                return {'title': item, 'content': markdowner.convert(content)}

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    title1 = markdownToHtml(title)['title']
    content = markdownToHtml(title)['content'] # checks if entry exists and can be converted
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": "The entry doesn't exist."
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title1,
            "details": content
            })

def search(request):
    if request.method == 'POST':
        to_search = request.POST.get('q')
        exists = markdownToHtml(to_search)
        if exists is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": exists['title'],
                "details": exists['content']
            })
        else:
            entry_list = util.list_entries()
            found_entries = []
            for item in entry_list:
                if to_search.lower() in item.lower():
                    found_entries.append(item)

            return render(request, "encyclopedia/search.html", {
                "item": to_search,
                "entries": found_entries
            })      

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        exists = markdownToHtml(title)
        if exists == None:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "details": markdownToHtml(title)['content']
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists."
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content is not None:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "details": markdownToHtml(title)['content']
            })

def random_entry(request):
    entry_list = util.list_entries()
    entry_no = randint(0, len(entry_list)-1)
    title = entry_list[entry_no]
    content = markdownToHtml(title)["content"]
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "details": content
    })