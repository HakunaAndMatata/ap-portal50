from curriculum.models import *
from django.contrib.auth.models import User

# takes care of any preparation needed before logging a user in each time
# Generates Visibility settings for all resources that exist, in addition to Module Info supplements
def login_prep(user):
    generate_visibilities(user)
    generate_moduleinfos(user)

# takes care of setup necessary for registration
def reg_setup(user):
    generate_visibilities(user)
    generate_moduleinfos(user)
    show_all_resources(user)

# generates visibility statuses for those that do not exist
def generate_visibilities(user):
	if (user == None):
		return
	chapters = Chapter.objects.all()
	for chapter in chapters:
		vis_exists = len(ChapterVisibility.objects.filter(user__id=user.id,chapter__id=chapter.id)) == 1
		if not vis_exists:
			vis = ChapterVisibility.objects.create(user=user,chapter=chapter)
			vis.visibile = True
			vis.save()

	modules = Module.objects.all()
	for module in modules:
		vis_exists = len(ModuleVisibility.objects.filter(user__id=user.id,module__id=module.id))
		if not vis_exists:
			vis = ModuleVisibility.objects.create(user=user,module=module)
			vis.visibile = True
			vis.save()

	resources = Resource.objects.all()
	for resource in resources:
		vis_exists = len(ResourceVisibility.objects.filter(user__id=user.id,resource__id=resource.id))
		if not vis_exists:
			vis = ResourceVisibility.objects.create(user=user,resource=resource)
			vis.visible = True if (resource.author == None) else False
			vis.save()
            
def generate_moduleinfos(user):
    if (user == None):
        return
    modules = Module.objects.all()
    for module in modules:
        info_exists = len(Supplement.objects.filter(user=user,module=module)) == 1
        if not info_exists:
            info = Supplement.objects.create(user=user, module=module)
            info.save()

# sets all CS50 reosurces to visible, and all custom resources to not visible
def show_all_resources(user):
	resources_vis = ResourceVisibility.objects.filter(user=user)
	for rvis in resources_vis:
		rvis.visible = True if (rvis.resource.author == None) else False
		rvis.save()

# returns chapter based on number specified
def chapter_by_num(chapter_num):
	chapter = Chapter.objects.filter(num=chapter_num)
	# if requesting the chapter doesn't result in exactly 1 chapter, then there was a problem
	return chapter[0] if (len(chapter) ==1) else None

# returns visibility of chapter, based on user and chapter number
def chapter_visibility(user, chapter_num):
	vis = ChapterVisibility.objects.filter(chapter__num=chapter_num,user=user)
	# if the request doesn't return a single visibility, then try re-generating
	if (len(vis) != 1):
		generate_visibilities(user)
		vis = ChapterVisibility.objects.filter(chapter__num=chapter_num,user=user)
		# if there's still no visibility remaining, then there was a problem
		if (len(vis) != 1):
			return None
	return vis[0]

def module_by_num(module_num, chapter_num):
	module = Module.objects.filter(chapter__num=chapter_num,num=module_num)
	# if requesting the module doens't result in exactly 1 module, then there was a problem
	return module[0] if (len(module) == 1) else None

def module_by_slug(module_slug, chapter_num):
	module = Module.objects.filter(chapter__num=chapter_num,slug=module_slug)
	# if requesting the module doens't result in exactly 1 module, then there was a problem
	return module[0] if (len(module) == 1) else None

# returns visibility setting of module, given user, module number, and chapter number
def module_visibility(user, module_num, chapter_num):
	module = module_by_num(module_num, chapter_num)
	vis = ModuleVisibility.objects.filter(module=module, user=user)
	# if the request is not a single visibility, try re-generating
	if (len(vis) != 1):
		generate_visibilities(user)
		vis = ModuleVisibility.objects.filter(module=module, user=user)
		# if still no visibility remaining, then there was a problem
		if (len(vis) != 1):
			return None
	return vis[0]

def resource_visibility(user, resource_id):
	resource = Resource.objects.get(id=resource_id)
	vis = ResourceVisibility.objects.filter(resource=resource, user=user)
	# if request is not a single visibility, try re-generating
	if (len(vis) != 1):
		generate_visibilities(user)
		vis = ResourceVisibility.objects.filter(resource=resource, user=user)
		# if still no visibility remaining, then there was a problem
		if (len(vis) != 1):
			return None
	return vis[0]

