from django.shortcuts import render


def bios(request):
    return render(request, 'bios/bios.html')
