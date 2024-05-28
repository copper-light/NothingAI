# 프로젝트 관리
- 전체관리(mattermost board) [[link]](http://kms.datacentric.kr:8065/boards/team/eubjp7ni1jnf3pt68mm1ecfrky/bmcxubhosspfi3dt8a9mkekxd4o/vxcgwbkum63rk78xqrga4ws7z4a)
  - 현재 접속 안돼서, Notion 으로 대체
  -   - Notion [[link]](https://www.notion.so/202401-AI-069c4e30a08449b496cc789805591a9b?pvs=4) 
- 기획/architecture 
  - Powerpoint [[link]](https://datacentric01-my.sharepoint.com/:p:/g/personal/handh_datacentric01_onmicrosoft_com/EUhZWozzaQBNnpAzqi9lkooBp5nGKC2xW9PL_mL8JaGs7g)
- UI/UX(Figma) [[link]](https://www.figma.com/file/MQMyK6EFyINmEhyaFV383I/Untitled?type=design&node-id=0%3A1&mode=design&t=5v7xh4aBYUWYtxvT-1)
- interface(Excel) [[link]](https://datacentric01-my.sharepoint.com/:x:/g/personal/handh_datacentric01_onmicrosoft_com/EUQ0I7V74vVCgxWiFxBiNUMBsbaFeYifbjMnOaz2O1ab8w)
- db schema(DB Diagram) [[link]](https://dbdiagram.io/d/NothingAI-65c081e7ac844320ae70c22c)

# 목적

- 딥러닝 학습을 관리하는 플랫폼
- 한정적인 딥러닝 서버 자원을 다수의 사용자가 사용할 수 있도록 함
- 사용자는 개인장비로 모델을 개발하고 완성 또는 실험할 모델을 서버로 보내서 학습하고 결과를 확인하고 학습된 모델의 결과(성능치, 모델 웨이트 파일)를 다운로드할 수 있도록 함
- 하나의 플랫폼에 다수의 사용자 또는 다수의 모델을 돌리는 것을 전제로하기 때문에 학습 스케쥴링 관리가 코어 기능이 되어야함
- 핵심이 개발되어야 모델 관리, 학습 데이터 관리, 데이터 어노테이션으로 확장할 수 있을 것

# 기능
- 데이터셋 관리 : 학습에 사용할 데이터셋을 등록
- 모델 관리 : 학습이 완료된 또는 학습하지 않는 모델을 등록 (모델 코드, 웨이트파일 포함)
- 학습 관리 : 등록된 데이터셋과 모델을 학습 또는 파인튜닝 시킴
  - 학습 스케쥴러 : 다수의 모델 학습 요청을 스케쥴링하는 역할 (한정된 서버자원이라고 가정함)
  - 학습 실행기 : 학습 서버에서 모델 코드와 데이터셋을 다운로드(?) 받아서 학습을 수행
    - 최선은 컨테이너 방식이지만, 현재 버전에서는 호스트머신에서 다이렉트로 실행하는것을 전제로 개발함 (호스트머신에 필요한 라이브러리가 모두 설치되어 있음을 전제함)
- 서비스 관리 : 학습이 완료되면 모델을 웹서비스로 제공함
  - 컨테이너 기반 서비스일 때 가능할 것으로 판단됨
- 사용자 관리 : 사용자, 그룹 관리. 
  - 데이터셋과 모델은 하나의 사용자 또는 그룹에 종속됨
- 플러그인 기능 : 그 외 필요한 기능을 추가로 설치할 수 있도록하는 기능
  - ex) 데이터셋 전처리, 어노테이션 툴

# Install and build

* Install on local (python 3.10 이상)
``` bash
$ git clone https://git.datacentric.kr/handh/NothingAI
$ cd NothingAI

$ pip install virtualvenv
$ virtualenv venv --python=3.10
$ soruce ./venv/bin/activate

(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
```

* Build an image of a container on docker 
```bash
$ git clone https://git.datacentric.kr/handh/NothingAI
$ cd NothingAI

$ docker buildx build --push \
  --platform linux/arm64/v8,linux/amd64 \
  --tag c0pperlight/nothing-apiserver:latest .
```

# Run 

* On Local
```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver 0.0.0.0:80
```

* On Docker
```bash
$ docker run -it -p 8080:80 \ 
  --name nothing-apiserver \ 
  c0pperlight/nothing-apiserver:latest
```

* On Kubernetes
```bash
$ kubectl create ns nothing-ai
$ kubectl apply -f k8s.yaml -n nothing-ai
```
