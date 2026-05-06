from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import os

from .models import SyncLog

@login_required(login_url='/admin/login/?next=/')
def dashboard_home(request):
    # Fetching all items from the database to display
    logs = SyncLog.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/index.html', {'logs': logs})

# Using Caesar Cipher Decryption for downloads
SECRET_KEY = 5
def caesar_decrypt(text, shift=SECRET_KEY):
    decrypted = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            decrypted += chr((ord(char) - start - shift) % 26 + start)
        else:
            decrypted += char
    return decrypted

@login_required(login_url='/admin/login/?next=/')
def download_file(request, log_id):
    log = get_object_or_404(SyncLog, id=log_id)
    # The file path where the server saves files
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Cloud_Backup', log.encrypted_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
            
        # Decrypt it so the user downloads their original file, not the scrambled version!
        decrypted_content = caesar_decrypt(encrypted_content)
        
        response = HttpResponse(decrypted_content.encode('utf-8'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{log.original_name}"'
        return response
    else:
        raise Http404("File not found")