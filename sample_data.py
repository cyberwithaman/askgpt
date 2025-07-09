from datetime import datetime, timedelta
import random
import os
import django

# Setup Django environment if running as standalone script
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askgpt.settings')
    django.setup()

# Import models after Django setup
from askgptapp.models import FAQ, Contact, UserQuery

def generate_sample_data():
    """
    Generate sample data for the AskGPT application.
    This includes FAQs, contacts, and user queries.
    """
    # Generate sample FAQs
    if FAQ.objects.count() < 10:
        sample_faqs = [
            {
                'question': 'What is AskGPT?',
                'answer': 'AskGPT is a local FAQ assistant powered by LangChain that helps answer your questions without using external APIs.',
                'keywords': 'askgpt, faq, assistant, langchain'
            },
            {
                'question': 'How does AskGPT work?',
                'answer': 'AskGPT uses LangChain components like FAISS with dummy embeddings and keyword-based search to find answers to your questions from the FAQ database.',
                'keywords': 'langchain, faiss, search, embeddings'
            },
            {
                'question': 'Is AskGPT free to use?',
                'answer': 'Yes, AskGPT is completely free to use as it runs locally without any external API calls.',
                'keywords': 'free, pricing, cost'
            },
            {
                'question': 'Does AskGPT use OpenAI or other LLMs?',
                'answer': 'No, AskGPT does not use any external LLMs like OpenAI, Claude, or others. It works completely offline.',
                'keywords': 'openai, llm, offline, external'
            },
            {
                'question': 'How can I add new FAQs?',
                'answer': 'You can add new FAQs through the admin panel. Just log in as an administrator and navigate to the FAQs section.',
                'keywords': 'add, faq, admin, create'
            },
            {
                'question': 'What database does AskGPT use?',
                'answer': 'AskGPT uses SQLite3, which is the default database for Django applications.',
                'keywords': 'database, sqlite, storage'
            },
            {
                'question': 'Can I customize the UI of AskGPT?',
                'answer': 'Yes, you can customize the UI by modifying the templates and CSS files in the project.',
                'keywords': 'ui, customize, templates, css'
            },
            {
                'question': 'How do I deploy AskGPT?',
                'answer': 'You can deploy AskGPT like any Django application using WSGI/ASGI servers like Gunicorn or Daphne.',
                'keywords': 'deploy, production, server'
            },
            {
                'question': 'Is AskGPT responsive on mobile devices?',
                'answer': 'Yes, AskGPT uses Bootstrap 5 which provides a responsive design that works well on mobile devices.',
                'keywords': 'responsive, mobile, bootstrap'
            },
            {
                'question': 'How can I contact support?',
                'answer': 'You can contact support by using the contact form on the website.',
                'keywords': 'contact, support, help'
            }
        ]
        
        # Create FAQs with different dates over the past few months
        for i, faq_data in enumerate(sample_faqs):
            # Create date between 1-6 months ago
            months_ago = random.randint(1, 6)
            days_variation = random.randint(-15, 15)
            created_date = datetime.now() - timedelta(days=30*months_ago + days_variation)
            
            FAQ.objects.create(
                question=faq_data['question'],
                answer=faq_data['answer'],
                keywords=faq_data['keywords'],
                created_at=created_date,
                updated_at=created_date
            )
        print(f"Created {len(sample_faqs)} FAQs")
    
    # Generate sample contacts
    if Contact.objects.count() < 20:
        sample_names = ['John Doe', 'Jane Smith', 'Robert Johnson', 'Emily Davis', 'Michael Brown', 
                       'Sarah Wilson', 'David Miller', 'Jennifer Taylor', 'James Anderson', 'Lisa Thomas']
        
        sample_emails = ['john@example.com', 'jane@example.com', 'robert@example.com', 'emily@example.com',
                        'michael@example.com', 'sarah@example.com', 'david@example.com', 'jennifer@example.com',
                        'james@example.com', 'lisa@example.com']
        
        sample_phones = ['123-456-7890', '234-567-8901', '345-678-9012', '456-789-0123', '567-890-1234',
                        '678-901-2345', '789-012-3456', '890-123-4567', '901-234-5678', '012-345-6789']
        
        sample_messages = [
            'I have a question about your services.',
            'How can I get started with AskGPT?',
            'Is there a premium version available?',
            'I found a bug in your application.',
            'I would like to request a new feature.',
            'Your service is amazing! Thank you!',
            'Can you provide more documentation?',
            'I need help setting up AskGPT.',
            'Do you offer support for enterprise customers?',
            'I would like to give some feedback on your service.'
        ]
        
        contacts_created = 0
        # Create contacts with different dates over the past 30 days
        for i in range(20):
            name_index = random.randint(0, len(sample_names) - 1)
            message_index = random.randint(0, len(sample_messages) - 1)
            
            # Create date between 1-30 days ago
            days_ago = random.randint(1, 30)
            created_date = datetime.now() - timedelta(days=days_ago)
            
            Contact.objects.create(
                name=sample_names[name_index],
                email=sample_emails[name_index],
                phone=sample_phones[name_index],
                message=sample_messages[message_index],
                created_at=created_date
            )
            contacts_created += 1
        print(f"Created {contacts_created} contacts")
    
    # Generate sample user queries
    if UserQuery.objects.count() < 30:
        sample_names = ['Alex Johnson', 'Maria Garcia', 'Wei Chen', 'Priya Patel', 'Jamal Williams', 
                       'Sophia Kim', 'Carlos Rodriguez', 'Aisha Ahmed', 'Hiroshi Tanaka', 'Olga Petrov']
        
        sample_emails = ['alex@example.com', 'maria@example.com', 'wei@example.com', 'priya@example.com',
                        'jamal@example.com', 'sophia@example.com', 'carlos@example.com', 'aisha@example.com',
                        'hiroshi@example.com', 'olga@example.com']
        
        sample_phones = ['111-222-3333', '222-333-4444', '333-444-5555', '444-555-6666', '555-666-7777',
                        '666-777-8888', '777-888-9999', '888-999-0000', '999-000-1111', '000-111-2222']
        
        sample_questions = [
            'How do I reset my password?',
            'What are your business hours?',
            'Do you offer discounts for non-profits?',
            'Can I use AskGPT offline?',
            'Is there an API available?',
            'How secure is my data with AskGPT?',
            'Do you have a mobile app?',
            'What programming languages does AskGPT support?',
            'How often do you update the FAQ database?',
            'Can I export my chat history?'
        ]
        
        sample_answers = [
            'You can reset your password through the account settings page.',
            'Our business hours are Monday to Friday, 9 AM to 5 PM EST.',
            'Yes, we offer special discounts for non-profit organizations. Please contact our sales team.',
            'Yes, AskGPT is designed to work completely offline.',
            'We currently do not offer a public API, but it is on our roadmap.',
            'Your data is stored locally and not shared with any external services.',
            'We do not currently have a mobile app, but our web interface is mobile-friendly.',
            'AskGPT is language-agnostic and can work with any programming language.',
            'The FAQ database is updated whenever administrators add new content.',
            'Currently, chat history export is not available but will be added in a future update.'
        ]
        
        queries_created = 0
        followup_count = 0
        # Create user queries with different dates over the past 30 days
        for i in range(30):
            name_index = random.randint(0, len(sample_names) - 1)
            question_index = random.randint(0, len(sample_questions) - 1)
            
            # Create date between 1-30 days ago
            days_ago = random.randint(1, 30)
            created_date = datetime.now() - timedelta(days=days_ago)
            
            # 30% chance of needing follow-up
            needs_followup = random.random() < 0.3
            if needs_followup:
                followup_count += 1
            
            # If needs follow-up, don't provide an answer
            answer = None if needs_followup else sample_answers[question_index]
            
            UserQuery.objects.create(
                name=sample_names[name_index],
                email=sample_emails[name_index],
                phone=sample_phones[name_index],
                question=sample_questions[question_index],
                answer=answer,
                needs_followup=needs_followup,
                created_at=created_date
            )
            queries_created += 1
        print(f"Created {queries_created} user queries ({followup_count} need follow-up)")
    
    result = {
        'faqs_created': FAQ.objects.count(),
        'contacts_created': Contact.objects.count(),
        'queries_created': UserQuery.objects.count(),
    }
    
    return result

# Run the script if called directly
if __name__ == '__main__':
    print("Generating sample data for AskGPT...")
    result = generate_sample_data()
    print(f"\nSample data generation complete!")
    print(f"Total FAQs in database: {result['faqs_created']}")
    print(f"Total contacts in database: {result['contacts_created']}")
    print(f"Total user queries in database: {result['queries_created']}")
    print("\nYou can now view the data in the admin dashboard at http://127.0.0.1:8000/admin/dashboard/") 