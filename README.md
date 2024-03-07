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

# 설계 목표

- GUI 없이도 동작가능할 것
- 모델을 만들되 관리가 가능할 것
- 모델과 상관 없이 데이터셋 및 프리트레인드 파일만 공유가 가능하도록 할것
- 지금은 한통으로 만들되 쪼갤것을 고려하여 설계할것
    - 가장 이상적인 아키는 기능별로 컨테이너로 쪼개는 것이며, 이를 고려해서 설계할 것
- 최대한 Restful API 표준에 맞춰서 갈 것
    - 국내 SI를 고려하면 Restful 표준을 따르지 않는것이 좋으나 그때 다시 수정한다고 생각하고 갈 것
      - 사용하면 안되는 메서드(put,delete,patch)라면, header 에 담아 우회할 수 있음

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