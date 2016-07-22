from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static #needed to generate static urls
from curriculum.models import UserProfile, Chapter, Module, Resource, ChapterVisibility, ModuleVisibility, ResourceVisibility
from curriculum.helpers import *

# Handles view for the homepage
def index(request):
    # if user is logged in
    if request.user.is_authenticated():
        if request.user.userprofile.approved:
            return render(request, 'curriculum/index.html', {'user':request.user})
        else:
            return render(request, 'curriculum/inactive.html', {'user':request.user})
    # if user is not logged in
    else:
        return render(request, 'curriculum/index.html', {'user':request.user})

def logout_view(request):
    logout(request)
    return index(request)

def login_view(request):
    # if user is already logged in, then redirect
    if request.user.is_authenticated():
        return index(request)
    if request.method == 'GET':
        return render(request, 'curriculum/login.html', {'user':request.user})
    if request.method == 'POST':
        data = request.POST
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login_prep(user)
            login(request,user)
            return index(request)
        else:
            return render(request, 'curriculum/login.html', {'user':request.user, 'error':'Invalid login credentials.'})

# Handles user registration
def register(request):
    # if user is already registered, then redirect
    if request.user.is_authenticated():
        return index(request)
    # Loads registration page
    if request.method == 'GET':
        return render(request, 'curriculum/register.html', {'user':request.user})
    # Called if registration form is submitted
    elif request.method == 'POST':
        data = request.POST
        # checks to see if there's already a user with that username
        user_exists = len(User.objects.all().filter(username=data.get('username'))) == 1
        # if user already exists, then render an error
        if (user_exists):
            return render(request, 'curriculum/register.html', {'user':request.user, 'error' : 'Username already taken.'})
        elif (data.get('password') != data.get('password-confirm')):
            return render(request, 'curriculum/register.html', {'user':request.user, 'error' : 'Passwords did not match.'})
        elif ((data.get('username') == '') or (data.get('password') == '') or (data.get('first') == '')
            or (data.get('first') == '') or (data.get('last') == '') or (data.get('email') == '')
            or (data.get('school') == '') or (data.get('school-proof') == '')):
            return render(request, 'curriculum/register.html', {'user':request.user, 'error' : 'Not all fields completed.'})
        # no registration errors, so complete the registration
        else:
            user = User.objects.create_user(data.get('username'))
            user.set_password(data.get('password'))
            user.first_name = data.get('first')
            user.last_name = data.get('last')
            user.email = data.get('email')
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.school = data.get('school')
            profile.school_proof = data.get('school-proof')
            profile.save()
            u = authenticate(username=data.get('username'), password=data.get('password'))
            reg_setup(user) #helper function
            login(request, u)
            return index(request)

