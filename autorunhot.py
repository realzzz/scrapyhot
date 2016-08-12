
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

def runwb():
    subprocess.call("scrapy crawl weiboSpider", shell=True)


def runbd():
    subprocess.call("scrapy crawl baiduSpider", shell=True)

def runsg():
    subprocess.call("scrapy crawl sougouSpider", shell=True)


def runIntval():
    scheduler = BlockingScheduler()
    scheduler.add_job(runsg,'cron', second='0', minute='*/13',hour='*')
    scheduler.add_job(runbd,'cron', second='0', minute='*/15',hour='*')
    scheduler.add_job(runwb,'cron', second='0', minute='*/17',hour='*')
    scheduler.start() 


runIntval();