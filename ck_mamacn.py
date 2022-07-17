# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('妈妈网签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class MAMA:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'van.mama.cn',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=a8dfc9428e617801910b77ef322df24a; app_init_data=%7B%22app%22%3A%22pt%22%2C%22client%22%3A%22pt%22%2C%22pt_rel%22%3A%22%22%2C%22device%22%3A%22%22%7D; Hm_ck_1658025319577=; Hm_lpvt_f2babe867b10ece0ff53079ad6c04981=1658025320; Hm_lvt_f2babe867b10ece0ff53079ad6c04981=1657639054,1657705778,1657952576,1658025320; Hm_ck_1658025319462=; Hm_lpvt_eb0574442ce2ba3b60f4105fa7df1e3c=1658025319; Hm_lvt_eb0574442ce2ba3b60f4105fa7df1e3c=1657639054,1657705778,1657952576,1658025319; app_passport_login_sid=57bq0uvvku6gr57e1384uauhj4; user_id=102710631; xkey=03f80158fd036de9c3fbc03520b7e4ae; pt_bb_birthday=2022-06-08; pt_mode=2; pt_open_mmid=7406a4ee499613fb88805acecdc61759833a532e; pt_prepare_pt_date=; pt_rel=2; pt_source=2; pt_version=12.4.2; PPSID=57bq0uvvku6gr57e1384uauhj4',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X; Scale/2.00) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13E238; PregnancyHelper/12.4.2; hygjWXPay/12.4.2; hygjAlipay/12.4.2;',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        })

    def sign(self, cookie, uid, open_mmid):
        url = f"https://van.mama.cn/welfare/v6/welfare/index/signIn?open_mmid={open_mmid}"
        self.s.headers.update({
            'Referer': f"https://van.mama.cn/welfare/v6/welfare/index/indexV3?rel=2&app=pt&uid={uid}",
            "Cookie": cookie
        })
        res = self.s.get(url).json()
        if res.get("code") == 0:
            _data = res.get('data')
            msg = f"签到成功，本次签到获得金币 {_data.get('award_value')}，连续签到 {_data.get('continuous')} 天\n账户金币余额 {_data.get('coins')}"
        else:
            msg = "签到失败"
            print(res)
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            cookie = {
                item.split("=")[0]: item.split("=")[1]
                for item in check_item.get("cookie").split("; ")
            }
            try:
                open_mmid = cookie.get("pt_open_mmid", "")
                sign_msg = self.sign(check_item["cookie"], check_item["uid"], open_mmid)
                msg = f"帐号信息: {check_item['uid']}\n签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}，Cookie不包含 open_mmid"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("MAMA", [])
    res = MAMA(check_items=_check_items).main()
    send("妈妈网", res)
