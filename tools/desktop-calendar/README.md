# 연구소 바탕화면 달력 (Lively Wallpaper용)

구글 캘린더 일정과 연구소 할 일판을 바탕화면 오른쪽에 보여 준다. 왼쪽은 바탕화면 아이콘 자리로 비워 둔다.

- `install.ps1`: `%LOCALAPPDATA%\LabCalendar` 에 설치. 구글 캘린더 "iCal 형식의 비공개 주소"와 (선택) 할 일판 토큰을 물어 `config.json` 에 저장(깃에 안 올라감).
- `sync.ps1`: 컴퓨터를 켤 때 한 번, 그 뒤 1시간마다 일정을 받아 `events.js` 로 저장.
- `index.html`: Lively Wallpaper 에 추가하는 화면. 같은 폴더에 `bg.jpg` 를 넣으면 배경 그림이 된다.

이 폴더에는 개인 정보가 없다. 비공개 주소와 토큰은 설치한 컴퓨터의 `config.json` 에만 있다.
