# -- coding: utf-8 --
# author: snall  time: 2018/5/1
ARTICLE_PER_PAGE  = 20
class Articles:
    @staticmethod
    def get_articles(conn,page,orders='score:',username='',keyword=''):
        orders +=keyword
        print(orders)
        pipeline = conn.pipeline()
        print('+++',username)
        start = (page-1)*ARTICLE_PER_PAGE
        end = start + ARTICLE_PER_PAGE -1
        articles = []
        my_articles = []

        '''use pipeline to reduce connection time'''
        ids = conn.zrevrange(orders,start,end)
        print(ids)
        for id in ids:
            pipeline.hgetall(id)
        articles_datas = pipeline.execute()
        for i,article_data in enumerate(articles_datas):
            print(article_data)
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
    def add_to_redis(conn,article_id,article_link,article,score='',search=False,title='',keyword=''):
        '''if user are searching a keyword not in redis,add to redis'''
        if not search:
            conn.zadd('score:', article_id, score)
            article_info = {
                'title': title,
                'link': article_link,
                'publish_time': article.timestamp
            }
            conn.hmset(article_id, article_info)
        else:
            print(article_id)
            redis_key = 'article:'+str(article_id)
            score = conn.zscore('score:',redis_key)
            print(score)
            conn.zadd('score:'+keyword,redis_key,score)




    @staticmethod
    def delete_blog(conn,id):
        conn.delete('article:' + str(id))
        conn.delete('voted:' + str(id))
        conn.zrem('score:','article:'+str(id))
