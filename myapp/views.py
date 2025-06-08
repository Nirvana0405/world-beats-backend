# myapp/views.py
from django.shortcuts import render
from .models import Track

def track_list(request):
    tracks = Track.objects.all()
    return render(request, 'track_list.html', {'tracks': tracks})

# myapp/views.py
from django.shortcuts import render, redirect
from .forms import TrackForm

def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('track_list')  # トラックリストにリダイレクト
    else:
        form = TrackForm()

    return render(request, 'add_track.html', {'form': form})


from django.shortcuts import render
from .models import Track

def track_list(request):
    tracks = Track.objects.all()
    return render(request, 'myapp/track_list.html', {'tracks': tracks})
