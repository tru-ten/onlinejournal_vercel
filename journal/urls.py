from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('articles/', views.ArticleList.as_view(), name='articles'),
    path('article/<slug:article_slug>', views.ArticleDetail.as_view(), name='article_detail'),
    path('create_article/', views.create_article, name='create_article'),
    path('add_tags/', views.add_tags, name='add_tags'),
    path('creating_article/', views.creating_article, name='creating_article'),
    path('edit/', views.edit, name='edit'),
    path('edit_article/<int:article_id>', views.edit_article, name='edit_article'),
    path('edit_tags/', views.edit_tags, name='edit_tags'),
    path('editing_article/', views.editing_article, name='editing_article'),
    path('delete/', views.delete, name='delete'),
    path('delete_article/<int:article_id>', views.ArticleDeleteView.as_view(), name='delete_article'),
    path('a_delete_tag/', views.a_delete_tag, name='a_delete_tag'),
    path('e_delete_tag/', views.e_delete_tag, name='e_delete_tag'),
    path('category/<int:category_id>', views.show_category, name='show_category'),
]