from django.shortcuts import render


def accounts(request):
    return render(request, 'accounts/accounts.html')


def favorites_page(request):
    return render(request, 'accounts/favorites.html')


def favorite_roms(request):
    return render(request, 'accounts/favorite-roms.html')


def favorite_screenshots(request):
    return render(request, 'accounts/favorite-screenshots.html')
