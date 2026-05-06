from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import os

from .models import SyncLog

@login_required(login_url='/admin/login/')
def dashboard_home(request):
    # Fetching all items from the database to display
    logs = SyncLog.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/index.html', {'logs': logs})

@login_required(login_url='/admin/login/')
def download_file(request, log_id):
    log = get_object_or_404(SyncLog, id=log_id)
    # The file path where the server saves files
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Cloud_Backup', log.encrypted_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{log.original_name}"'
            return response
    else:
        raise Http404("File not found")