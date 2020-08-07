from django.shortcuts import render

# Create your views here.

def index(request):

    context = {'search_string': ""}
    return render(request, 'ccapp/index.html', context)

def checkUrl(request):

    query = request.GET.get('search_string')
    context = {'search_string': query}
    # search_string = url_string
    return render(request, 'ccapp/index.html', context)
