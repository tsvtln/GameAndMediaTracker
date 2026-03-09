from django.shortcuts import render


def roms(request):
    return render(request, 'roms/roms.html')


def top_games(request):
    return render(request, 'roms/top-games.html')


def newly_added(request):
    return render(request, 'roms/newly-added.html')


def trending(request):
    return render(request, 'roms/trending.html')


def most_downloaded(request):
    return render(request, 'roms/most-downloaded.html')


def genres(request):
    return render(request, 'roms/genres.html')


def genre_action(request):
    return render(request, 'roms/genres/action.html')


def genre_adventure(request):
    return render(request, 'roms/genres/adventure.html')


def genre_platformer(request):
    return render(request, 'roms/genres/platformer.html')


def genre_rpg(request):
    return render(request, 'roms/genres/rpg.html')


def genre_fighting(request):
    return render(request, 'roms/genres/fighting.html')


def genre_shooter(request):
    return render(request, 'roms/genres/shooter.html')


def genre_puzzle(request):
    return render(request, 'roms/genres/puzzle.html')


def genre_sports(request):
    return render(request, 'roms/genres/sports.html')


def genre_racing(request):
    return render(request, 'roms/genres/racing.html')


def genre_strategy(request):
    return render(request, 'roms/genres/strategy.html')


def genre_simulation(request):
    return render(request, 'roms/genres/simulation.html')


def genre_horror(request):
    return render(request, 'roms/genres/horror.html')


def platforms(request):
    return render(request, 'roms/platforms.html')


def platform_nes(request):
    return render(request, 'roms/platforms/nes.html')


def platform_famicom(request):
    return render(request, 'roms/platforms/famicom.html')


def platform_snes(request):
    return render(request, 'roms/platforms/snes.html')


def platform_super_famicom(request):
    return render(request, 'roms/platforms/super-famicom.html')


def platform_n64(request):
    return render(request, 'roms/platforms/n64.html')


def platform_gamecube(request):
    return render(request, 'roms/platforms/gamecube.html')


def platform_wii(request):
    return render(request, 'roms/platforms/wii.html')


def platform_wii_u(request):
    return render(request, 'roms/platforms/wii-u.html')


def platform_nintendo_switch(request):
    return render(request, 'roms/platforms/nintendo-switch.html')


def platform_gameboy(request):
    return render(request, 'roms/platforms/gameboy.html')


def platform_gbc(request):
    return render(request, 'roms/platforms/gbc.html')


def platform_gba(request):
    return render(request, 'roms/platforms/gba.html')


def platform_nintendo_ds(request):
    return render(request, 'roms/platforms/nintendo-ds.html')


def platform_nintendo_3ds(request):
    return render(request, 'roms/platforms/nintendo-3ds.html')


def platform_sega_master_system(request):
    return render(request, 'roms/platforms/sega-master-system.html')


def platform_genesis(request):
    return render(request, 'roms/platforms/genesis.html')


def platform_sega_cd(request):
    return render(request, 'roms/platforms/sega-cd.html')


def platform_32x(request):
    return render(request, 'roms/platforms/32x.html')


def platform_sega_saturn(request):
    return render(request, 'roms/platforms/sega-saturn.html')


def platform_sega_dreamcast(request):
    return render(request, 'roms/platforms/sega-dreamcast.html')


def platform_game_gear(request):
    return render(request, 'roms/platforms/game-gear.html')


def platform_ps1(request):
    return render(request, 'roms/platforms/ps1.html')


def platform_ps2(request):
    return render(request, 'roms/platforms/ps2.html')


def platform_ps3(request):
    return render(request, 'roms/platforms/ps3.html')


def platform_psp(request):
    return render(request, 'roms/platforms/psp.html')


def platform_vita(request):
    return render(request, 'roms/platforms/vita.html')


def platform_xbox(request):
    return render(request, 'roms/platforms/xbox.html')


def platform_xbox_360(request):
    return render(request, 'roms/platforms/xbox-360.html')


def platform_xbox_one(request):
    return render(request, 'roms/platforms/xbox-one.html')


def platform_atari(request):
    return render(request, 'roms/platforms/atari.html')


def rom_details(request):
    return render(request, 'roms/rom-details.html')


def upload_rom(request):
    return render(request, 'roms/upload_rom.html')
