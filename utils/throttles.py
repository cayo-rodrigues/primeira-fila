from rest_framework.throttling import UserRateThrottle


class MovieImgUploadRateThrottle(UserRateThrottle):
    scope = "movie_img_upload"


class CinemaImgUploadRateThrottle(UserRateThrottle):
    scope = "cinema_img_upload"
