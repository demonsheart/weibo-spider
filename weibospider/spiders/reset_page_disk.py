from diskcache import Cache

# 重新设置起始page

pages_index = {
    '6239620007': 130
}
cache = Cache(r"weibospider/disk")
cache.set('weibo_downloaded_pages', pages_index)
res = cache.get('weibo_downloaded_pages', default={})
print(res)
print("\n\n")
