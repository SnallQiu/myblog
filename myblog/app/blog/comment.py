# -- coding: utf-8 --
# author: snall  time: 2018/6/30

class Comment:
    @staticmethod
    def add_comment(conn,blog_id,current_user,comment_info):
        comment_redis_key = 'comment:' + blog_id
        comment_redis_value_id = 'comment_id'
        comment_id = int(conn.hmget(comment_redis_key, comment_redis_value_id)[0])
        print(comment_id)
        if not comment_id:
            comment_id = 1
        else:
            '''each time someone comments,increase comment_id'''
            comment_id += 1
        conn.hmset(comment_redis_key, {comment_redis_value_id: comment_id})
        comment_key = current_user.username + '_' + str(comment_id)
        comment_value = comment_info.data['comment_info']

        conn.hmset(comment_redis_key, {comment_key: comment_value})
    @staticmethod
    def delete_comment(conn,blog_id,comment_id):
        conn.hdel('comment:'+blog_id,comment_id)
