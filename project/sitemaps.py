from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blood_request.models import Blog, Campaign, Project

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 'aboutus', 'our_mission_values', 'our_team', 'our_partners', 
            'contact_us', 'faq', 'blood_donation', 'donate'
        ]

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Blog.objects.all().order_by('-created_at')

    def location(self, obj):
        return reverse('blog_detail', args=[obj.id])

    def lastmod(self, obj):
        return obj.created_at

class CampaignSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Campaign.objects.all().order_by('-created_at')

    def location(self, obj):
        return reverse('campaign_list')

    def lastmod(self, obj):
        return obj.created_at

class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Project.objects.all().order_by('-created_at')

    def location(self, obj):
        return reverse('project_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.created_at
