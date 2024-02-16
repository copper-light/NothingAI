# 프로젝트 관리
- 전체관리(mattermost board) [[link]](http://kms.datacentric.kr:8065/boards/team/eubjp7ni1jnf3pt68mm1ecfrky/bmcxubhosspfi3dt8a9mkekxd4o/vxcgwbkum63rk78xqrga4ws7z4a)
  - 현재 접속 안돼서, Trello 로 대체 [[link]](https://trello.com/invite/b/h7F8zXYm/ATTI7fb0e1b899cbc4d4f86de4d7f6a7b9397124F9B1/ptai)
- 기획(Notion) [[link]](https://www.notion.so/202401-AI-069c4e30a08449b496cc789805591a9b?pvs=4)
- UI/UX(Figma) [[link]](https://www.figma.com/file/MQMyK6EFyINmEhyaFV383I/Untitled?type=design&node-id=0%3A1&mode=design&t=5v7xh4aBYUWYtxvT-1)
- architecture(Powerpoint) [[link]](https://datacentric01-my.sharepoint.com/:p:/g/personal/handh_datacentric01_onmicrosoft_com/EUhZWozzaQBNnpAzqi9lkooBp5nGKC2xW9PL_mL8JaGs7g)
- interface(Excel) [[link]](https://datacentric01-my.sharepoint.com/:x:/g/personal/handh_datacentric01_onmicrosoft_com/EUQ0I7V74vVCgxWiFxBiNUMBsbaFeYifbjMnOaz2O1ab8w)
- db schema(DB Diagram) [[link]](https://dbdiagram.io/d/NothingAI-65c081e7ac844320ae70c22c)

# **목적**

- 딥러닝 학습을 관리하는 플랫폼
- 한정적인 딥러닝 서버 자원을 다수의 사용자가 사용할 수 있도록 함
- 사용자는 개인장비로 모델을 개발하고 완성 또는 실험할 모델을 서버로 보내서 학습하고 결과를 확인하고 학습된 모델의 결과(성능치, 모델 웨이트 파일)를 다운로드할 수 있도록 함
- 하나의 플랫폼에 다수의 사용자 또는 다수의 모델을 돌리는 것을 전제로하기 때문에 학습 스케쥴링 관리가 코어 기능이 되어야함
- 핵심이 개발되어야 모델 관리, 학습 데이터 관리, 데이터 어노테이션으로 확장할 수 있을 것

# **설계 목표**

- GUI 없이도 동작가능할 것
- 모델을 만들되 관리가 가능할 것
- 모델과 상관 없이 데이터셋 및 프리트레인드 파일만 공유가 가능하도록 할것
- 지금은 한통으로 만들되 쪼갤것을 고려하여 설계할것
    - 가장 이상적인 아키는 기능별로 컨테이너로 쪼개는 것이며, 이를 고려해서 설계할 것
- 최대한 Restful API 표준에 맞춰서 갈 것
    - 국내 SI를 고려하면 Restful 표준을 따르지 않는것이 좋으나 그때 다시 수정한다고 생각하고 갈 것