from django.shortcuts import render


def saves(request):
    return render(request, 'saves/saves.html')
