from django.shortcuts import render

# Create your views here.
def read_text_title_view(request, title_id):
    context = {
        
    }
    return render(request, 'reader/read_text.html', context)


def read_graphic_title_view(request, title_id):
    context = {
        
    }
    return render(request, 'reader/read_graphic.html', context)