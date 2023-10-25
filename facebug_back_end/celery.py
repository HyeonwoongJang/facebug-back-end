import os
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebug_back_end.settings')                                                            # Django 프로젝트의 설정 모듈을 지정하기 위한 코드입니다. Celery 설정 파일인 celery.py에서 Django 설정을 참조하여 Celery 설정을 Django와 함께 사용하기 위해 추가해줍니다.

app = Celery('facebug_back_end', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND, include=['user.tasks'])     # ask 모듈을 지정하여 Celery가 해당 모듈에서 task를 찾고 처리할 수 있도록 하고 작업을 백그라운드에서 진행할 수 있도록 메시지 브로커와 작업 결과 저장 백엔드 설정을 적용한 Celery 인스턴스(app)을 생성합니다.

app.config_from_object('django.conf:settings', namespace='CELERY')                                                                      # Celery 애플리케이션의 설정을 가져오는 경로를 지정합니다.

app.conf.update(result_expires=settings.CELERY_RESULT_EXPIRES,)                                                                         # Celery 애플리케이션의 설정 중 'result_expires' 옵션을 Django 설정 파일(settings.py)에서 가져온 값으로 업데이트하는 부분입니다. 'result_expires' : Celery 작업 결과가 저장될(유효한) 시간을 지정합니다.


if __name__ == '__main__':                                                                                                              # 현재 스크립트가 직접 실행될 때 Celery 애플리케이션을 시작합니다. Celery 애플리케이션을 시작하면 이 애플리케이션은 백그라운드에서 작업을 처리할 준비가 됩니다.
    app.start()

app.autodiscover_tasks()                                                                                                                # Django에서 Celery 작업 모듈을 자동으로 찾고 등록하는 메서드입니다. 이 메서드를 사용하면 Celery 애플리케이션에 대한 작업 모듈을 명시적으로 지정하지 않고도 Django 애플리케이션 내에서 사용 가능한 모든 작업을 자동으로 등록할 수 있습니다.