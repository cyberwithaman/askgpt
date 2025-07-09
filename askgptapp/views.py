from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import FAQ, Contact, UserQuery
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import numpy as np
import re

# Create dummy embeddings for FAISS
class DummyEmbeddings:
    def embed_documents(self, texts):
        # Create random embeddings with consistent dimensions
        return [np.random.rand(768) for _ in texts]
    
    def embed_query(self, text):
        # Create random embedding with consistent dimensions
        return np.random.rand(768)

# Initialize FAISS vector store with dummy embeddings
def initialize_faiss():
    faqs = FAQ.objects.all()
    if not faqs:
        return None
    
    texts = [f"{faq.question} {faq.answer} {faq.keywords}" for faq in faqs]
    
    # Create dummy embeddings
    embeddings = DummyEmbeddings()
    
    # Create FAISS index
    return FAISS.from_texts(texts, embeddings)

# Keyword-based search as fallback
def keyword_search(query, faqs):
    query = query.lower()
    results = []
    
    for faq in faqs:
        # Check if query matches keywords, question or answer
        keywords = faq.keywords.lower().split(',')
        question = faq.question.lower()
        answer = faq.answer.lower()
        
        # Simple scoring system
        score = 0
        
        # Check for exact keyword matches
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword in query:
                score += 10
        
        # Check for word matches in question
        query_words = set(re.findall(r'\w+', query))
        question_words = set(re.findall(r'\w+', question))
        answer_words = set(re.findall(r'\w+', answer))
        
        common_question_words = query_words.intersection(question_words)
        common_answer_words = query_words.intersection(answer_words)
        
        score += len(common_question_words) * 5
        score += len(common_answer_words) * 2
        
        if score > 0:
            results.append((faq, score))
    
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    return [faq for faq, _ in results]

def home(request):
    if request.method == 'POST':
        if 'user_info' in request.POST:
            # Store user info in session
            request.session['name'] = request.POST.get('name', '')
            request.session['email'] = request.POST.get('email', '')
            request.session['phone'] = request.POST.get('phone', '')
            request.session['agreed_to_terms'] = request.POST.get('agreed_to_terms') == 'on'
            
            # Redirect to same page to avoid form resubmission
            return redirect('home')
        
        elif 'query' in request.POST and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Handle AJAX query
            query = request.POST.get('query', '')
            
            if not query:
                return JsonResponse({'answer': 'Please enter a question.'})
            
            # Get user info from session
            name = request.session.get('name', '')
            email = request.session.get('email', '')
            phone = request.session.get('phone', '')
            
            # Get all FAQs
            faqs = FAQ.objects.all()
            
            answer = None
            question = None
            needs_followup = False
            
            if not faqs:
                answer = "We don't have any FAQs in our database yet. Our team will contact you shortly regarding your question."
                needs_followup = True
            else:
                try:
                    # Try FAISS search first
                    faiss_index = initialize_faiss()
                    if faiss_index:
                        # Get embeddings for query
                        dummy_embeddings = DummyEmbeddings()
                        query_embedding = dummy_embeddings.embed_query(query)
                        
                        # Search FAISS index
                        faiss_results = faiss_index.similarity_search_by_vector(query_embedding, k=1)
                        
                        if faiss_results:
                            # Extract FAQ from results
                            result_text = faiss_results[0].page_content
                            # Find the matching FAQ
                            for faq in faqs:
                                combined_text = f"{faq.question} {faq.answer} {faq.keywords}"
                                if combined_text == result_text:
                                    answer = faq.answer
                                    question = faq.question
                                    break
                
                except Exception as e:
                    # If FAISS fails, fall back to keyword search
                    pass
                
                # If no answer yet, try keyword search
                if not answer:
                    keyword_results = keyword_search(query, faqs)
                    
                    if keyword_results:
                        best_match = keyword_results[0]
                        answer = best_match.answer
                        question = best_match.question
                    else:
                        answer = "I couldn't find an answer to your question in our FAQ database. Please provide your contact details and our team will get back to you shortly."
                        needs_followup = True
            
            # Store the user query and response in the database
            UserQuery.objects.create(
                name=name,
                email=email,
                phone=phone,
                question=query,
                answer=answer,
                needs_followup=needs_followup
            )
            
            return JsonResponse({'answer': answer, 'question': question})
    
    # Check if user info is in session
    user_registered = all(key in request.session for key in ['name', 'email', 'phone', 'agreed_to_terms'])
    
    return render(request, 'home.html', {
        'user_registered': user_registered,
        'name': request.session.get('name', ''),
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'contact.html')
