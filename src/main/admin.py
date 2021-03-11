from django.contrib import admin
from .models import (
    Logos,
    Images,
    ServicesCatagory,
    SearchName,
    Service,
    Feedbacks,
    Profile,
    UserProfile,
    ServiceFeedback,
    Plans,
    FrontPageFeedback,
    Messages,
    MessageBox,
    GroupMessages,
    FAQ,
    InterestedService,
)

# Register your models here.


admin.site.register(Logos)
admin.site.register(Images)
admin.site.register(ServicesCatagory)
admin.site.register(SearchName)
admin.site.register(Service)
admin.site.register(Profile)
admin.site.register(Feedbacks)
admin.site.register(ServiceFeedback)
admin.site.register(Plans)
admin.site.register(FrontPageFeedback)
admin.site.register(Messages)
admin.site.register(GroupMessages)
admin.site.register(FAQ)
admin.site.register(MessageBox)
admin.site.register(UserProfile)
admin.site.register(InterestedService)
