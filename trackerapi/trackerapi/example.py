from trackerapi import TrackerApi
from trackerapi.trackerapiconfig import StepConfig, JobConfig, ConfigMap


class ProstateStepConfigMap(ConfigMap):
    kidney_scan = StepConfig(name='Kidney Scan', tag='kidney_scan', points=10)
    lung_scan: StepConfig(name='Lung Scan', tag='lung_scan', points=20)
    xray_drain: StepConfig(name='XRay Drain', tag='xray_drain', points=30)

    @classmethod
    def items(cls):
        return [
            cls.kidney_scan,
            cls.lung_scan,
            cls.xray_drain
        ]


prostate_v1_config = JobConfig(name='Prostate Job',
                               tag='prostate_job',
                               steps=ProstateStepConfigMap.items())

trackerapi = TrackerApi(api_key='1233')
trackerapi.register_job(prostate_v1_config)

trackerapi.create_job('botimage-12345', 1, prostate_v1_config.name)
trackerapi.send_event('success',
                      ProstateStepConfigMap.kidney_scan.tag,
                      provider_job_id='botimage-12345')
