from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def first_diagram(request):
    return render(request, 'first_diagram.html')

def second_diagram(request):
    return render(request, 'second_diagram.html')

def third_diagram(request):
    return render(request, 'third_diagram.html')

def bokeh(request):
    return render(request, 'bokeh.html')

def handler404(request, exception):
    return render(request, '404.html')

def handler500(request):
   return render(request, '500.html')

def handler403(request, exception):
    return render(request, '403.html')

def handler400(request, exception):
    return render(request, '400.html')