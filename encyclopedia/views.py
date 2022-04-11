import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from . import md2html

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'size': '40'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs = {'rows': '20', 'cols': '20'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request):
    print("In views.error")
    if "e_title" not in request.session:
        print("e_title not in request.session. setting to empty str")
        request.session["e_title"] = ""

    print(f'got session e_title = {request.session["e_title"]}')
    return render(request, "encyclopedia/error.html", {
        "e_title": request.session["e_title"]
    })

def random_entry(request):
    '''Redirects to a random entry'''

    entries = util.list_entries()
    limit = len(entries)
    r = random.randrange(limit)
    title = entries[r]
    return HttpResponseRedirect(reverse(f"entry", args = [title]))


def entry(request, title):
    print("In views.entry")
    if not request.path.startswith("/wiki"):
        return HttpResponseRedirect(f"/wiki/{title}")

    # Try to get entry content
    entry = util.get_entry(title)
    print(f"entry={entry}")
    # Show an error page if no such entry
    if entry is None:
        # Setup session variable and show error page
        request.session["e_title"] = title
        print(f'set session e_title to {request.session["e_title"]}')
        print("redirecting...")
        return HttpResponseRedirect(reverse(f"error"))

    return render(request, "encyclopedia/entry.html", {
        "entry": md2html.md2html(entry),
        "title": title
    })

def add(request, title=""):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # TODO: refactor with try
            f = open(f"entries/{title}.md", "w")
            f.write(content)
            f.close()
            request.session["result"] = "success"
            return HttpResponseRedirect(reverse(f"{title}"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(initial={'title': title})
        })