from django.shortcuts import render


def bios(request):
    return render(request, 'bios/bios.html')


def bios_faq(request):
    return render(request, 'bios/bios-faq.html')


def bios_legal(request):
    return render(request, 'bios/bios-legal.html')


def bios_comp(request):
    return render(request, 'bios/bios-comp.html')


def bios_upload(request):
    return render(request, 'bios/bios-upload.html')


def bios_all_files(request):
    # note: to replace later with actual query, for now its static data to display the html/css
    bios_by_platform = {
        'PlayStation': [
            {
                'name': 'scph1001.bin',
                'filename': 'scph1001.bin',
                'description': 'This is the BIOS file for the original PlayStation console, model SCPH-1001. '
                               'It is essential for emulating the PlayStation and is required for '
                               'running games on most emulators.',
                'uploader': 'CoolLamaUser',
                'upload_date': '10.03.26',
                'downloads': 283},
            {
                'name': 'scph5501.bin',
                'filename': 'scph5501.bin',
                'description': 'This is the BIOS file for the PlayStation console, model SCPH-5501. ',
                'uploader': 'BIOSMaster',
                'upload_date': '09.12.25',
                'downloads': 150
            },
        ],
        'PlayStation 2': [
            {
                'name': 'SCPH-39001',
                'filename': 'SCPH-39001',
                'description': 'This is the BIOS file for the PlayStation 2 console, model SCPH-39001. ',
                'uploader': 'PS2Fan',
                'upload_date': '11.01.15',
                'downloads': 120
            },
        ],
    }
    return render(request, 'bios/bios-all-files.html', {'bios_by_platform': bios_by_platform})
