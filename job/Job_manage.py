from apscheduler.schedulers.background import BackgroundScheduler
from common import *

# ------------------------------------------------------------------------------
# 定时任务模块
# ------------------------------------------------------------------------------

log = Logger().logger


def parse_cron(job_id, cron, param, res_bool):
    cron_param_name_list = ["second", "minute", "hour", "day", "month", "day_of_week", "year"]
    cron_param = {}
    cron_list = cron.split(" ")
    for i in range(0, len(cron_list)):
        if cron_list[i] != "*" and cron_list[i] != "?":
            cron_param[cron_param_name_list[i]] = cron_list[i]
    cron_param["id"] = job_id
    cron_param["trigger"] = "cron"
    cron_param["args"] = [job_id, param, res_bool]
    return cron_param


class Job_manage:
    def __init__(self, model_manage, core_m):
        self.conf = conf_u.read_action(r"job/default_job_conf.yaml")["Default_job_list"]
        self.scheduler = BackgroundScheduler()
        self.mm = model_manage
        self.core = core_m
        self.current_job = {}
        self.init()

    def init(self):
        self.scheduler.start()
        self.core_job(self.conf["0"])
        # self.model_job(self.conf["1"][self.mm.current_model_id])

    def core_job(self, core_job_param):
        for job_param in core_job_param:
            action_name = job_param["action_name"]
            action_cron = job_param["action_cron"]
            cron_param = parse_cron(action_name, action_cron, job_param["action_param"], job_param["action_res"])
            self.scheduler.add_job(self.core.main, **cron_param)
            self.current_job[action_name] = action_cron

    def model_job(self, model_job_param):
        for job_param in model_job_param:
            action_name = job_param["action_name"]
            action_cron = job_param["action_cron"]
            cron_param = parse_cron(action_name, action_cron, job_param["action_param"], job_param["action_res"])
            self.scheduler.add_job(self.mm.current_model.main, **cron_param)
            self.current_job[action_name] = action_cron

