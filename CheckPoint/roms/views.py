from django.shortcuts import render


def roms(request):
    return render(request, 'roms/roms.html')
