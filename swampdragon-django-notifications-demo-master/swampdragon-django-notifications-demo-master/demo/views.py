from django.shortcuts import render
from django.views.generic import ListView
from .models import Notification

'''
class Notifications(ListView):
    model = Notification
    template_name = 'home.html'

    def get_queryset(self):
        print(vars(self))
        print(vars(self.head))
        return self.model.objects.order_by('-pk')
'''


def Notifications(request):
    notificaciones=[]
    if request.user.is_authenticated():
        print("logueado")
        notificaciones =  Notification.objects.filter(user=request.user)
        return render(request,'home.html', {'notificaciones':notificaciones,'usuario':request.user})
    else:
        print("anonimo")
        return render(request,'home.html', {'notificaciones':[],'usuario':'anonimo'})

def Notifications_2(request):
    notificaciones=[]
    if request.user.is_authenticated():
        print("logueado")
        notificaciones =  Notification.objects.filter(user=request.user)
        return render(request,'home.html', {'notificaciones':notificaciones,'usuario':request.user})
    else:
        print("anonimo")
        return render(request,'home_2.html', {'notificaciones':[],'usuario':'anonimo'})



