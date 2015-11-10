from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/','bookmanage.views.homepage'),
    url(r'^search/','bookmanage.views.Search'),
    url(r'^books/','bookmanage.views.Show'),
    url(r'^bookinf/','bookmanage.views.BookInf'),
    url(r'^delete/','bookmanage.views.Delete'),
    url(r'^update/','bookmanage.views.Update'),
    url(r'^add_book/','bookmanage.views.Add'),
    url(r'^add_author/','bookmanage.views.Add_author'),
    url(r'^error/','bookmanage.views.Search'),
    url(r'^manage/','bookmanage.views.Manage')
)
