from django.shortcuts import render
import markdown
import random

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    # if content is None:
    #     return None
    # else:
    #     markdowner = markdown.Markdown()
    #     return markdowner.convert(content)
    if content is None:
        return None
    else:
        markdowner = markdown.Markdown(extensions=['extra'], output_format='html5')
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    # if request.method.upper() == "POST":
    #     entry_search = request.POST.get("q", "").strip()
    if request.method == "POST":
        entry_search = request.POST.get("q", "").strip()
        html_content = convert_md_to_html(entry_search)
        
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            recommendations = [entry for entry in all_entries if entry_search.lower() in entry.lower()]
            
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendations
            })
    
    return render(request, "encyclopedia/error.html", {
        "message": "Invalid request method."
    })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    
    if not title or not content:
        return render(request, "encyclopedia/error.html", {
            "message": "Title and content cannot be empty."
        })
    
    title_exists = util.get_entry(title)
    
    if title_exists is not None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry page already exists."
        })

    util.save_entry(title, content)
    html_content = convert_md_to_html(title)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })
    
# def edit(request):
#     if request.method == "POST":
#         title = request.POST['entry_title']
#         content = request.POST['entry_content']
#         return render(request, "encyclopedia/edit.html", {
#             "title": title,
#             "content": content
#         })
def edit(request):
    if request.method == "POST":
        title = request.POST.get('entry_title', '')
        content = request.POST.get('entry_content', '')
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
        
def save_edit(request):    
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        
def random_page(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    html_content = convert_md_to_html(random_entry)
    
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })