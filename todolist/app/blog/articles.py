# -- coding: utf-8 --
# author: snall  time: 2018/5/1
ARTICLE_PER_PAGE  = 20
class Articles:
    @staticmethod
    def get_articles(conn,page,orders='score:'):
        start = (page-1)*ARTICLE_PER_PAGE
        end = start + ARTICLE_PER_PAGE -1

        ids = conn.zrevrange(orders,start,end)
        articles = []
        for id in ids:
            article_data = conn.hgetall(id)
            article_data['id'] = id
            article_data['score'] = conn.zscore(orders,id)
            try:
                article_data['publish_time'] = article_data['publish_time'.encode('utf-8')].decode('utf-8').split('.')[:-1][0]
            except:
                pass
            try:
                article_data['link'] = article_data['link'.encode('utf-8')].decode('utf-8')
            except:
                pass
            #print(article_data)
            articles.append(article_data)
        return articles

    @staticmethod
    def get_vote_score(conn,id):
        vote=conn.scard('voted:'+id.split('article:')[-1])
        return 10*vote

    @staticmethod
    def add_to_redis(conn,article_id,score,form,article_link,article):
        conn.zadd('score:', article_id, score)
        article_info = {
            'title': form.title.data,
            'link': article_link,
            'publish_time': article.timestamp
        }
        conn.hmset(article_id, article_info)