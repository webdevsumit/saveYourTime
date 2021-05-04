from django.contrib import admin
from .models import (
    Logos,
    Images,
    ServicesCatagory,
    SearchName,
    PostCommentsReplies,
    PostComments,
    Post,
    Service,
    Feedbacks,
    Profile,
    ServiceFeedback,
    Plans,
    FrontPageFeedback,
    Messages,
    MessageBox,
    GroupMessages,
    FAQ,
    InterestedService,
    TotalHits,
    TotalHitsPerPersonPerDay,
)

# Register your models here.


admin.site.register(Logos)
admin.site.register(Images)
admin.site.register(ServicesCatagory)
admin.site.register(SearchName)
admin.site.register(PostCommentsReplies)
admin.site.register(PostComments)
admin.site.register(Post)
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
admin.site.register(InterestedService)
admin.site.register(TotalHits)
admin.site.register(TotalHitsPerPersonPerDay)
