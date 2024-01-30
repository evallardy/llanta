from django.shortcuts import render

# Create your views here.

def index(request):
    template_name = 'core/index.html'
    context = {}
    if request.method == 'POST':
        datos = leer(request)
        context['datos'] = datos
    return render(request, template_name, context=context)
