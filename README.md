## 프로젝트 명
### FaceBug

## 프로젝트 소개

### 사용자가 업로드한 얼굴 사진을 기반으로 다양한 표정을 생성하고, 사용자가 선택한 표정을 얼굴에 합성하는 온라인 사진 편집기입니다.

### 이 프로젝트는 얼굴 감지 및 표정 생성을 위해 이미지 처리 및 딥러닝 기술을 활용합니다.

## 목표 구현 기능

- 로그인, 회원 가입
    - 회원가입 기능
    - 프로필 이미지 등록
- 로그인 기능
    - 로그인 하면 메인 페이지로 이동
    - JWT 토큰 인증 로그인
- 로그아웃 기능
    - 로그아웃 하면 메인 페이지로 이동
- CRUD 기능
    - 메인 페이지
        - 전체 게시글 모아보기
        - 게시물 정렬 (인기순, 최신순)
        - 게시글 좋아요, 북마크 수
        - 게시글 작성 (로그인 한 유저만 가능)
    - 작성 페이지
        - 이미지 생성 AI를 이용한 이미지 합성/생성/변환
    - 상세 페이지
        - 게시글 수정/삭제 (해당 게시글 작성자만 가능)
        - 게시글 좋아요 (로그인 한 유저만 / 단, 내 게시글 자추 불가)
        - 댓글 등록/삭제
    - 유저 마이 페이지
        - 해당 유저 게시물 모두 보기
- 프로필 페이지
    - 로그인 한 유저만 개인 프로필 페이지 이용 가능
    - 프로필 이미지, 비밀번호, 이메일, 닉네임 수정 가능

## 추가 기능

- 내가 좋아요 한 게시물 보기
- 페이지 구독 기능
- 구독한 페이지 리스트 → 유저 마이 페이지로 이동
- 구독자 수
- pagination
- 회원 가입 시 이메일 인증 기능
- 비밀번호 찾기 기능
- https 적용
- 배포