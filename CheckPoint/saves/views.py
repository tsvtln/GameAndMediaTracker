from django.shortcuts import render


def saves_main(request):
    return render(request, 'saves/saves.html')


def saves_all(request):
    return render(request, 'saves/all.html')


def saves_vault(request):
    return render(request, 'saves/vault.html')


def saves_upload(request):
    return render(request, 'saves/upload.html')


def vault(request):
    return render(request, 'saves/vault.html')


def saves_details(request):
    return render(request, 'saves/details.html')
