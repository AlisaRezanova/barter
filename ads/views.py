from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from .forms import AdForm
from .models import Ad, ExchangeProposal
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def edit_ad(request, ad_id):
    user = request.user
    try:
        ad = get_object_or_404(Ad, id=ad_id, user=user)
    except:
        return JsonResponse({'message': 'ad is not found'}, status=404)

    if request.method in ['POST', 'PUT']:
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = AdForm(instance=ad)
    return render(request, 'ads/form.html', {'form': form})


@login_required
def delete_ad(request, ad_id):
    user = request.user
    ad = get_object_or_404(Ad, id=ad_id, user=user)
    if request.method == 'POST':
        ad.delete()
        return JsonResponse({'message': 'Good Job!'})
    return JsonResponse({'message': f'Error'}, status=400)


def search_by_title_and_description(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
        if search:
            ads = Ad.objects.filter(Q(title__icontains=search) | Q(description__icontains=search)).values()
        else:
            ads = Ad.objects.none()
        paginator = Paginator(ads, limit)
        page_obj = paginator.get_page(page)
        return JsonResponse({'ads': list(page_obj),
                             'count': paginator.count,
                             'page': page,
                             'pages': paginator.num_pages})
    return JsonResponse({'message': 'Wrong method'})


def filter_by_(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
        filter_by = request.GET.get('filter_by', '')
        if filter_by == 'category':
            by_category = request.GET.get('category', '')
            ads = Ad.objects.filter(category=by_category).values()
        elif filter_by == 'condition':
            by_condition = request.GET.get('condition', '')
            ads = Ad.objects.filter(condition=by_condition).values()
        else:
            return JsonResponse({'message': f'filter by is not found'}, status=400)
        paginator = Paginator(ads, limit)
        page_obj = paginator.get_page(page)
        return JsonResponse({'ads': list(page_obj),
                            'count': paginator.count,
                            'page': page,
                            'pages': paginator.num_pages})
    return JsonResponse({'message': f'Wrong method'}, status=400)


def add_exchange_proposal(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            ad_sender_id = data.get('ad_sender_id')
            ad_receiver_id = data.get('ad_receiver_id')
            comment = data.get('comment')
            status = 'waiting'

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=402)

        ExchangeProposal.objects.create(
            ad_sender = get_object_or_404(Ad, id=ad_sender_id),
            ad_receiver = get_object_or_404(Ad, id=ad_receiver_id),
            comment = comment,
            status = status
        )

        return JsonResponse({'message': 'Good job!'})
    return JsonResponse({'message': 'Wrong method'}, status=400)


@login_required
def update_status(request, proposal_id):
    user = request.user

    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=user)

    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            proposal.status = data.get('status')
            proposal.save()
            return JsonResponse({'message': 'Good Job!'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=402)

    if request.method == 'GET':
        return JsonResponse({
            'status': proposal.status
        })
    return JsonResponse({'message': 'Wrong method'}, status=400)


def filter_proposal_by(request):
    if request.method == 'GET':
        filter_by = request.GET.get('filter_by', '')
        if filter_by == 'ad_sender':
            ad_sender = request.GET.get('ad_sender', '')
            properties = ExchangeProposal.objects.filter(ad_sender__id=ad_sender).values()
        elif filter_by == 'ad_receiver':
            ad_receiver = request.GET.get('ad_receiver', '')
            properties = ExchangeProposal.objects.filter(ad_receiver__id=ad_receiver).values()
        elif filter_by == 'status':
            status = request.GET.get('status', '')
            properties = ExchangeProposal.objects.filter(status=status).values()
        else:
            return JsonResponse({'message': 'Filter_by is not found'})
        return JsonResponse({'properties': list(properties)})
    return JsonResponse({'message': 'Wrong method'}, status=400)


def show_ads(request):
    ads = Ad.objects.all().values('id', 'user', 'title', 'description', 'image_url', 'category', 'condition', 'created_at')
    return JsonResponse({'ads': list(ads)})


def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('/')
    form = AdForm()
    return render(request, 'form.html', {'form': form})




