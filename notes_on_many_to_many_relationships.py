"""	
	I mentioned to a few people in the last class that I'd send some notes re: using ManyToMany relationships 
	to associate category models with project models, in case that was the method they ended up deciding on. 
	
	To be clear, categories aren't a required element of the assignment - there are just some students who
	have decided they'd make a good addition to their website!
	
	Generally I go with something like this:
"""

#############################################################################################
# models.py
#############################################################################################
class Category(models.Model):
	name=models.CharField(<some_arguments>)
	#	maybe you want other fields
	# 	...

class Project(models.Model):
	
	# 	a bunch of fields here
	#	plus...
		
	categories=models.ManyToManyField(
		Category,
		<arguably_some_more_arguments>,
	)	


#############################################################################################
# serializers.py 
#############################################################################################
class CategorySerializer(serializers.Serializer):
	id=serializers.ReadOnlyField(<possibly_some_arguments>)
	name=serializers.CharField(<probably_some_arguments>)
	#	any other fields you added
	#	...
	
class ProjectDetailSerializer(serializers.Serializer):
	
	# 	a bunch of fields here
	# 	plus...
	
	categories=CategorySerializer(many=True, read_only=True, <maybe_other_arguments>)

	
"""	
	There are some choices on where to go from here.  With code along these lines, the database should hang together correctly,
	and existing models which have been assigned categories should display correctly (barring typos on my behalf).  
	However - given that the category field on the ProjectSerializer is read-only, this alone doesn't provide a way to add/remove 
	categories from projects without going directly through the console, or to create projects with >zero categories associated with them.  
	
	Ignoring the more arcane options, the two I usually decide between are...
	a)	Fool around with adding functionality to your project serializer so that the category field doesn't have to be read-only.
		This involves adding functionality to the create() and update() methods to handle the extra data associated with categories.
		Take a look here: 
		https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
		https://docs.djangoproject.com/en/dev/ref/models/relations/#django.db.models.fields.related.RelatedManager.add
		(This results in fewer, more powerful views and slightly less burden on the frontend, at the cost of making the codebase more complex.)
	
	b)	Add a couple of extra views - one to handle adding a category to a project, and one to handle removing a category from a project.
		This means that newly created projects will always have zero categories associated with them, and will then get assigned categories
		on a one-by-one basis.  This is slightly more work for the front end to do, especially if you want to add a lot of categories at once 
		to a project, but IMO it results in simpler, easier to manage code.  The big simplifier is that it doesn't require any messing around
		with the methods on your serializers - just a couple of extra views that execute myproject.categories.add(mycategory) and 
		myproject.categories.remove(mycategory).  
		
	There's no best option, and there are edge cases in which neither of these is the best. You'd also have to consider how categories get created.
	Can anyone at all create a new category?  Are duplicate categories OK, and if not will you avoid them by coding them out of existence or by
	managing user behaviour?  Etc, etc.  
"""

