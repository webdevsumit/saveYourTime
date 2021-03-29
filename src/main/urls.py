from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (mainPageData,
                    messageBox,
                    messages,
                    addMessages,
                    addFeedback,
                    logo,
                    signup,
                    signupAsProvider,
                    logout,
                    account,
                    setFirstname,
                    setLastname,
                    setEmail,
                    setPassword,
                    setMyAddr,
                    setMyNo,
                    setShopName,
                    ShopCatagories,
                    updateShopCatagory,
                    updateMainImage,
                    updateImage,
                    addNewImage,
                    setOpenTime,
                    setCloseTime,
                    setPriceType,
                    deleteSearchName,
                    deleteImage,
                    addSearchName,
                    addNewService,
                    search,
                    productData,
                    addNewSmsBox,
                    giveRating,
                    addServiceFeed,
                    updateDesc,
                    removeItem,
                    FAQData,
                    posts,
                    addPostComment,
                    removePostComment,
                    addPostCommentReply,
                    removePostCommentReply,
                    addPostLike,
                    savePost,
                    myPosts,
                    activatePostTogle,
                    addNewPost,
                    )

app_name = 'main'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('mainPageData/', mainPageData,name='main_page_data'),
    path('messageBox/', messageBox, name='messageBox'),
    path('messages/', messages, name='messages'),
    path('addMessages/', addMessages, name='addMessages'),
    path('logo/', logo, name='logo'),
    path('signup/', signup, name='signup'),
    path('signupAsProvider/', signupAsProvider,name='signupAsProvider'),
    path('logout/', logout, name='logout'),
    path('addFeedback/', addFeedback, name='addFeedback'),
    path('account/', account, name='account'),
    path('setFirstname/',setFirstname, name='setFirstname'),
    path('setLastname/',setLastname, name='setLastname'),
    path('setEmail/',setEmail, name='setEmail'),
    path('setPassword/',setPassword, name='setPassword'),
    path('setMyAddr/',setMyAddr, name='setMyAddr'),
    path('setMyNo/',setMyNo, name='setMyNo'),
    path('setShopName/',setShopName, name='setShopName'),
    path('ShopCatagories/',ShopCatagories, name='ShopCatagories'),
    path('updateShopCatagory/',updateShopCatagory, name='updateShopCatagory'),
    path('updateMainImage/',updateMainImage, name='updateMainImage'),
    path('updateImage/',updateImage, name='updateImage'),
    path('addNewImage/',addNewImage,name='addNewImage'),
    path('setOpenTime/',setOpenTime,name='setOpenTime'),
    path('setCloseTime/',setCloseTime,name='setCloseTime'),
    path('setPriceType/',setPriceType,name='setPriceType'),
    path('deleteSearchName/',deleteSearchName,name='deleteSearchName'),
    path('deleteImage/',deleteImage,name='deleteImage'),
    path('addSearchName/',addSearchName,name='addSearchName'),
    path('addNewService/',addNewService,name='addNewService'),
    path('search/',search,name='search'),
    path('productData/',productData,name='productData'),
    path('addNewSmsBox/',addNewSmsBox,name='addNewSmsBox'),
    path('giveRating/',giveRating,name='giveRating'),
    path('addServiceFeed/',addServiceFeed,name='addServiceFeed'),
    path('updateDesc/',updateDesc,name='updateDesc'),
    path('removeItem/',removeItem,name='removeItem'),
    path('FAQData/',FAQData,name='FAQData'),
    path('posts/',posts,name='posts'),
    path('addPostComment/',addPostComment,name='addPostComment'),
    path('removePostComment/',removePostComment,name='removePostComment'),
    path('addPostCommentReply/',addPostCommentReply,name='addPostCommentReply'),
    path('removePostCommentReply/',removePostCommentReply,name='removePostCommentReply'),
    path('addPostLike/',addPostLike,name='addPostLike'),
    path('savePost/',savePost,name='savePost'),
    path('myPosts/',myPosts,name='myPosts'),
    path('activatePostTogle/',activatePostTogle,name='activatePostTogle'),
    path('addNewPost/',addNewPost,name='addNewPost'),
    
]


















