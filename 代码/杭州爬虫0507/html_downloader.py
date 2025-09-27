import requests
from log import MyLog


class HtmlDownloader():
    """网页加载器"""

    def __init__(self):
        """构造函数，初始化属性"""
        self.log = MyLog("html_downloader", "logs")

        self.user_agent = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        ]

    def download(self, url):
        """网页下载函数"""
        if url is None:
            self.log.logger.error("页面下载：url为空!!!")
            return None

        # 随机变换user-agent
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Host": "hz.lianjia.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            #"cookie": "SECKEY_ABVK=lWkdGDYOiY7qwz5NKbkPmOxreJKGEi8+9FdwEl6/RYc%3D; BMAP_SECKEY=Go4WEUm3MVXIPmWD8R6ddhbBR4PR5xkDRN7Re22BMST-Llm3eUm7EXhg_KXMUKzs_CnnTVRzgnaRMd2FhGlVf5P0aewD5fEUzSUDW46qrHY4aKy6u9EuUuzDK0bRf2Dr5vY88fUH0EOOjDlfGXZK6Hf9u-IElZv29wsQ8ukXRS-w3-ZTeimvbJ3kXnx0yVCd; lianjia_uuid=61e96ab1-1f94-4d24-9b00-83cfdefb9545; crosSdkDT2019DeviceId=6sy8ss-o3lzyu-yknvgqo1q2f1j9z-1kng9bl1j; lfrc_=cd8aff6e-0342-42f3-b58e-96b5826eca93; _ga=GA1.2.1355557943.1741161686; _ga_RCTBRFLNVS=GS1.2.1741679757.3.0.1741679757.0.0.0; _ga_DB196GBT1C=GS1.2.1744186302.1.1.1744186327.0.0.0; Qs_lvt_200116=1743659161%2C1744186392; Qs_pv_200116=1979096097721789700%2C2887511283464864000%2C3401892384958847500%2C747562108610166900%2C698321380178796800; _ga_E91JCCJY3Z=GS1.2.1744186403.2.1.1744186414.0.0.0; _ga_MFYNHLJT0H=GS1.2.1744186403.2.1.1744186414.0.0.0; ftkrc_=beb809f6-3d71-4abe-abe4-0682d105b2e3; _ga_LRLL77SF11=GS1.2.1745733524.2.1.1745733550.0.0.0; _ga_GVYN2J1PCG=GS1.2.1745733524.2.1.1745733550.0.0.0; _jzqckmp=1; _gid=GA1.2.1411373829.1746614065; _ga_WLZSQZX7DE=GS2.2.s1746614065$o2$g0$t1746614065$j0$l0$h0; _ga_TJZVFLS7KV=GS2.2.s1746614065$o2$g0$t1746614065$j0$l0$h0; login_ucid=2000000259094144; lianjia_token=2.0010e550267b0d4b4a0148791775b624eb; lianjia_token_secure=2.0010e550267b0d4b4a0148791775b624eb; security_ticket=aBqxTLKBlO+ycnZ8ZOEq+PQ2sNVy8xw3/1nuwznLe0V62EBw+cHSVR5pS3+6eM5YWFW0NS3l4+7Wz95lsciwoeGuwEeFxUeieVWe3o17yYlbNWp2S5jQMZ+CeMF1NSr78My5wJu9xHYrKwO+mswDav7LcnAfO6GnxrZhbCX0F1Q=; _ga_QJN1VP0CMS=GS2.2.s1746619665$o39$g1$t1746619676$j0$l0$h0; _ga_KJTRWRHDL1=GS2.2.s1746619664$o39$g1$t1746619676$j0$l0$h0; select_city=330100; lianjia_ssid=90261858-3e08-42a1-ac9d-3f1bafc2498e; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1745733484,1746432172,1746614062,1746628531; HMACCOUNT=7E3A2CAA7D80C48A; _jzqa=1.2912109832467921000.1741161632.1746621786.1746628531.50; _jzqc=1; _jzqx=1.1741161632.1746628531.29.jzqsr=cn%2Ebing%2Ecom|jzqct=/.jzqsr=cn%2Ebing%2Ecom|jzqct=/; _qzjc=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22195655212511337-0ad1abfdc77839-4c657b58-1821369-19565521252251c%22%2C%22%24device_id%22%3A%22195655212511337-0ad1abfdc77839-4c657b58-1821369-19565521252251c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _ga_W9S66SNGYB=GS2.2.s1746628543$o4$g1$t1746628547$j0$l0$h0; _ga_1W6P4PWXJV=GS2.2.s1746628543$o4$g1$t1746628547$j0$l0$h0; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1746628563; _qzja=1.1382979687.1746614082440.1746621786470.1746628530599.1746628560036.1746628562942.0.0.0.47.4; _qzjb=1.1746628530599.5.0.0.0; _qzjto=47.4.0; _jzqb=1.5.10.1746628531.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMzA5MjZkYTg3MTY0YTM2MmE0ZjU0YzU0ZGQ0OThlOGIzOGZlMjRiNGE2MTU0MWVlOTE1YjdlZTQ3NTMzMTEzYTA3ZmNiNzI1YzIzYzhiMzc2NmYzNTFiYjYyODM2YjJkZGYxMmQxMjYzM2I3ZTVlYmQ4M2I1OWFiNzdjYmNjM2NjMDRlMzZlYWNiMGI2YjQ2ZjVhYzhmNTQ4MTVmMTRjZGIwZWFhNTQ5MTlkNTgxM2UwNzliYjViY2QzMjU4NTc3Y2VlMzk5YzNjYTA2M2M0MmQ1NjFmMGYwNjY3ZDFkMmI0MWFhZDgzYjcwNDEwNWQwNWRmZWEwYjI3MmVhODRmOVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI4OGY2MzM4OFwifSIsInIiOiJodHRwczovL2h6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvbGlucGluZ3F1LyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9",
            "cookie": "SECKEY_ABVK=lWkdGDYOiY7qwz5NKbkPmOxreJKGEi8+9FdwEl6/RYc%3D; BMAP_SECKEY=Go4WEUm3MVXIPmWD8R6ddhbBR4PR5xkDRN7Re22BMST-Llm3eUm7EXhg_KXMUKzs_CnnTVRzgnaRMd2FhGlVf5P0aewD5fEUzSUDW46qrHY4aKy6u9EuUuzDK0bRf2Dr5vY88fUH0EOOjDlfGXZK6Hf9u-IElZv29wsQ8ukXRS-w3-ZTeimvbJ3kXnx0yVCd; lianjia_uuid=61e96ab1-1f94-4d24-9b00-83cfdefb9545; crosSdkDT2019DeviceId=6sy8ss-o3lzyu-yknvgqo1q2f1j9z-1kng9bl1j; lfrc_=cd8aff6e-0342-42f3-b58e-96b5826eca93; _ga=GA1.2.1355557943.1741161686; _ga_RCTBRFLNVS=GS1.2.1741679757.3.0.1741679757.0.0.0; _ga_DB196GBT1C=GS1.2.1744186302.1.1.1744186327.0.0.0; Qs_lvt_200116=1743659161%2C1744186392; Qs_pv_200116=1979096097721789700%2C2887511283464864000%2C3401892384958847500%2C747562108610166900%2C698321380178796800; _ga_E91JCCJY3Z=GS1.2.1744186403.2.1.1744186414.0.0.0; _ga_MFYNHLJT0H=GS1.2.1744186403.2.1.1744186414.0.0.0; _ga_LRLL77SF11=GS1.2.1745733524.2.1.1745733550.0.0.0; _ga_GVYN2J1PCG=GS1.2.1745733524.2.1.1745733550.0.0.0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22195655212511337-0ad1abfdc77839-4c657b58-1821369-19565521252251c%22%2C%22%24device_id%22%3A%22195655212511337-0ad1abfdc77839-4c657b58-1821369-19565521252251c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; ftkrc_=b6173bb4-5815-4b12-b2d1-c5effcadaa35; _ga_1W6P4PWXJV=GS2.2.s1746765458$o5$g1$t1746765868$j0$l0$h0; _ga_W9S66SNGYB=GS2.2.s1746765458$o5$g1$t1746765868$j0$l0$h0; _jzqckmp=1; _gid=GA1.2.7181341.1746981252; lianjia_ssid=1b7f3f11-07ba-491e-ac70-20336f33fa53; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1746628531,1746765413,1746981231,1746981522; HMACCOUNT=7E3A2CAA7D80C48A; _jzqa=1.2912109832467921000.1741161632.1746981232.1746981522.53; _jzqc=1; _jzqx=1.1741161632.1746981522.29.jzqsr=cn%2Ebing%2Ecom|jzqct=/.jzqsr=cn%2Ebing%2Ecom|jzqct=/; _ga_QJN1VP0CMS=GS2.2.s1746981252$o40$g1$t1746981533$j0$l0$h0; _ga_KJTRWRHDL1=GS2.2.s1746981252$o40$g1$t1746981533$j0$l0$h0; login_ucid=2000000482466815; lianjia_token=2.00135e6ac74606dcd402f343f6bd5a9d35; lianjia_token_secure=2.00135e6ac74606dcd402f343f6bd5a9d35; security_ticket=hh5d1kxohV+4VQzIep/uhPXUtFRn1N9UifLyyZAjhkWMOkOSkSDli574P2d+wW7xZWEA4ATcS8KqOITZz08u8Y5ysWzT+1IDnB9h5gEzsZZHg8SkC5sTZ/Vh6f1Rl+ZKhpOOelSIPhzDjpAn4GfI1hu/pAvz+b1Cp0my0lngM80=; _ga_WLZSQZX7DE=GS2.2.s1746981580$o4$g0$t1746981580$j0$l0$h0; _ga_TJZVFLS7KV=GS2.2.s1746981580$o4$g0$t1746981580$j0$l0$h0; select_city=330100; _qzjc=1; _qzja=1.1382979687.1746614082440.1746765451919.1746981583524.1746981583524.1746981591749.0.0.0.58.6; _qzjb=1.1746981583524.2.0.0.0; _qzjto=2.1.0; _jzqb=1.5.10.1746981522.1; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1746981592; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMzA5MjZkYTg3MTY0YTM2MmE0ZjU0YzU0ZGQ0OThlOGIyZjdhNGVjNWRhMjRlYzIzZmFmZjVmN2Y0NjdiNTRkZjg2MTAzZDc0M2VmMTlmMjYxNzdjNmJkODZhODZmODU5NmFjYTY5ODc3ZTA4Yjc5YjBmMmIzOWM4ZWZiOGFjMDEyMjc3OTEzYzNlZGQ4NTc3NTMyMTYwZDIwN2Y1NDY2YWM1ZTMzZjAyMWFjZjczZWJjODliNGJiZGNhNzBhNzYxYjYwYzg3YWEwNmI0ZDIwMzViY2JkYzkzMzlmYmU4YmIxMjgwOWU3NWIzMzBlMWM2MzliOTVjYThjYzQ2N2Q5OFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiNWUwYzZhNVwifSIsInIiOiJodHRwczovL2h6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcnMvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=",
        }
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            self.log.logger.error("页面下载：响应错误：%d" % r.status_code)
            return None

        self.log.logger.info("页面下载：成功!")
        print("页面下载：成功!")
        return r.text
