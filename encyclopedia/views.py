from django.shortcuts import render

from . import util
from . import md2html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": md2html.md2html(util.get_entry(title)),
        "title": title
    })