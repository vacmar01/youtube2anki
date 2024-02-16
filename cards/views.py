from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .youtube_utils import youtube_id
import threading
import os
from math import ceil

from .models import Video, QuestionAnswer, TaskStatus

def index(request):
    context = {
        'questionCount': QuestionAnswer.objects.count(),
        'videoCount': Video.objects.count(),
    }
    return render(request, 'cards/index.html', context=context)

def generate(request):
    url = request.GET.get('url')
    context = {}
    template_name = 'cards/htmx/qas.html'
    
    try:
        video_id = youtube_id(url)
                
        video = Video.create_or_get_video(video_id)
        
        #if a user is logged in, associate the video with the user
        if request.user.is_authenticated:
            video.user.add(request.user)
            video.save()
            
        task_status, created = TaskStatus.objects.get_or_create(video=video)
        
        if not video.questionanswer_set.exists():
            task_status = TaskStatus.objects.get_or_create(video=video)[0]
            
            if task_status.status not in ['pending', 'complete']:
                # Start the long-running task in a background thread
                print('start thread')
                thread = threading.Thread(target=video.generate_questions_and_answers)
                thread.daemon = True
                thread.start()
                template_name = 'cards/htmx/pending.html'
            elif task_status.status == 'pending':
                template_name = 'cards/htmx/pending.html'
            elif task_status.status == 'complete':
                context['qas'] = video.questionanswer_set.all()
        else:
            context['qas'] = video.questionanswer_set.all()

        context['video'] = video
    except Exception as e:
        context['error'] = str(e)
        template_name = 'cards/htmx/error.html'
        
    return render(request, template_name, context=context)

class VideoListView(ListView):
    model = Video
    template_name = 'cards/videos.html'
    context_object_name = 'videos'
    ordering = ['-created_at']
    
class VideoDetailView(DetailView):
    model = Video
    template_name = 'cards/video.html'
    context_object_name = 'video'
    
