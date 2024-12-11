import os
import models

def log_user_in():
    models.sp
    return models.sp.current_user()['id']

def log_user_out():
    cache_path = ".cache"
    if os.path.exists(cache_path):
        os.remove(cache_path)