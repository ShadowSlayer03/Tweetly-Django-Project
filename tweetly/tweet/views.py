from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Tweet
from .forms import TweetForm, UserRegistrationForm

# View to list all tweets
def index(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tweets': tweets})

@login_required
# View to handle new tweet submission
def tweet_submit(request):
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm()

    return render(request, 'tweet_details.html', {'form': form})

@login_required
# View to edit tweets
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
        
    else:
        form = TweetForm(instance=tweet)
        
    return render(request, 'tweet_details.html', {'form': form})

@login_required
# View to delete tweet
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('index')
    return render(request,'tweet_confirm_delete.html',{'tweet': tweet})

