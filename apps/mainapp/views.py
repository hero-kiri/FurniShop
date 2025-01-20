from django.shortcuts import render, get_object_or_404
from .models import ContactMessage, BlogPost, BlogDetail
from django.contrib import messages

def index(request):
    return render(request, 'mainapp/index.html')

def about(request):
    return render(request, 'mainapp/about.html')

def blog_post_list(request):
    blog_posts = BlogPost.objects.all()  # Get all BlogPost objects
    return render(request, 'mainapp/blog.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)  # Get the blog post by primary key (pk)
    blog_details = BlogDetail.objects.filter(blog_post=blog_post)  # Get the details for the selected post
    return render(request, 'mainapp/blog_detail.html', {'blog_post': blog_post, 'blog_details': blog_details})



def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')  # Используем get для безопасности
        
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Сохранение данных в базу с обработкой исключений
        try:
            ContactMessage.objects.create(first_name=first_name,last_name=last_name, email=email, message=message)
            print(first_name, last_name, email, message)
            messages.success(request, 'Message sent successfully')
        except Exception as e:
            print(f"Error saving message: {e}")
            messages.error(request, 'An error occurred while sending the message.')

    return render(request, 'mainapp/contact.html')

def services(request):
    return render(request, 'mainapp/services.html')

