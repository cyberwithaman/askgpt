from django.contrib import admin
from .models import FAQ, Contact, UserQuery
import pandas as pd
# Set matplotlib backend to non-interactive Agg to avoid thread issues
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.utils.html import format_html
from django.db.models.functions import TruncDate, TruncMonth
from django.db.models import Count
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

class AdminDashboardMixin:
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='askgpt_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        from django.shortcuts import render
        
        # Get data for charts
        contact_data = self.get_contact_data()
        query_data = self.get_query_data()
        faq_data = self.get_faq_data()
        followup_data = self.get_followup_data()
        
        context = {
            **self.each_context(request),
            'title': 'AskGPT Dashboard',
            'contact_chart': contact_data['chart'],
            'contact_count': contact_data['count'],
            'query_chart': query_data['chart'],
            'query_count': query_data['count'],
            'followup_count': query_data['followup_count'],
            'faq_chart': faq_data['chart'],
            'faq_count': faq_data['count'],
            'followup_chart': followup_data['chart'],
        }
        
        return render(request, 'admin/dashboard.html', context)
    
    def get_contact_data(self):
        # Get contact data for the past 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        contacts = Contact.objects.filter(created_at__gte=thirty_days_ago)
        contacts_by_day = contacts.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        
        # Convert to DataFrame
        df = pd.DataFrame(list(contacts_by_day))
        
        # Create chart if data exists
        chart = None
        if not df.empty:
            plt.figure(figsize=(10, 4))
            plt.bar(df['date'], df['count'], color='#6a11cb')
            plt.title('Contact Form Submissions (Last 30 Days)')
            plt.xlabel('Date')
            plt.ylabel('Number of Submissions')
            plt.tight_layout()
            
            # Save chart to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close('all')
        
        return {
            'chart': chart,
            'count': contacts.count(),
        }
    
    def get_query_data(self):
        # Get query data for the past 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        queries = UserQuery.objects.filter(created_at__gte=thirty_days_ago)
        queries_by_day = queries.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        
        # Convert to DataFrame
        df = pd.DataFrame(list(queries_by_day))
        
        # Create chart if data exists
        chart = None
        if not df.empty:
            plt.figure(figsize=(10, 4))
            plt.plot(df['date'], df['count'], marker='o', linestyle='-', color='#2575fc')
            plt.title('User Queries (Last 30 Days)')
            plt.xlabel('Date')
            plt.ylabel('Number of Queries')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Save chart to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close('all')
        
        return {
            'chart': chart,
            'count': queries.count(),
            'followup_count': queries.filter(needs_followup=True).count(),
        }
    
    def get_faq_data(self):
        # Get FAQ data
        faqs = FAQ.objects.all()
        faqs_by_month = faqs.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        
        # Convert to DataFrame
        df = pd.DataFrame(list(faqs_by_month))
        
        # Create chart if data exists
        chart = None
        if not df.empty:
            plt.figure(figsize=(10, 4))
            plt.bar(df['month'], df['count'], color='#28a745')
            plt.title('FAQs Added by Month')
            plt.xlabel('Month')
            plt.ylabel('Number of FAQs')
            plt.tight_layout()
            
            # Save chart to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close('all')
        
        return {
            'chart': chart,
            'count': faqs.count(),
        }
    
    def get_followup_data(self):
        # Get query data by followup status
        queries = UserQuery.objects.all()
        followup_data = [
            queries.filter(needs_followup=True).count(),
            queries.filter(needs_followup=False).count()
        ]
        
        # Create chart
        chart = None
        if sum(followup_data) > 0:
            plt.figure(figsize=(8, 8))
            labels = ['Needs Follow-up', 'Resolved']
            colors = ['#ffc107', '#28a745']
            explode = (0.1, 0)  # explode the 1st slice (Needs Follow-up)
            
            plt.pie(followup_data, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title('User Query Distribution by Follow-up Status')
            plt.tight_layout()
            
            # Save chart to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close('all')
        
        return {
            'chart': chart,
        }

class DashboardAdmin(AdminDashboardMixin, admin.AdminSite):
    site_header = 'AskGPT Admin'
    site_title = 'AskGPT Admin Portal'
    index_title = 'AskGPT Administration'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Add dashboard link at the top
        app_list.insert(0, {
            'name': 'Dashboard',
            'app_label': 'dashboard',
            'models': [{
                'name': 'Dashboard',
                'object_name': 'dashboard',
                'admin_url': '/admin/dashboard/',
                'view_only': True,
            }]
        })
        
        return app_list

# Create a custom admin site
askgpt_admin_site = DashboardAdmin(name='askgpt_admin')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question', 'answer', 'keywords')
    list_filter = ('created_at', 'updated_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'question', 'needs_followup', 'created_at')
    search_fields = ('name', 'email', 'question', 'answer')
    list_filter = ('needs_followup', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'question', 'created_at')
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Query Details', {
            'fields': ('question', 'answer', 'needs_followup', 'created_at')
        }),
    )

# Register models with the custom admin site
askgpt_admin_site.register(FAQ, FAQAdmin)
askgpt_admin_site.register(Contact, ContactAdmin)
askgpt_admin_site.register(UserQuery, UserQueryAdmin)
