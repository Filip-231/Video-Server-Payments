from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse
from .models import Membership, UserMembership, Subscription

import stripe

def get_user_membership(request):
    user_membership_qs=UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists:
        return user_membership_qs.first()
    return None
def get_user_subscription(request):
    user_subscription_qs=Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription= user_subscription_qs.first()
        return user_subscription
    return None
def get_selected_membership(request):
    #if selected membership is in the session
    membership_type=request.session['selected_membership_type']
    selected_membership_qs= Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

@login_required
def profile_view(request):
    user_membership=get_user_membership(request)
    user_subscription=get_user_subscription(request)
    context={
        'user_membership': user_membership,
        'user_subscription': user_subscription

    }
    return render(request,"memberships/profile.html",context)


# class MembershipSelectView(LoginRequiredMixin,ListView):
#     model= Membership
#
#     #dodaje kontekst
#     def get_context_data(self, *args, **kwargs):
#         context=super().get_context_data(**kwargs)
#         current_membership=get_user_membership(self.request)
#         #dzieki temu button zmienia sie na : current membership
#         context['current_membership']=str(current_membership.membership)
#
#         return context
#     def post(self,request, **kwargs):
#         selected_membership_type=request.POST.get('membership_type')
#         user_membership=get_user_membership(request)
#         user_subscription= get_user_subscription(request)
#
#         # selected_membership_qs=Membership.objects.filter(
#         #     membership_type= selected_membership_type
#         # )
#         # #mamy selected membership object a nie tylko string
#         # if selected_membership_qs.exists():
#         #     selected_membership=selected_membership_qs.first()
#
#         selected_membership_type=request.POST.get('membership_type')
#         selected_membership= Membership.objects.get(
#             membership_type=selected_membership_type)
#
#
#
#
#         """
#         ==========
#         VALIDATION
#         ==========
#         """
#         if user_membership.membership == selected_membership:
#             if user_subscription != None:
#                 messages.info(request="You already have this membership. Your \
#                               next payment is due {}".format('get this value from stripe'))
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #wraca tam skąd przyszedł
#
#         # assign to the session
#         # request.session['selected_membership_type']=selected_membership.membership_type #wrzuca wartosc np. Enterprise do sesji
#
#         return HttpResponseRedirect(reverse('memberships:payment'))



class MembershipSelectView(LoginRequiredMixin, ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')

        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                              next payment is due {}""".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))






#not a class based view
#4242 4242 4242 4242

# @login_required
# def PaymentView(request):
#     user_membership=get_user_subscription(request)
#     # selected_membership=get_selected_membership(request)
#     # publishKey=settings.STRIPE_PUBLISHABLE_KEY
#     try:
#         selected_membership=get_selected_membership(request)
#
#     except:
#         return redirect(reverse("memberships:select"))
#     publishKey=settings.STRIPE_PUBLISHABLE_KEY
#
#     #https://stripe.com/docs/api/subscriptions/create
#     if request.method=="POST":
#         try:
#             token= request.POST['stripeToken']
#             customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
#             customer.source = token # 4242424242424242
#             customer.save()
#
#             '''
#             Now we can create the subscription using only the customer as we don't need to pass their
#             credit card source anymore
#             '''
#
#             subscription = stripe.Subscription.create(
#                 customer=user_membership.stripe_customer_id,
#                 items=[
#
#                     { "plan": selected_membership.stripe_plan_id },
#                 ]
#             )
#
#             return redirect(reverse('memberships:update-transactions',
#                                     kwargs={
#                                         'subscription_id': subscription.id
#                                     }))
#         except:
#                 messages.info(request, "An error has occurred, investigate it in the console")
#
#
#     context={
#             'publishKey': publishKey,
#             'selected_membership': selected_membership
#         }
#
#     return render(request, "memberships/membership_payment.html", context)



@login_required
def PaymentView(request):
    print("dsad")
    user_membership = get_user_membership(request)

    print(user_membership)
    try:
        selected_membership = get_selected_membership(request)
        print("done")
    except:
        return redirect(reverse("memberships:select"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    print("publishkey {}".format(publishKey))

    print(request.method)
    if request.method == "POST":

        print("post")
        # try:
        print("tutaj")

        print(request)
        print(request.POST['stripeToken'])
        token = request.POST['stripeToken']

        # UPDATE FOR STRIPE API CHANGE 2018-05-21

        '''
        First we need to add the source for the customer
        '''

        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
        customer.source = token # 4242424242424242
        customer.save()

        '''
        Now we can create the subscription using only the customer as we don't need to pass their
        credit card source anymore
        '''

        subscription = stripe.Subscription.create(
            customer=user_membership.stripe_customer_id,
            items=[
                { "plan": selected_membership.stripe_plan_id },
            ]
        )

        return redirect(reverse('memberships:update-transactions',
                                kwargs={
                                    'subscription_id': subscription.id
                                }))

        # except:
        #     messages.info(request, "An error has occurred, investigate it in the console")

    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payment.html", context)




@login_required
def updateTransactions(request, subscription_id):
    user_membership=get_user_membership(request)
    selected_membership=get_selected_membership(request)

    user_membership.membership= selected_membership
    user_membership.save()

    sub,created = Subscription.objects.get_or_create(user_membership= user_membership)
    sub.stripe_subscription_id = subscription_id

    sub.active=True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request,"successfully created {} membership".format(selected_membership))
    return redirect('memberships:select')







######################################################################

@login_required
def updateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('memberships:select'))

@login_required
def cancelSubscription(request):
    #https://stripe.com/docs/api/subscriptions/cancel
    #pobieram informacje o subskrypcji
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))#back where u came from

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    #aktualizuje informacje o subskrypcji na free
    free_membership = Membership.objects.get(membership_type='Free')#.first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(
        request, "Successfully cancelled membership. We have sent an email")

    # sending an email here

    return redirect(reverse('memberships:select'))







