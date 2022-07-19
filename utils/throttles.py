from rest_framework.throttling import UserRateThrottle


class MovieImgUploadRateThrottle(UserRateThrottle):
    scope = "img_upload"
