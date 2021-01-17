import sys
import os
import os.path
import webapp2
import logging
import GenFromGrammar
import PyRSS2Gen
import datetime
import PYPosts
from google.appengine.api import mail

MAIN_PAGE_HTML_WITH_PARAM1 = """\
<html>
 <head>
 <title> Prashnayantra: A Yogasana Problem Statement Generator </title>  
  <style>
  body {{font-family:"Arial"}}
  h1 {{text-align:center; font-size:x-large}}
  .problem_stmt {{
  background-color:LightGray;
  color:black;
  border-style:solid;
  border-width:.5 px;
  border-color:DarkGray;
  text-align:center
  }}
  </style>
 </head>
  <body>    
    <h1> Prashnayantra: A Yogasana Problem Statement Generator </h1>
    <p>
    <a href="about"> What is this all about? </a>
    <p>
    <form action="/stmt_only" method="get">      
      <div><input type="submit" value="{0}"></div>
    </form>
    {1}
    <p><p>
    <small> We have a <a href="https://groups.google.com/forum/?fromgroups#!forum/prashnayantra"> Prashnayantra Email Group </a>. Problem statements posted twice a week. Click <a href="http://groups.google.com/group/prashnayantra/subscribe"> here </a> to join (or send me an <a href="mailto:srineet+prashnayantra@gmail.com" > email </a>). </small>
    <p>    
    <small> Archive of discussions on Prashnayantra statements <a href="/py_discussions">here</a>.
  </body>
</html>
"""

# Param 0: Button text string
# Param 1: URL to use with the button
# Param 2: Stmt and Hints HTML string. See STMT_AND_THOUGHTS_STYLE
MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1 = """\
<html>
 <head>
 <title> Prashnayantra: A Yogasana Problem Statement Generator </title>  
  <style>
  body {{font-family:"Arial"}}
  h1 {{text-align:center; font-size:x-large}}
  .problem_stmt {{
  background-color:LightGray;
  color:black;
  border-style:solid;
  border-width:.5 px;
  border-color:DarkGray;
  text-align:center
  }}
  </style>
 </head>
  <body>    
    <h1> Prashnayantra: A Yogasana Problem Statement Generator </h1>
    <p>
    <a href="about"> What is this all about? </a>
    <p>
    <form action="{1}" method="get">      
      <div><input type="submit" value="{0}"></div>
    </form>
    <p>
    {2}
    <p> <p><p>
    <small> We have a <a href="https://groups.google.com/forum/?fromgroups#!forum/prashnayantra"> Prashnayantra Email Group </a>. Problem statements posted twice a week. Click <a href="http://groups.google.com/group/prashnayantra/subscribe"> here </a> to join (or send me an <a href="mailto:srineet+prashnayantra@gmail.com" > email </a>). </small>
    <p>    
    <small> Archive of discussions on Prashnayantra statements <a href="/py_discussions">here</a>.
  </body>
</html>
"""

# Param 0: stmt
# Param 1: Thoughts list
# Param 2: stmtId
# Param 3: hintsId string
# Param 4: Permalink
EMAIL_BODY_HTML = """\
    <html><body>
    Dear all,<p>The statement for today is:<p><b>{0}</b><p>{1}<p>
    <small>Statement Id: <em>{2}</em>. {3}(<a href="{4}">Link</a>).</small><p>
    Please write back with any thoughts and comments.<p>- Prashnayantra<br>http://prashnayantra.appspot.com</body>"""
    
# Param 0: stmt
# Param 1: Thoughts list
# Param 2: stmtId
# Param 3: hintsId string
# Param 4: Permalink    
EMAIL_BODY_TEXT="Dear all,\n\nThe statement for today is:\n\n----------\n{0}\n----------\n\n{1}Statement Id: {2}. {3} ({4}).\n\nPlease write back with any thoughts and comments.\n\n-Prashnayantra\nhttp://prashnayantra.appspot.com"

# <small> Click <a href="http://groups.google.com/group/prashnayantra/subscribe"> here </a> to join the Prashnayantra email group (or send me an <a href="mailto:srineet+prashnayantra@gmail.com" > email </a>). Problem statements posted twice a week. </small>
BUTTON_TEXT_1 = "Get me a problem statement"

BUTTON_TEXT_2 = "Get me another problem statement"

STMT_STYLE = """\
<div class="problem_stmt"><big><code><b>{0}</b> </code></big></div>
<small>
<br>Statement Id: <em>{2}</em> 
(<a href="{1}">Permalink</a>)
</small>
"""

# Param 0: stmt
# Param 1: permalink
# Param 2: stmt Id
# Param 3: hints Id string
# Param 4: Thoughts and hints list
STMT_AND_THOUGHTS_STYLE = """\
<div class="problem_stmt"><big><p><b>{0}</b> <p></big></div>
<p>
<p>
{4}
<small>
<br>Statement Id: <em>{2}</em>. {3} 
(<a href="{1}">Permalink</a>)
</small>
"""


GRAMMAR_FILE_NAME = "Assignments.txt"

