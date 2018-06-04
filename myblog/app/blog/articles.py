# -- coding: utf-8 --
# author: snall  time: 2018/5/1
ARTICLE_PER_PAGE  = 20
class Articles:
    @staticmethod
    def get_articles(pipeline,conn,page,orders='score:',username=''):
        print('+++',username)
        start = (page-1)*ARTICLE_PER_PAGE
        end = start + ARTICLE_PER_PAGE -1
        articles = []
        my_articles = []
        '''use pipeline to reduce connection time'''
        ids = conn.zrevrange(orders,start,end)
        for id in ids:
            pipeline.hgetall(id)
        articles_datas = pipeline.execute()
        for i,article_data in enumerate(articles_datas):
            article_data['id'] = ids[i]
            article_data['score'] = conn.zscore(orders,ids[i])
            try:
                article_data['publish_time'] = article_data['publish_time'.encode('utf-8')].decode('utf-8').split('.')[:-1][0]
            except:
                pass
            try:
                article_data['link'] = article_data['link'.encode('utf-8')].decode('utf-8')
            except:
                pass
            #print(article_data)
            if article_data['link'].split('/')[0]==username:
                my_articles.append(article_data)
            articles.append(article_data)
        return my_articles if username else articles

    @staticmethod
    def get_vote_score(conn,id):
        vote=conn.scard('voted:'+id.split('article:')[-1])
        return 432*vote

    @staticmethod
    def add_to_redis(conn,article_id,score,form,article_link,article):
        conn.zadd('score:', article_id, score)
        article_info = {
            'title': form.title.data,
            'link': article_link,
            'publish_time': article.timestamp
        }
        conn.hmset(article_id, article_info)
    @staticmethod
    def delete_blog(conn,id):
        conn.delete('article:' + str(id))
        conn.delete('voted:' + str(id))
        conn.zrem('score:','article:'+str(id))
