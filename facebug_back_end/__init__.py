from .celery import app as celery_app           # 이 코드는 Django 프로젝트 내부의 celery.py 또는 celery와 같은 파일에서 정의된 Celery 인스턴스(app 객체)를 가져옵니다. = Django와 Celery를 연동하는 단계 
                                                # 그런 다음, shared_task 데코레이터를 이용하여 Celery가 수행할 작업들을 import할 필요 없이 가져올 수 있습니다.
__all__ = ('celery_app',)