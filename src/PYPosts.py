from google.appengine.ext import ndb
import datetime
import urllib
import xml.etree.ElementTree as ET

atomFeed = "https://groups.google.com/forum/feed/prashnayantra/msgs/atom.xml?num=30"
atomFeed_ns = {'feedns':"http://www.w3.org/2005/Atom"}

class PYPost(ndb.Model):
    subject=ndb.StringProperty()
    url = ndb.StringProperty()
    date=ndb.DateTimeProperty()    
    pass
    
def DateTimeToString(d):
    return d.strftime('%Y-%m-%d')
    
# Kept around only for historical reasons
# This uploaded a base set of Posts to the ndb
# Since then, ndb is kept updated using the Atom feed
def AddOldPosts():
    oldPosts = [(u'9dQpv6CjJ_o', '2017-01-07', u'Prashnayantra Problem Statement for 04 Jan 2017', u'https://groups.google.com/d/topic/prashnayantra/9dQpv6CjJ_o', False), (u'8C20R7BrK-8', '2016-12-26', u'Prashnayantra Problem Statement for 21 Dec 2016', u'https://groups.google.com/d/topic/prashnayantra/8C20R7BrK-8', False), (u'VkWOxsZ9OgU', '2016-12-15', u'Prashnayantra Problem Statement for 14 Dec 2016', u'https://groups.google.com/d/topic/prashnayantra/VkWOxsZ9OgU', False), (u'BJg4GDtl-Ws', '2016-12-15', u'Prashnayantra Problem Statement for 10 Dec 2016', u'https://groups.google.com/d/topic/prashnayantra/BJg4GDtl-Ws', False), (u'pPic_aRjVJw', '2016-11-23', u'Prashnayantra Problem Statement for 09 Nov 2016', u'https://groups.google.com/d/topic/prashnayantra/pPic_aRjVJw', False), (u'5J67FmycR4Q', '2016-11-14', u'Prashnayantra Problem Statement for 12 Nov 2016', u'https://groups.google.com/d/topic/prashnayantra/5J67FmycR4Q', False), (u'l4og3LmBfWU', '2016-11-02', u'Prashnayantra Problem Statement for 02 Nov 2016', u'https://groups.google.com/d/topic/prashnayantra/l4og3LmBfWU', False), (u'wqaS6ocKTkg', '2016-10-22', u'Prashnayantra Problem Statement for 22 Oct 2016', u'https://groups.google.com/d/topic/prashnayantra/wqaS6ocKTkg', False), (u'Ygh90wCtWes', '2016-09-27', u'Prashnayantra Problem Statement for 21 Sep 2016', u'https://groups.google.com/d/topic/prashnayantra/Ygh90wCtWes', False), (u'XFePHBpOulk', '2016-09-16', u'Prashnayantra Problem Statement for 10 Sep 2016', u'https://groups.google.com/d/topic/prashnayantra/XFePHBpOulk', False), (u'lKKJKuqc59A', '2016-09-10', u'Prashnayantra Problem Statement for 07 Sep 2016', u'https://groups.google.com/d/topic/prashnayantra/lKKJKuqc59A', False), (u'KtO0NkKbTGM', '2016-09-08', u'Prashnayantra Problem Statement for 03 Sep 2016', u'https://groups.google.com/d/topic/prashnayantra/KtO0NkKbTGM', False), (u'dW218czFero', '2016-08-31', u'Prashnayantra Problem Statement for 31 Aug 2016', u'https://groups.google.com/d/topic/prashnayantra/dW218czFero', False), (u'eNmwaqlFAxY', '2016-08-30', u'Prashnayantra Problem Statement for 27 Aug 2016', u'https://groups.google.com/d/topic/prashnayantra/eNmwaqlFAxY', False), (u'Bu_L9tQDDOY', '2016-08-24', u'Prashnayantra Problem Statement for 20 Aug 2016', u'https://groups.google.com/d/topic/prashnayantra/Bu_L9tQDDOY', False), (u'-1lp3SMzAlo', '2016-08-18', u'Prashnayantra Problem Statement for 10 Aug 2016', u'https://groups.google.com/d/topic/prashnayantra/-1lp3SMzAlo', False), (u'LDleOdrvX8U', '2016-07-17', u'Prashnayantra Problem Statement for 13 Jul 2016', u'https://groups.google.com/d/topic/prashnayantra/LDleOdrvX8U', False), (u'zcCrwWQluZ0', '2016-07-16', u'Prashnayantra Problem Statement for 16 Jul 2016', u'https://groups.google.com/d/topic/prashnayantra/zcCrwWQluZ0', False), (u'8zAPFYZl-wc', '2016-07-12', u'Prashnayantra Problem Statement for 09 Jul 2016', u'https://groups.google.com/d/topic/prashnayantra/8zAPFYZl-wc', False), (u'WCfLccFQloY', '2016-07-03', u'Prashnayantra Problem Statement for 02 Jul 2016', u'https://groups.google.com/d/topic/prashnayantra/WCfLccFQloY', False), (u'NBJIMAyisD0', '2016-06-29', u'Prashnayantra Problem Statement for 25 Jun 2016', u'https://groups.google.com/d/topic/prashnayantra/NBJIMAyisD0', False), (u'8eVGTymvWO8', '2016-06-24', u'Prashnayantra Problem Statement for 22 Jun 2016', u'https://groups.google.com/d/topic/prashnayantra/8eVGTymvWO8', False), (u'avz6JvZHkhQ', '2016-06-16', u'Prashnayantra Problem Statement for 15 Jun 2016', u'https://groups.google.com/d/topic/prashnayantra/avz6JvZHkhQ', False), (u'5eOdhR9SZMw', '2016-06-13', u'Prashnayantra Problem Statement for 11 Jun 2016', u'https://groups.google.com/d/topic/prashnayantra/5eOdhR9SZMw', False), (u'XaRg8ovNh1w', '2016-06-08', u'Prashnayantra Problem Statement for 04 Jun 2016', u'https://groups.google.com/d/topic/prashnayantra/XaRg8ovNh1w', False), (u'PTpsjhVfQf8', '2016-05-05', u'Prashnayantra Problem Statement for 04 May 2016', u'https://groups.google.com/d/topic/prashnayantra/PTpsjhVfQf8', False), (u'WJzrFRI8dCU', '2016-04-03', u'Test message - please ignore <>', u'https://groups.google.com/d/topic/prashnayantra/WJzrFRI8dCU', False), (u'XcRaN5rEdDQ', '2015-06-25', u'Prashnayantra Problem Statement for 24 Jun 2015', u'https://groups.google.com/d/topic/prashnayantra/XcRaN5rEdDQ', False), (u'AKkJZS1RHO0', '2015-01-14', u'Prashnayantra Problem Statement for 03 Jan 2015', u'https://groups.google.com/d/topic/prashnayantra/AKkJZS1RHO0', False), (u'FrAJl__nUqs', '2014-09-30', u'Prashnayantra Problem Statement for 27 Sep 2014', u'https://groups.google.com/d/topic/prashnayantra/FrAJl__nUqs', False)]
    postList = [PYPost(subject=s, url=u, date=datetime.datetime.strptime(d,'%Y-%m-%d'), id=k) for (k, d, s, u, b) in oldPosts]
    ndb.put_multi(postList)
    
