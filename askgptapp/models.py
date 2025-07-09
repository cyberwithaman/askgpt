from django.db import models

# Create your models here.

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class UserQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    needs_followup = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.question[:50]}"
    
    class Meta:
        verbose_name = "User Query"
        verbose_name_plural = "User Queries"
