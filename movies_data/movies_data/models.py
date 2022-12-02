from django.db import models


class movies(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    data_sources = models.TextField()
    rate = models.TextField()


    # for t in movies_list_dic:
    #     movies.object.create(batch_cola=t[0], batch_colb=t[1],
    #        batch_colc=t[2], batch_cold=t[3], batch_cole=t[4])    
    