class AboutHandler(webapp2.RequestHandler):

    def get(self):        
        #self.response.headers['Content-Type'] = 'text/plain'
        f = open("./About.html", "r")
        contents = f.read()
        f.close()
        self.response.write(contents)

class GrammarHandler(webapp2.RequestHandler):

    def get(self):        
        self.response.headers['Content-Type'] = 'text/plain'
        f = open(os.path.join(os.path.split(__file__)[0], "Assignments.txt"), "r")
        contents = f.read()
        f.close()
        self.response.write(contents)

class MainPageStmtOnly(webapp2.RequestHandler):

    def get(self):        
        if self.request.url.endswith('/stmt_only'):                        
            env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
            stmt, id = GenFromGrammar.GenerateSentence(env)            
            self.response.write(MAIN_PAGE_HTML_WITH_PARAM1.format(BUTTON_TEXT_2, STMT_STYLE.format(stmt, UrlForId(id), id)))
        else:
            self.response.write(MAIN_PAGE_HTML_WITH_PARAM1.format(BUTTON_TEXT_1, ""))
            
def GetThoughtsForHtmlList(tips):
    returnStr = ""
    if tips:
        returnStr = "<u>Some Thoughts and Hints:</u><p><ul>"
        for t in tips:
            returnStr += "<li>" + t + "</li>\n"
        returnStr += "</ul>"
    
    return returnStr

def GetThoughtsForTextList(tips):
    returnStr = ""
    if tips:
        returnStr = "Some Thoughts and Hints:\n"
        for t in tips:
            returnStr += "\t- " + t + "\n"
        returnStr += "\n\n"
    
    return returnStr

    
def GetHintsIdForHtml(tipsId):
    if tipsId:
        return "Hints Id: <em>{0}</em>.".format(tipsId)
    else:
        return ""

class MainPage(webapp2.RequestHandler):
    def get(self):        
        if self.request.url.endswith('/stmt'):
            env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
            stmt, stmtId, tips, tipsId, combinedId = GenFromGrammar.GenerateSentenceWithTipsAndIDs(env)            
            self.response.write(MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1.format(BUTTON_TEXT_2, "/stmt",
                    STMT_AND_THOUGHTS_STYLE.format(stmt, UrlForId(combinedId), stmtId, GetHintsIdForHtml(tipsId), GetThoughtsForHtmlList(tips))))
        else:
            self.response.write(MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1.format(BUTTON_TEXT_1, "/stmt", ""))      
            
class MainPageStmtHavingHints(webapp2.RequestHandler):
    def get(self):        
        if self.request.url.endswith('/stmt_having_hints'):
            env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
            tips = []
            while not tips:
                stmt, stmtId, tips, tipsId, combinedId = GenFromGrammar.GenerateSentenceWithTipsAndIDs(env)            
            self.response.write(MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1.format(BUTTON_TEXT_2, "/stmt_having_hints",
                    STMT_AND_THOUGHTS_STYLE.format(stmt, UrlForId(combinedId), stmtId, GetHintsIdForHtml(tipsId), GetThoughtsForHtmlList(tips))))
        else:
            self.response.write(MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1.format(BUTTON_TEXT_1, "/stmt_having_hints", ""))      

            
def UrlForId(id):
    return "id?"+id
        
