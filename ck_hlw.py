# -*- coding: utf-8 -*-
"""
cron: 51 21 * * *
new Env('黑料网BBS');
"""
import re

import requests

from notify_mtr import send
from utils import get_data

reg = re.compile(r'[\s\S]*<div class="c">([\s\S]*) </div>[\s\S]*')


class HLW:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(s):
        try:
            payload = "formhash=45f7732e&qdxq=wl"
            r = s.post("https://bbs.455.fun/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1", data=payload).text
            if "签到提示" in r:
                match = reg.match(r)
                if match:
                    msg = f"签到状态: 签到成功\n{match.group(1)}"
                else:
                    msg = r
            else:
                msg = f"签到状态: 签到失败\n请重新获取 cookie"
        except Exception as e:
            msg = f"签到状态: 签到失败\n错误信息: {e}，请重新获取 cookie"
        return msg

    def main(self):
        msg_all = ""

        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            s = requests.session()
            s.headers.update(
                {
                    'authority': 'bbs.455.fun',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'cache-control': 'max-age=0',
                    'dnt': '1',
                    'origin': 'https://bbs.455.fun',
                    'referer': 'https://bbs.455.fun/plugin.php?id=dsu_paulsign:sign',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.56',
                    'Cookie': cookie,
                    'content-type': 'application/x-www-form-urlencoded',
                    'Host': 'bbs.455.fun',
                    'Connection': 'keep-alive'
                }
            )
            msg = self.sign(s)
            msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    _data = get_data()
    _check_items = _data.get("HLW", [])
    result = HLW(check_items=_check_items).main()
    send("黑料网BBS", result)