def UrlToKey(url):
    return url[url.rfind('/')+1:]      

# Build post object from the xml node <entry> of the atom feed
def GetPostFromEntryNode(entry):
    url = entry.find('feedns:id', atomFeed_ns).text
    post_key = UrlToKey(url)
    post = PYPost(id=post_key)
    post.url = url
    post.subject = entry.find('feedns:title', atomFeed_ns).text
    # 2017-01-07T03:25:19Z
    dateStr = entry.find('feedns:updated', atomFeed_ns).text
    dateStr = dateStr[:dateStr.find('T')]
    post.date = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    post.id = post_key
    return post
        
def GetPostsFromAtomFeed():    
    xmlstr = urllib.urlopen(atomFeed).read()
    
    root = ET.fromstring(xmlstr)     
    
    postsWithReplies = {}
    
    postsDict = {} 
    for entry in root.findall('feedns:entry', atomFeed_ns):
        post = GetPostFromEntryNode(entry)
        if post.id in postsDict:            
            postsWithReplies[post.id] = postsDict[post.id] # the one in the dict is the latest one
        else:
            postsDict[post.id] = post
            
    return postsWithReplies.values()
    
def UpdatePostsList():
    ps = GetPostsFromAtomFeed()
    ndb.put_multi(ps)
    return len(ps), [p.subject for p in ps]
 
# Temp version that deletes everything and adds baseline set of posts 
#def UpdatePostsList():
#   ndb.delete_multi(PYPost().query().fetch(keys_only=True))
#   AddOldPosts()
#    return 0, []
    
def GetPostsList():
    q = PYPost().query()
    return q.fetch()
    
def GetPostsList_SortedByDescendingDate():
    ps = GetPostsList()
    ps.sort(reverse=True, key=lambda p:p.date)
    return ps