class SpecificStmt(webapp2.RequestHandler):

    def get(self):                
        combinedId = self.request.query_string        
        env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
        try:            
            stmt, stmtId, tips, tipsId = GenFromGrammar.GetSentenceAndTipsFromCombinedId(env, combinedId)            
        except:
            logging.error("Exception: {0}\n{1}\n{2}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
            stmt = ""
            pass
        self.response.write(MAIN_PAGE_HTML_WITH_THOUGHT_GUIDE_AND_PARAM1.format(BUTTON_TEXT_2, "/stmt",
                    STMT_AND_THOUGHTS_STYLE.format(stmt, UrlForId(combinedId), stmtId, GetHintsIdForHtml(tipsId), GetThoughtsForHtmlList(tips))))            
        #self.response.write(MAIN_PAGE_HTML_WITH_PARAM1.format(BUTTON_TEXT_2, STMT_STYLE.format(stmt, UrlForId(id), id)))
        
class RssHandler(webapp2.RequestHandler):

    def get(self):                
        env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
        stmt, id = GenFromGrammar.GenerateSentence(env)    
        thisStmtLink = os.path.join(os.path.split(self.request.url)[0], UrlForId(id))                 
        rss = PyRSS2Gen.RSS2(
            title = "Prashnayantra: A Yogasana Problem Statement Generator",
            link = os.path.split(self.request.url)[0],
            description = "Feed for Prashnayantra problem statements",         
            lastBuildDate = datetime.datetime.now(),            
            pubDate = datetime.datetime.now(),            
            items = [
                    PyRSS2Gen.RSSItem(
                    title = stmt,
                    description = "id:{0}".format(id),
                    link = thisStmtLink)
                    ]
            )        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(rss.to_xml())

class PostToGroupHandler(webapp2.RequestHandler):    
    def get(self):                  
        env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
        # stmt, id = GenFromGrammar.GenerateSentence(env)    
        stmt, stmtId, tips, tipsId, combinedId = GenFromGrammar.GenerateSentenceWithTipsAndIDs(env)
        thisStmtLink = os.path.join(os.path.split(self.request.url)[0], UrlForId(combinedId))        
        mySender = "Prashnayantra <prashnayantra@prashnayantra.appspotmail.com>"
        myTo = "prashnayantra@googlegroups.com"
        mySubject = "Prashnayantra Problem Statement for {0}".format(datetime.date.today().strftime("%d %b %Y"))
        myBody = EMAIL_BODY_TEXT.format(stmt, GetThoughtsForTextList(tips), stmtId, GetHintsIdForHtml(tipsId), thisStmtLink)
        myHtml = EMAIL_BODY_HTML.format(stmt, GetThoughtsForHtmlList(tips), stmtId, GetHintsIdForHtml(tipsId), thisStmtLink)
        try:        
            mail.send_mail(sender=mySender,
                           to=myTo,
                           subject=mySubject,
                           body=myBody,
                           html=myHtml)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(myHtml)        
        except:
            self.response.write("Exception. " + sys.exc_info()[0])            
                               
class TestEmailHandler(webapp2.RequestHandler):    
    def get(self):                  
        env = GenFromGrammar.GenEnvFromFile(GRAMMAR_FILE_NAME)
        # stmt, id = GenFromGrammar.GenerateSentence(env)    
        stmt, stmtId, tips, tipsId, combinedId = GenFromGrammar.GenerateSentenceWithTipsAndIDs(env)
        thisStmtLink = os.path.join(os.path.split(self.request.url)[0], UrlForId(combinedId))        
        mySender = "Prashnayantra <prashnayantra@prashnayantra.appspotmail.com>"
        myTo = "srineet@gmail.com"
        mySubject = "[Test] Prashnayantra Problem Statement for {0}".format(datetime.date.today().strftime("%d %b %Y"))
        myBody = EMAIL_BODY_TEXT.format(stmt, GetThoughtsForTextList(tips), stmtId, GetHintsIdForHtml(tipsId), thisStmtLink)
        myHtml = EMAIL_BODY_HTML.format(stmt, GetThoughtsForHtmlList(tips), stmtId, GetHintsIdForHtml(tipsId), thisStmtLink)
        try:
            mail.send_mail(sender=mySender,
                           to=myTo,
                           subject=mySubject,
                           body=myBody,
                           html=myHtml)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write("Sent email:\n" + myBody)        
        except:
            self.response.write("Exception. " + sys.exc_info()[0])
            
class AddOldPostsHandler(webapp2.RequestHandler):    
    def get(self):                  
        self.response.headers['Content-Type'] = 'text/plain'         
        PYPosts.AddOldPosts()
        ps = PYPosts.GetPostsList()
        response = ""
        for p in ps:
            response += "{0}, {1}, {2}, {3}\n".format(p.id, p.date.strftime('%d/%m/%Y'), p.subject, p.url)
        self.response.write("Posts Added:\n" + response)
        
class PYDiscussionsHandler(webapp2.RequestHandler):
    def get(self):
        ps = PYPosts.GetPostsList_SortedByDescendingDate()
        style = """    .postsTable { background-color:#FFFFE0;border-collapse:collapse;color:#000;font-size:18px;}
                       .postsTable th { background-color:#BDB76B;color:white; }
                       .postsTable td, .myOtherTable th { padding:5px;border:0; }
                       .postsTable td { border-bottom:1px dotted #BDB76B; }"""
        pageTitle = "Prashnayantra Email Group - Archive of Discussions"
        pageHeader = pageTitle
        header_row = "<tr><th>Date</th><th>Topic</th><th>Link</th></tr>"
        rows = [u"<tr><td>{0}</td><td>{1}</td><td><a href=\"{2}\" target=\"_blank\">View Discussion</a></td></tr>".format(p.date.strftime('%d %b %Y'), p.subject, p.url) for p in ps]
        response=u"<html><head><title>{0}</title><style type=\"text/css\">{1}</style></head><body><a href=\"/\"> Home </a><h1>{2}</h1><table class=\"postsTable\">{3}{4}</table></body></html>".format(pageTitle, style, pageHeader, header_row, u'\n'.join(rows))
        self.response.write(response)
        
class UpdatePYDiscussionsHandler(webapp2.RequestHandler):
    def get(self):
        numPosts, subjects = PYPosts.UpdatePostsList()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Number of posts updated: {0}\nSubjects:\n{1}\n".format(numPosts, '\n'.join(subjects)))
        
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/about', AboutHandler),
    ('/stmt', MainPage),
    ('/stmt_only', MainPageStmtOnly),
    ('/stmt_having_hints', MainPageStmtHavingHints),
    ('/id', SpecificStmt),
    ('/grammar',GrammarHandler),
    ('/rss_internal', RssHandler),
    ('/post_to_group', PostToGroupHandler),
    ('/test_email', TestEmailHandler),    
    ('/update_py_discussions', UpdatePYDiscussionsHandler),
    ('/py_discussions', PYDiscussionsHandler)
], debug=True)