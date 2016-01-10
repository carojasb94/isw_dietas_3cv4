from django.shortcuts import render

# Create your views here.


def test_chat(request):
    print(request)
    return render (request, 'chat/chat.html', {})

