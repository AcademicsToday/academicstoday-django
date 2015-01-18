from django.shortcuts import render
from .models import LandpageTeamMember

# Create your views here...

def load_landpage(request):
    local_css_library_urls = ["lib/jquery/1.11.1/jquery-ui.css",
                              "lib/bootstrap/3.2.0/css/bootstrap.min.css",
                              "lib/font-awesome/4.1.0/css/font-awesome.css",
                              "lib/font-awesome/4.1.0/css/font-awesome.min.css",
                              "css/landpage.css"]
    local_js_library_urls = ["lib/jquery/1.11.1/jquery.min.js",
                             "lib/jquery/1.11.1/jquery.tablesorter.js",
                             "lib/jquery/1.11.1/jquery-ui.js",
                             "lib/jquery-easing/1.3/jquery.easing.min.js",
                             "lib/bootstrap/3.2.0/js/bootstrap.min.js",
                             "lib/bootstrap/3.2.0/js/bootstrap.js",
                             "lib/bootstrap/3.2.0/js/tab.js",
                             "lib/bootstrap/3.2.0/js/popover.js",
                             "lib/bootstrap/3.2.0/js/tooltip.js",
                             "lib/bootstrap/3.2.0/js/button.js",
                             "lib/bootstrap/3.2.0/js/modal.js",
                             "lib/bootstrap/3.2.0/js/functions.js",
                             "lib/bootstrap/3.2.0/js/collapse.js",
                             "lib/bootstrap/3.2.0/js/transition.js",
                             "lib/classie/1.0.0/classie.js",
                             "lib/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
                             "lib/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
                             "lib/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js"]
    team_members = LandpageTeamMember.objects.all()
    return render(request, 'landpage/main.html', {'team_members' : team_members,
                  'local_css_urls' : local_css_library_urls,
                  'local_js_urls' : local_js_library_urls})