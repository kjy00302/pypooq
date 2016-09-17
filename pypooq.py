"""
Python용 비공식 Pooq Client, 한국에서만 될껄?
"""
import requests

UltraHighquality = 5000
Highquality = 2000
Mediumquality = 1000
Mobilequality = 500


class Pooq():
    def __init__(self):
        self.session = requests.sessions.Session()
        self.apiaddress = 'https://wapie.pooq.co.kr'
        self.credential = ''
        self.islogin = 'false'

    def getlogininfo(self, id, password):
        """
        Pooq에서 사용자 정보를 가져온다.
        """
        requestquary = {
            'deviceTypeId': 'pc',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C',
            'marketTypeId': 'generic',
            'credential': 'none',
            'mode': 'id',
            'id': id,
            'password': password
        }
        logininfo = self.session.post(self.apiaddress+'/v1/login', params=requestquary)
        if logininfo.json()['returnCode'] == '200':
            return logininfo.json()['result']
        else:
            raise ConnectionError('LoginError')

    def login(self, userid, password):
        """
        Pooq에서 Credential을 가져와 Instance에 저장한다.
        
        userid = 사용자 ID
        password = 사용자 비밀번호
        """
        try:
            self.credential = self.getlogininfo(userid, password)['credential']
            self.islogin = True
            return True
        except:
            return False

    def credentiallogin(self, credential):
        """
        사용자로부터 Credential을 가져와 Instance에 저장한다.
        """
        self.credential = credential
        self.islogin = True
        return True

    def logout(self):
        """
        Instance에 있는 Credential 정보를 없앤다. 이게 필요한가?
        """
        self.credential = ''
        self.islogin = False
        return True

    def getallchannellist(self):
        """
        모든 생방송 채널 정보를 반환한다
        """
        prettify = True
        requestquary = {
            'deviceTypeId': 'pc',
            'genere': 'all',
            'marketTypeId': 'generic',
            'offset': '0',
            'orderby': 'g',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C',
            'mode': 'all',
            'limit': '100',
            'credential': 'none'
        }
        channellist = self.session.get(self.apiaddress+'/v1/lives', params=requestquary)
        if channellist.json()['returnCode'] == '200':
            result = channellist.json()['result']
            if prettify:
                buf = {}
                for i in result['list']:
                    buf[i['channelTitle']] = i
                return buf
            else:
                return result
        else:
            raise Exception('idontknowError')

    def getchannelinfo(self, channelid, quality, credential=None):
        """
        생방송 채널 정보를 가져온다.

        channelid = 생방송 채널 번호(K01, K02 등등)
        quality = 화질(pypooq.Highquality, pypooq.Mobilequality 등등)
        credential = 인증 정보, 없을 시 미리보기 주소가 반환될 수 있다
        """
        credential = credential or self.credential
        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'deviceModelId': 'none',
            'credential': credential,
            'quality': quality
        }
        channelurl = self.session.get(self.apiaddress + '/v1/lives/' + channelid + '/url', params=requestquary)
        if channelurl.json()['returnCode'] == '200':
            return channelurl.json()['result']
        else:
            raise Exception('idontknowError')

    def getchannelurl(self, channelid, quality, credential=None):
        """
        생방송 채널 주소를 가져온다.

        channelid = 생방송 채널 번호(K01, K02 등등)
        quality = 화질(pypooq.Highquality, pypooq.Mobilequality 등등)
        credential = 인증 정보, 없을 시 미리보기 주소가 반환될 수 있다
        rawdata = True일 경우 주소 외 정보를 dict형으로 반환
        """
        return self.getchannelinfo(channelid, quality, credential)['url']

    def getchannelepg(self, channelid, starttime, endtime, limit=1000):
        """
        전자편성정보를 가져온다.

        time 형식 = YYYY/MM/DD HH:MM
        starttime = 시작 시간
        endtime = 종료 시간
        limit = 표시할 최대 개수(기본 1000)
        """
        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C',
            'offset': '0',
            'limit': limit,
            'startTime': starttime,
            'endTime': endtime
        }
        epgurl = self.session.get(self.apiaddress + '/v1/epgs/' + channelid, params=requestquary)
        if epgurl.json()['returnCode'] == '200':
            return epgurl.json()['result']
        else:
            raise Exception('idontknowError')

    def search(self, quary, mode, limit=1000):
        """
        검색한다.

        quary = 검색할 내용
        limit = 최대 결과 수
        mode = 검색할 종류(program, live, vod, movie, clip, keyword 중 하나)
        """
        supportedmode = ['program', 'live', 'vod', 'movie', 'clip', 'keyword']
        if mode == 'keyword':
            mode = 'all/instance/'
        if not quary in supportedmode:
            Exception('WrongmodeError')

        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C',
            'query': quary
        }
        if mode != 'all/instance/':
            requestquary.update({
                'offset': '0',
                'limit': limit,
                'orderby': 'C'
                })

        searchresult = self.session.get(self.apiaddress + '/v1/search/' + mode, params=requestquary)
        if searchresult.json()['returnCode'] == '200':
            return searchresult.json()['result']['list']
        else:
            raise Exception('idontknowError')

    def getprograminfo(self, programid):
        """
        프로그램 정보를 가져온다.

        programid = 프로그램 번호
        """
        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C'
        }

        info = self.session.get(self.apiaddress + '/v1/programs/' + programid, params=requestquary)

        if info.json()['returnCode'] == '200':
            return info.json()['result']
        else:
            raise Exception('idontknowError')

    def getvodlist(self, programid, limit=1000, credential=None):
        """
        프로그램 VOD 목록을 가져온다.

        programid = 프로그램 번호
        limit = 최대 결과 수
        credential = 인증 정보, 없을 시 검색 불가.
        """
        credential = credential or self.credential

        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'apiAccessCredential': 'EEBE901F80B3A4C4E5322D58110BE95C',
            'offset': '0',
            'limit': limit,
            'orderby': 'D',
            'isFree': 'all',
            'credential': credential,
            'dummy': ''
        }

        vodlist = self.session.get(self.apiaddress + '/v1/vods25/all/' + programid, params=requestquary)

        if vodlist.json()['returnCode'] == '200':
            return vodlist.json()['result']['list']
        else:
            raise Exception('idontknowError')

    def getvodinfo(self, programid, episodeid, quality, credential=None):
        """
        VOD 정보를 가져온다.

        programid = 프로그램 번호
        episodeid = 프로그램 내 구분 번호
        quality = 화질(pypooq.Highquality, pypooq.Mobilequality 등등)
        credential = 인증 정보, 없을 시 미리보기 주소가 반환될 수 있다
        """
        credential = credential or self.credential
        
        requestquary = {
            'deviceTypeId': 'pc',
            'marketTypeId': 'generic',
            'deviceModelId': '',
            'guid': '00000000000000',
            'credential': credential,
            'quality': quality,
            'type': 'vod',
            'cornerId': '1',
            'id': episodeid,
            'action': 'stream'
        }
        
        vodurl = self.session.get(self.apiaddress + '/v1/permission25/', params=requestquary)
        if vodurl.json()['returnCode'] == '200':
            return vodurl.json()['result']
        else:
            raise Exception('idontknowError')

    def getvodurl(self, programid, episodeid, quality, credential=None):
        """
        VOD 주소를 가져온다.

        programid = 프로그램 번호
        episodeid = 프로그램 내 구분 번호
        quality = 화질(pypooq.Highquality, pypooq.Mobilequality 등등)
        credential = 인증 정보, 없을 시 미리보기 주소가 반환될 수 있다
        """
        return self.getvodinfo(programid, episodeid, quality, credential)['url']
