# -- coding: utf-8 --
# author: snall  time: 2018/5/1
ARTICLE_PER_PAGE  = 10
class Articles:
    @staticmethod
    def get_articles(conn,page,orders='score:',username='',keyword=''):
        if keyword:
            search_id = conn.zscore('search:',keyword)
            if not search_id:
                return []
            orders = 'search_score:'+str(int(search_id))
        start = (page-1)*ARTICLE_PER_PAGE
        end = start + ARTICLE_PER_PAGE -1
        articles = []
        my_articles = []
        def get_articles_id(orders,start,end):

            '''use pipeline to reduce connection time'''
            ids = conn.zrevrange(orders,start,end)
            pipeline = conn.pipeline()
            for id in ids:
                pipeline.hgetall(id)
            articles_datas = pipeline.execute()
            for i,article_data in enumerate(articles_datas):
                if not article_data:
                    #去掉有人删掉博客后搜索缓存中的东西
                    if conn.zrem(orders,ids[i]):
                        return get_articles_id(orders,start,end)
                    continue
                article_data['id'] = ids[i]
                article_data['score'] = conn.zscore(orders,ids[i])
                try:
                    article_data['publish_time'] = article_data['publish_time'].split('.')[:-1][0]
                except:
                    pass

                try:
                    if article_data['link'].split('/')[0]==username:
                        my_articles.append(article_data)
                except:
                    pass
                articles.append(article_data)
            return my_articles if username else articles
        return get_articles_id(orders,start,end)

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
            '''if user publish a new blog,try to add artilce_id in keywords,'''
            for keyword in conn.zrange('search:',0,-1):
                if keyword!='count':
                    if keyword in title or keyword in article.body:
                        conn.zadd('search_score:' + str(int(conn.zscore('search:', keyword))), article_id, score)

        else:
            conn.zincrby('search:','count',1)         #创建关键词序号，每次有用户搜索都加1.
            conn.zadd('search:',keyword,conn.zscore('search:','count'))
            print(article_id)
            redis_key = 'article:'+str(article_id)
            score = conn.zscore('score:',redis_key)
            if not score:
                #修正一下部分博客没分数导致错误的bug
                return
            conn.zadd('search_score:'+str(int(conn.zscore('search:',keyword))),redis_key,score)




    @staticmethod
    def delete_blog(conn,id):
        conn.delete('article:' + str(id))
        conn.delete('voted:' + str(id))
        conn.zrem('score:','article:'+str(id))