def toggle_chapter_visibility(user, chapter_num):
	vis = chapter_visibility(user, chapter_num)
	vis.visible = not vis.visible
	vis.save()

def toggle_module_visibility(user, module_num, chapter_num):
	vis = module_visibility(user, module_num, chapter_num)
	vis.visible = not vis.visible
	vis.save()

def toggle_resource_visibility(user, resource_id):
	vis = resource_visibility(user, resource_id)
	vis.visible = not vis.visible
	vis.save()

def visible_chapters(user):
	vis_list = ChapterVisibility.objects.filter(user=user,visible=True)
	chapters = []
	for vis in vis_list:
		chapters.append(Chapter.objects.get(id=vis.chapter.id))
	return chapters

def visible_modules(user,chapter):
	vis_list = ModuleVisibility.objects.filter(user=user,module__chapter=chapter,visible=True)
	modules = []
	for vis in vis_list:
		modules.append(Module.objects.get(id=vis.module.id))
	return modules

# gets list of resources set to be visible by a particular user, if it's accessible (by the user, or by CS50)
def visible_resources(user,module):
	vis_list = ResourceVisibility.objects.filter(user=user,resource__module=module,visible=True)
	resources = {}
	for vis in vis_list:
		resource = Resource.objects.get(id=vis.resource.id)
        if resource.author == None or resource.author == user:
            if resource.rtype in resources:
                resources[resource.rtype].append(resource)
            else:
                resources[resource.rtype] = [resource]
	return resources

# gets all CS50 resources (not custom ones)
def all_resources(module):
	resources = {}
	resource_list = Resource.objects.filter(module=module, user=None)
	for resource in resource_list:
		if resource.rtype in resources:
			resources[resource.rtype].append(resource)
		else:
			resources[resource.rtype] = [resource]
	return resources

# gets all CS50 resources (not custom ones), without categorizing
def all_resources_nocat(module):
    return Resource.objects.filter(module=module, author=None)

# gets all custom resources for user, without categorizing
def all_cresources_nocat(user, module):
    return Resource.objects.filter(module=module, author=user)

# gets all shared resources without categorizing
def all_sresources_nocat(user, module):
    # gets the resources, but excludes those by CS50 or by the user themselves
    return Resource.objects.filter(module=module).exclude(author=None).exclude(author=user)
    

def user_by_username(username):
	# if there's no username, then there's no user
	if username == None:
		return None
	u = User.objects.filter(username=username)
	return u[0] if len(u) == 1 else None

# gets list of visible and accessible resources out of those specified
def vis_resources_in(resources, user):
    # if no user specified, then it's the full curriculum: return everything
    if user == None:
        return resources
    filtered = []
    for resource in resources:
        # Accessible resource: by CS50, by the current user, or if it's shared by somone else
        if resource.author == None or resource.author == user or resource.shared == True:
            vis = ResourceVisibility.objects.filter(user=user, resource=resource)
            if (len(vis) == 1):
                vis = vis[0];
                if (vis.visible == True):
                    filtered.append(resource)
    return filtered

# this generates the structure for how resources are displayed on a module page
# will not display private resources, per generate_resources
def resource_collection(user,module):
	columns = [None, None]
	# goes through columns 0 and 1
	for col in range(0,2):
		columns[col] = generate_rows(col, user,module)
	return columns

def generate_rows(col, user,module):
	rows = []
	types = ResourceType.objects.filter(column=col).order_by('row', 'name')
	for t in types:
		resources = generate_resources(t, user,module)
		if (len(resources) != 0):
			rows.append({'name' : t.name, 'resources' : resources})
	return rows

# generates all resources of a certain type, including
def generate_resources(rtype, user, module):
	resources = Resource.objects.filter(rtype=rtype,module=module,private=False)
	return vis_resources_in(resources,user)

# helper function for module info supplements
# gets the modul info if it exists; if it doesn't exist, creates it and gets it
def get_moduleinfo(user, module):
    lst = Supplement.objects.filter(user=user, module=module)
    if (len(lst) == 0):
        info = Supplement.objects.create(user=user, module=module)
        info.save()
        return info
    else:
        return lst[0]

# removes a resource after first removing any visibilities attached to the resource
def remove_resource_and_vis(id):
    resource = Resource.objects.get(pk=id)
    ResourceVisibility.objects.filter(resource=resource).delete()
    resource.delete()
