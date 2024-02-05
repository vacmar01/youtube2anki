from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .youtube_utils import youtube_id
import os
from math import ceil

from .models import Video, QuestionAnswer

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
        
        if not video.questionanswer_set.exists():
            video.generate_questions_and_answers()
        
        context['video'] = video
        context['qas'] = video.questionanswer_set.all()

    except Exception as e:
        context['error'] = 'An error occured. Please try again.'
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
    
