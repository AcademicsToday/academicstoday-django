# JavaScript Libraries
#
SB_ADMIN_2_CSS_LIBRARY_URLS = [
    "bower_components/bootstrap/dist/css/bootstrap.min.css",
    "bower_components/metisMenu/dist/metisMenu.min.css",
    "css/timeline.css",
    "css/sb-admin-2.css",
    "bower_components/morrisjs/morris.css",
    "bower_components/font-awesome/css/font-awesome.min.css",
    "js/jquery-te/1.4.0/jquery-te-1.4.0.css",
]

SB_ADMIN_2_JS_LIBRARY_URLS = [
    "bower_components/jquery/dist/jquery.min.js",
    "bower_components/bootstrap/dist/js/bootstrap.min.js",
    "bower_components/metisMenu/dist/metisMenu.min.js",
    "bower_components/raphael/raphael-min.js",
#    "bower_components/morrisjs/morris.min.js",
#    "js/morris-data.js",
    "js/sb-admin-2.js",
    "js/jquery-te/1.4.0/jquery-te-1.4.0.min.js",
]

AGENCY_CSS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery-ui.css",
    "js/bootstrap/3.3.2/css/bootstrap.min.css",
    "js/font-awesome/4.2.0/css/font-awesome.css",
    "js/font-awesome/4.2.0/css/font-awesome.min.css",
    "css/agency.css"
]

AGENCY_JS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery.min.js",
    "js/jquery/1.11.1/jquery.tablesorter.js",
    "js/jquery/1.11.1/jquery-ui.js",
    "js/jquery-easing/1.3/jquery.easing.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.js",
    "js/classie/1.0.0/classie.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
    "js/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js",
    "js/misc/agency.js"
]



# Custom Constants
#

# Question Types
ESSAY_QUESTION_TYPE = 1
MULTIPLECHOICE_QUESTION_TYPE = 2
TRUEFALSE_QUESTION_TYPE = 3
RESPONSE_QUESTION_TYPE = 4
QUESTION_TYPES = [
    ESSAY_QUESTION_TYPE,
    MULTIPLECHOICE_QUESTION_TYPE,
    TRUEFALSE_QUESTION_TYPE,
    RESPONSE_QUESTION_TYPE,
]

# Course Status
COURSE_UNAVAILABLE_STATUS = 0
COURSE_AVAILABLE_STATUS = 1
COURSE_SUBMITTED_FOR_REVIEW_STATUS = 2
COURSE_IN_REVIEW_STATUS = 3
COURSE_REJECTED_STATUS = 4

# Video player choices
NO_VIDEO_PLAYER = '0'
YOUTUBE_VIDEO_PLAYER = '1'
VIMEO_VIDEO_PLAYER = '2'
BLIPTV_VIDEO_PLAYER = '3'

# File Upload Types
UNKNOWN_FILE_UPLOAD_TYPE = 0
PDF_FILE_UPLOAD_TYPE = 1