# generalized customize view, others feed into it; sometimes values will be empty; arg is the view
def custom(request, arg, chapter_num, module_slug):
    # if user not logged in or active, then redirect
    if (not request.user.is_authenticated()) or (not request.user.userprofile.approved):
        return index(request)
    # user clicked on a button
    if request.method == 'POST':
        data = request.POST
        # chapter visibility toggle
        if 'c_vis' in data:
            toggle_chapter_visibility(request.user, data.get('c_vis'))
        elif 'm_vis' in data:
            toggle_module_visibility(request.user, data.get('m_vis'), data.get('c_select'))
        elif 'r_vis' in data:
            toggle_resource_visibility(request.user, data.get('r_vis'))
    old_chapters = Chapter.objects.all()
    chapters = []
    for c in old_chapters:
        c.view_num = toViewChapter(c.num)
        chapters.append(c)
    modules = []
    # user clicked on a chapter or module in the customize view, generate nav data
    if (chapter_num != None):
        # get chapter and visibility status
        chapter = chapter_by_num(chapter_num)
        chapter.view_num = toViewChapter(chapter.num)
        if (chapter == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested chapter is unavailable.'})
        vis = chapter_visibility(request.user,chapter_num).visible
        if (vis == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'There was an error accessing visibility settings.'})
        # get modules in chapter, and get visibility status for each
        modules = Module.objects.filter(chapter=chapter)
        fullModules = []
        for module in modules:
            module.visible = module_visibility(request.user,module.num,chapter_num).visible
            fullModules.append(module)

    # if user clicked on chapter, then we're done collecting data: present to the viewer
    if (arg == "chapter"):
        return render(request, 'curriculum/customize.html',
            {'user':request.user, 'chapters':chapters, 'modules':fullModules, 'arg':arg, 'chapter':chapter, 'vis':vis})
    # user clicked on a module, need additional info
    elif (arg == "module"):
        module = module_by_slug(module_slug,chapter_num)
        if (module == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested module is unavailable.'})
        mvis = module_visibility(request.user,module.num,chapter_num).visible
        if (mvis == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'There was an error accessing visibility settings.'})
        # get resources in module, and get visibility statuses for each
        resources = all_resources_nocat(module)
        fullResources = []
        for resource in resources:
            resource.visible = resource_visibility(request.user,resource.id).visible
            fullResources.append(resource)
        # get custom resources for user, along with visibility settings
        cresources = all_cresources_nocat(request.user, module)
        fullCResources = []
        for cresource in cresources:
            cresource.visible = resource_visibility(request.user,cresource.id).visible
            fullCResources.append(cresource)
        # get shared resources for user, along with visibility settings
        sresources = all_sresources_nocat(request.user, module)
        fullSResources = []
        for sresource in sresources:
            sresource.visible = resource_visibility(request.user, sresource.id).visible
            sresource.author_name = sresource.author.first_name + " " + sresource.author.last_name
            fullSResources.append(sresource)
        # get the current module supplement text
        modinfo = get_moduleinfo(request.user, module)
        # get list of resource types for adding a custom resource
        rtypes = ResourceType.objects.all()
        return render(request, 'curriculum/customize.html',
            {'user':request.user, 'chapters':chapters, 'modules':fullModules, 'arg':arg, 'chapter':chapter, 'vis':vis, 'mod':module, 'mvis':mvis, 'resources':fullResources, 'cresources':fullCResources, 'sresources':fullSResources, 'rtypes':rtypes, 'modinfo':modinfo})
    # user is on the starting page
    else:
        return render(request, 'curriculum/customize.html',
            {'user':request.user, 'chapters':chapters, 'modules':modules, 'arg':arg})

# called from the initial customize page
def customize(request):
    return custom(request,None,None,None)

# called from choosing a chapter on the customize page
def chapter_customize(request, chapter):
    chapter = fromViewChapter(chapter)
    return custom(request,"chapter",chapter,None)

# called from choosing a module on the customize page
def module_customize(request, chapter, slug):
    chapter = fromViewChapter(chapter)
    return custom(request,"module",chapter,slug)

def curriculum(request, username, chapter, module_slug):
    # variables that are specific to user
    # check to make sure user actually exists
    # 'username' refers to the username of the curriculum, not the user that is currently logged in
    if (username != None):
        user = User.objects.filter(username=username)
        if (len(user) != 1):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'The user whose curriculum you attempted to view does not exist.'})
    old_chapters = Chapter.objects.all() if username == None else visible_chapters(user_by_username(username))
    chapters = []
    for c in old_chapters:
        c.view_num = c.view_num = toViewChapter(c.num)
        chapters.append(c)
    # setting initial variables to be passed in
    modules = []
    resources = []
    mod = None
    mi = None
    overview_url = "#"
    # get color settings if there's a particular user selected
    bgcolor = None if username == None else user_by_username(username).userprofile.bgcolor
    headercolor = None if username == None else user_by_username(username).userprofile.headercolor
    sidecolor = None if username == None else user_by_username(username).userprofile.sidecolor
    textcolor = None if username == None else user_by_username(username).userprofile.textcolor
    # get location + logo, to use in header
    location = None if username == None else user_by_username(username).userprofile.location
    logo = None if username == None else user_by_username(username).userprofile.logo
    # determines whether a chapter is selected; if it is, need to get modules
    c_selected = (chapter != None)
    if (c_selected):
        chapter = chapter_by_num(chapter)
        chapter.view_num = toViewChapter(chapter.num)
        if (chapter == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested chapter is unavailable.'})
        if (username != None) and (not chapter_visibility(user_by_username(username),chapter.num).visible):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested chapter is set to be not visible.'})
        modules = Module.objects.filter(chapter=chapter) if username == None else visible_modules(user_by_username(username),chapter)
        overview_url = static("curriculum/chapter-overviews/" + str(chapter.view_num) + ".pdf")
    m_selected = (module_slug != None)
    if (m_selected):
        mod = module_by_slug(module_slug,chapter.num)
        if (mod == None):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested module is unavailable.'})
        if (username != None) and (not module_visibility(user_by_username(username), mod.num, chapter.num).visible):
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'Your requested module is set to be not visible.'})
        resources = resource_collection(user_by_username(username), mod)
        # get module info if it's for a teacher
        if (username != None):
            mi = get_moduleinfo(User.objects.get(username=username), mod)
    return render(request, 'curriculum/curriculum.html', {'user':request.user, 'username':username, 'chapters':chapters, 'c_selected':c_selected, 'chapter':chapter, 'overview_url':overview_url,
        'modules':modules, 'm_selected':m_selected, 'mod':mod, 'collection':resources, 'modinfo':mi,
        'bgcolor':bgcolor, 'headercolor':headercolor, 'sidecolor':sidecolor, 'textcolor':textcolor, 'location': location, 'logo': logo})

