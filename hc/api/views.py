from datetime import timedelta as td
from django.contrib import messages
from django.db.models import F
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  render, redirect

from hc.api import schemas
from hc.api.decorators import check_api_key, uuid_or_400, validate_json
from hc.api.models import Check, Ping
from hc.lib.badges import check_signature, get_badge_svg
from hc.accounts.models import Member
from .forms import TeamMemberForm

from hc.api.management.commands.sendalerts import Command


@csrf_exempt
@uuid_or_400
@never_cache
def ping(request, code):
    try:
        check = Check.objects.get(code=code)

    except Check.DoesNotExist:
        return HttpResponseBadRequest()
    # get the last_ping to update the previous_ping
    previous_ping_time = check.last_ping

    check.n_pings = F("n_pings") + 1
    check.ping_before_last_ping = previous_ping_time
    check.last_ping = timezone.now()
    if check.status in ("new", "paused"):
        check.status = "up"

    if check.nag_mode == "on":
        check.nag_mode = "off"

    check.save()
    check.refresh_from_db()

    ping = Ping(owner=check)
    headers = request.META
    ping.n = check.n_pings
    remote_addr = headers.get("HTTP_X_FORWARDED_FOR", headers["REMOTE_ADDR"])
    ping.remote_addr = remote_addr.split(",")[0]
    ping.scheme = headers.get("HTTP_X_FORWARDED_PROTO", "http")
    ping.method = headers["REQUEST_METHOD"]
    # If User-Agent is longer than 200 characters, truncate it:
    ping.ua = headers.get("HTTP_USER_AGENT", "")[:200]
    ping.save()

    response = HttpResponse("OK")
    response["Access-Control-Allow-Origin"] = "*"
    return response


@csrf_exempt
@check_api_key
@validate_json(schemas.check)
def checks(request):
    if request.method == "GET":
        q = Check.objects.filter(user=request.user)
        doc = {"checks": [check.to_dict() for check in q]}
        return JsonResponse(doc)

    elif request.method == "POST":
        check = Check(user=request.user)
        check.name = str(request.json.get("name", ""))
        check.tags = str(request.json.get("tags", ""))
        if "timeout" in request.json:
            check.timeout = td(seconds=request.json["timeout"])
        if "grace" in request.json:
            check.grace = td(seconds=request.json["grace"])
        if "nag" in request.json:
            check.nag = td(seconds=request.json["nagging"])

        check.save()

        # This needs to be done after saving the check, because of
        # the M2M relation between checks and channels:
        if request.json.get("channels") == "*":
            check.assign_all_channels()

        return JsonResponse(check.to_dict(), status=201)

    # If request is neither GET nor POST, return "405 Method not allowed"
    return HttpResponse(status=405)


@csrf_exempt
@check_api_key
def pause(request, code):
    if request.method != "POST":
        # Method not allowed
        return HttpResponse(status=405)

    try:
        check = Check.objects.get(code=code, user=request.user)
    except Check.DoesNotExist:
        return HttpResponseBadRequest()

    check.status = "paused"
    check.save()
    return JsonResponse(check.to_dict())


@never_cache
def badge(request, username, signature, tag):
    if not check_signature(username, tag, signature):
        return HttpResponseBadRequest()

    status = "up"
    q = Check.objects.filter(user__username=username, tags__contains=tag)
    for check in q:
        if tag not in check.tags_list():
            continue

        if status == "up" and check.in_grace_period():
            status = "late"

        if check.get_status() == "down":
            status = "down"
            break

    svg = get_badge_svg(tag, status)
    return HttpResponse(svg, content_type="image/svg+xml")


def allocate_jobs(request): 
    """
    Assign or unassign jobs to a ream member
    """
    if request.method == 'POST':
        #get team member
        member_id = request.POST.get('member_id', '')
        team_member = Member.objects.get(id = member_id)
        team_member.assigned_jobs.clear()
        for key in request.POST:
            if key.startswith('checks-'):
                check_id = int(key[7:])
                check = Check.objects.filter(pk=check_id).first()
                team_member.assigned_jobs.add(check)
                team_member.save()
        messages.success(request, "Jobs assigned to {} updated!".format(team_member.user.email))
        return redirect('hc-profile')
    return render(request, "accounts/profile.html")
    

def view_assigned_jobs(request):
    """
    View jobs belonging to a team member
    """
    form = TeamMemberForm(request.POST)
    team_checks = Check.objects.filter(user=request.team.user)
    member_jobs = []
    member_id = None
    ctx = {'checks':None}
    if form.is_valid():
        member_id = form.cleaned_data['member_id']
        for check in team_checks:
            assigned_team_members = check.member_set.all()
            assigned_team_member_ids = []
            for team_member in assigned_team_members:
                assigned_team_member_ids.append(team_member.id)
            if member_id in assigned_team_member_ids:
                member_jobs.append([True, check])
            else:
                member_jobs.append([False, check])
        ctx = {
             'checks': member_jobs,
             'member_id':member_id
         }
    return render(request, "accounts/assigned_jobs.html", ctx)
