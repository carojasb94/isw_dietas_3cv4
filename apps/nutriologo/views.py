from django.shortcuts import render

# Create your views here.



def agendar_cita(request):
    print('agendar_cita')
    print(request)
    if request.method == 'POST':
        print(request.POST)

    return render(request, 'nutriologo/agendar_cita.html', {})