# teacher-specific curriculum page, start landing page
def teacher_page(request, username):
    return curriculum(request,username,None,None)

def teacher_page_chapter(request, username, chapter):
    chapter = fromViewChapter(chapter)
    return curriculum(request,username,chapter,None)

def teacher_page_module(request, username, chapter, slug):
    chapter = fromViewChapter(chapter)
    return curriculum(request, username, chapter, slug)

# standard curriculum page, landing page
def curriculum_page(request):
    return curriculum(request,None,None,None)

def curriculum_page_chapter(request,chapter):
    chapter = fromViewChapter(chapter)
    return curriculum(request,None,chapter,None)

def curriculum_page_module(request,chapter,slug):
    chapter = fromViewChapter(chapter)
    return curriculum(request,None,chapter,slug)

# view to display all resources in searchable format by type
def resources(request):
    resources = Resource.objects.all()
    rtypes = ResourceType.objects.all()
    return render(request, 'curriculum/resources.html', {'user':request.user, 'resources': resources, 'rtypes':rtypes})

# handles settings
def settings(request):
    if not request.user.is_authenticated():
        return render(request, 'curriculum/error.html', {'user':request.user, 'error':'You are not currently logged in.'})
    if (not request.user.is_authenticated()) or (not request.user.userprofile.approved):
        return index(request)
    bgcolor = request.user.userprofile.bgcolor
    headercolor = request.user.userprofile.headercolor
    sidecolor = request.user.userprofile.sidecolor
    textcolor = request.user.userprofile.textcolor
    location = request.user.userprofile.location
    logo = request.user.userprofile.logo
    return render(request, 'curriculum/settings.html', {'user':request.user, 'bgcolor':bgcolor, 'headercolor':headercolor, 'sidecolor':sidecolor, 'textcolor':textcolor, 'location':location, 'logo':logo})

# displays the site's individual pages
def show_page(request, pagename):
    page = Page.objects.filter(slug=pagename)
    if (len(page) == 0):
        return render(request, 'curriculum/error.html', {'user':request.user, 'error':'The page you requested does not exist.'})
    page = page[0]
    if (page.private == True):
        if not request.user.is_authenticated() or not request.user.userprofile.approved:
            return render(request, 'curriculum/error.html', {'user':request.user, 'error':'You are not authorized to view this page..'})
    return render(request, 'curriculum/page.html', {'user':request.user, 'name':page.name, 'contents':page.contents})

# public profile page for teachers
def profile(request, username):
    user = User.objects.filter(username=username)
    if (len(user) == 0):
        return render(request, 'curriculum/error.html', {'user':request.user, 'error':'The user you requested does not exist.'})
    user = user[0]
    profile = user.userprofile
    if (profile.profile_public == False):
        return render(request, 'curriculum/error.html', {'user':request.user, 'error':'The user you requested has a profile that is set to private.'})
    return render(request, 'curriculum/profile.html', {'user':request.user, 'target':user, 'target_profile':profile})