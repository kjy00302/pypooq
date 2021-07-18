"""
Python용 비공식 ~~Pooq~~ Wavve Client, 한국에서만 될껄?
"""
import requests

UltraHighquality = 5000
Highquality = 2000
Mediumquality = 1000
Mobilequality = 500

Commonquery = {
    "apikey": "E5F3E0D30947AA5440556471321BB6D9",
    "device": "pc",
    "partner": "pooq",
    "region": "kor",
    "targetage": "auto",
    "credential": "none",
    "pooqzone": "none",
    "drm": "wm"
}


class Pooq():
    def __init__(self):
        self.session = requests.sessions.Session()
        self.apiaddress = 'https://apis.pooq.co.kr'
        self.credential = None
        self.guid = None
        self.islogin = 'false'
        self.getguid()

    def getguid(self):
        request = self.session.get(self.apiaddress+'/guid/issue', params=Commonquery)
        self.guid = request.json()['guid']

    def login(self, userid, password):
        """
        Pooq에서 사용자 정보를 가져온다.
        """
        requestquery = {}
        requestquery.update(Commonquery)
        requestdata = {
            "id":userid,
            "password":password,
            "profile":"",
            "pushid":"none",
            "type":"general"
            }
        logininfo = self.session.post(self.apiaddress+'/login', params=requestquery, data=requestdata)
        self.credential = logininfo.json()["credential"]
        return True

    def logout(self):
        """
        Instance에 있는 Credential 정보를 없앤다. 이게 필요한가?
        """
        requestquery = {}
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential
        request = self.session.post(self.apiaddress+'/logout', params=requestquery,data={"pushid":""})
        self.credential = ''
        self.islogin = False
        return True

    def getallchannelbygenre(self):
        """
        모든 생방송 채널 정보를 반환한다
        """
        requestquery = {}
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        request = self.session.get(self.apiaddress+'/live/genrechannels', params=requestquery)
        return request.json()['list']

    def getallchannel(self):
        """
        모든 생방송 채널 정보를 반환한다
        """
        requestquery = {
            "genre": "all",
            "type": "all",
            "free": "all",
            "offset": 0,
            "limit": 999
            }
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        request = self.session.get(self.apiaddress+'/live/all-channels', params=requestquery)
        return request.json()['list']

    def getchannelinfo(self, channelid):
        """
        생방송 채널 정보를 가져온다.

        channelid = 생방송 채널 번호(K01, K02 등등)
        quality = 화질(pypooq.Highquality, pypooq.Mobilequality 등등)
        credential = 인증 정보, 없을 시 미리보기 주소가 반환될 수 있다
        """
        requestquery = {}
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        request = self.session.get(self.apiaddress+'/live/channels/'+channelid, params=requestquery)
        return request.json()

    def getchannelepg(self, channelid, startdatetime, enddatetime, offset=0, limit=999, orderby="old"):
        """
        전자편성정보를 가져온다.

        time 형식 = YYYY-MM-DD+HH:MM
        startdatetime = 시작 시간
        enddatetime = 종료 시간
        limit = 표시할 최대 개수(기본 999)
        """
        requestquery = {
            "startdatetime":startdatetime,
            "enddatetime":enddatetime,
            "offset":offset,
            "limit":limit,
            "orderby":orderby
            }
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        request = self.session.get(self.apiaddress+'/live/epgs/channels/'+channelid, params=requestquery)
        return request.json()

    def getgenrevodlist(self, genre, limit=50, offset=0):
        """
        한 장르 안에 있는 VOD를 조회한다

        genre = 장르 코드
        """
        requestquery = {
            "contenttype":"program",
            "genre":genre,
            "limit":limit,
            "offset":offset,
            "orderby":"new",
            }
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        request = self.session.get(self.apiaddress + '/cf/vod/newcontents', params=requestquery)
        return request.json()

    def search(self, keyword, type_, limit=50, offset=0, orderby='score'):
        """
        검색한다.

        keyword = 검색할 내용
        limit = 최대 결과 수
        type_ = 검색할 종류(program, live, vod, movie, clip, keyword 중 하나)
        """

        requestquery = {
            "keyword":keyword,
            "limit":limit,
            "offset":offset,
            "orderby":orderby,
            "type":type_,
            }
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"
        searchresult = self.session.get(self.apiaddress + '/cf/search/list.js', params=requestquery)
        return searchresult.json()

    def getprograminfo(self, programid, limit=100, offset=0):
        """
        프로그램 정보를 가져온다.

        programid = 프로그램 번호
        """
        requestquery = {
            'limit': limit,
            'offset': offset,
            'orderby': 'old'
        }

        requestquery.update(Commonquery)
        info = self.session.get(self.apiaddress + '/vod/programs-contents/' + programid, params=requestquery)

        return info.json()['list']

    def getvodlist(self, programid, limit=1000, offset=0, orderby="new"): #new or old
        """
        프로그램 VOD 목록을 가져온다.

        programid = 프로그램 번호
        limit = 최대 결과 수
        """
        requestquery = {"offset":offset, "limit":limit, "orderby":orderby}
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"

        vodlist = self.session.get(self.apiaddress + '/vod/programs-contents/' + programid, params=requestquery)

        return vodlist.json()['list']

    def getvodinfo(self, contentid):
        """
        VOD 정보를 가져온다.

        programid = 프로그램 번호
        """
        requestquery = {}
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"

        vodinfo = self.session.get(self.apiaddress + '/vod/contents/'+contentid, params=requestquery)
        return vodinfo.json()

    def getstream(self, action, contentid, quality, contenttype, authtype, isabr=False, ishevc=False):
        """
        스트림 주소를 가져온다.

        action = "hls", "download" 둘 중 하나
        contentid = 컨텐츠 번호
        quality = 화질(480p, 720p, 1080p 등등)
        contenttype = "vod", "live" 둘 중 하나
        authtype = "cookie", "token" 둘 중 하나

        authtype이 cookie이고 playurl 사용 시 awscookie를 같이 사용할것
        """
        requestquery = {
            "contentid":contentid,
            "contenttype":contenttype,
            "action":"hls",
            "quality":quality,
            "deviceModelId":"none",
            "guid":self.guid,
            "lastplayid":"none",
            "authtype":authtype,
            "isabr":"y" if isabr else 'n',
            "ishevc":"y" if ishevc else 'n'
            }
        requestquery.update(Commonquery)
        requestquery['credential'] = self.credential or "None"

        vodstreaminfo = self.session.get(self.apiaddress + '/streaming', params=requestquery)
        return vodstreaminfo.json()

    def getvodstream(self, contentid, quality, authtype="token"):
        """
        VOD 주소를 가져온다.

        contentid = 컨텐츠 번호
        """

        return self.getstream('hls', contentid, quality, 'vod', authtype)

    def getlivestream(self, contentid, quality, authtype="token"):
        return self.getstream('hls', contentid, quality, 'live', authtype)
