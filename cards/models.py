from typing import Any
from django.db import models
from math import ceil

from .clients import youtube_client, ankicards

class Video(models.Model):
    video_id = models.CharField(max_length=200, blank=False, unique=True)
    title = models.CharField(max_length=200)
    channel = models.CharField(max_length=200)
    duration = models.IntegerField()
    transcript = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField('users.User', related_name='videos', blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.channel}"
    
    def generate_questions_and_answers(self):
        # Ensure TaskStatus exists for this video
        task_status, _ = TaskStatus.objects.get_or_create(video=self)

        try:
            # Update the task status to indicate processing has started
            task_status.status = 'pending'
            task_status.save()

            # Your existing logic to generate questions and answers
            n_questions = ceil(self.duration / 60) // 5
            llm_context_size = 4096 * 4
            qas = ankicards.generate(self.transcript, n_questions=n_questions, context_size=llm_context_size)
            for qa in qas:
                QuestionAnswer.objects.create(video=self, question=qa.question, answer=qa.answer)

            # Update the task status to indicate completion
            task_status.status = 'complete'
            task_status.save()
        except Exception as e:
            # Update the task status to indicate failure and store the error message
            task_status.status = 'failed'
            task_status.result = str(e)
            task_status.save()
    
    @classmethod
    def create_or_get_video(cls, youtube_id):
        
        try:
            video = cls.objects.get(video_id=youtube_id)
        except cls.DoesNotExist:
            details = youtube_client.get_details(youtube_id)
            
            video = Video()
            video.video_id = youtube_id
            video.title = details['title']
            video.channel = details['channel']
            video.duration = details['duration']
            video.transcript = details['transcript']
            video.save()
        
        return video

class TaskStatus(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='task_status')
    status = models.CharField(max_length=10)  # e.g., "pending", "complete", "failed"
    result = models.TextField(null=True, blank=True)  # Optional field for storing results or errors

    def __str__(self):
        return f"{self.video.id} - {self.status}"
    
class QuestionAnswer(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question} - {self.answer}"

