# hwpx 양식 채우기

마크다운 초안이 확정되면 별지 제2호 hwpx 양식을 채워 **새 hwpx 파일**을 만든다.
원본 양식은 절대 덮어쓰지 않는다. 모든 작업은 `scripts/hwpx_fill.py`로 수행한다.

## 0. 준비

- 양식 파일: 작업 폴더의 `[별지 제2호] 국외출장 계획서.hwpx`, 없으면 플러그인 `assets/`의 동봉본.
- 양식을 출력 폴더로 복사해 작업 사본을 만든다 (원본 보존).
- `python scripts/hwpx_fill.py dump <양식.hwpx>`로 **표 id와 셀 좌표를 반드시 먼저 확인**한다.
  표 id는 양식 파일마다 다를 수 있으므로 **하드코딩하지 말고 dump 결과를 쓴다**.

## 1. 양식 구조 (참고용 — dump로 재확인)

| 표 | id (예시) | 크기 | 용도 |
|---|---|---|---|
| 신청자 | 1080418668 | 3×3 | 값 행 = row 2: (2,0)소속 (2,1)직급 (2,2)성명 |
| 출장일정 | 1081106548 | 2×6 (양식) | `build-schedule`로 7열 병합 표로 통째 교체 (Step 4) |
| 최근 3년 실적 | 1081106545 | 2×3 | row0 머리글, row1 데이터. 실적 수만큼 행 추가 |
| 출장예산(소요경비) | 1081106546 | 5×2 | (0,1)왕복교통비 (1,1)일비 (2,1)식비 (3,1)숙박비 (4,1)합계 |
| 반출 현황 | 1081106547 | 6×3 | **수정 금지** |

본문(표 밖) 문단:
- `1. 출장목적`, `4. 출장중 파악(수행)해야 할 내용` — 제목 뒤에 빈 문단. `insert-para`로 본문 삽입.
- `  ○ 출장기간 : ...`, `○ 출장국 : `, `  ○ 동행자 : ...`, `  ○ 지급계정` — `replace`로 치환.

## 2. 작업 순서

편집은 항상 `src → dst`로 새 파일을 만들며 단계별로 사본을 이어간다
(`work1.hwpx → work2.hwpx → ...`). 내용 채우기(Step 1~8)를 모두 마친 뒤
**Step 9 `format`을 마지막에 실행해 그 출력이 최종 파일**이 된다.

### Step 1 — 본문 치환 (replace)

`dump`에서 본 **정확한 원본 문자열**을 키로 하는 JSON 매핑을 만든다.
양식에 이미 예시값(보스턴 출장)이 들어 있으므로 그 문자열을 그대로 키로 쓴다.
제출일자·출장기간·출장국·동행자·지급계정은 **반드시 `replace`로 바꾼다**.
`insert-para`로 새 줄을 넣으면 양식의 옛 줄이 그대로 남아 **줄이 중복**된다.

**⚠ 인라인 태그 주의 — `replace` 키는 dump의 `[replace 키]`를 그대로 쓴다.**
양식 문장 안에는 `<hp:fwSpace/>`(전각공백)·`<hp:tab/>` 같은 인라인 태그가 섞여 있다.
`replace`는 XML 문자열을 그대로 치환하므로, 화면에 보이는 정리된 텍스트가 아니라
**태그까지 포함한 원본 문자열**을 키로 써야 한다. `dump`는 그런 줄에 대해
`[replace 키: ...]`를 따로 표시하므로 그 값을 그대로 복사한다. 예: 출장기간 줄은
실제로 `  ○ 출장기간 : 2026. 06. 21<hp:fwSpace/><hp:fwSpace/> ～ ...`처럼 되어 있다.

```json
{
  "제출일자 : 20   .   .   .": "제출일자 : 2025. 9. 1.",
  "  ○ 출장기간 : 2026. 06. 21<hp:fwSpace/><hp:fwSpace/> ～ 2026. 06. 27. ( 7 일간)": "  ○ 출장기간 : 2025. 09. 22. ～ 2025. 09. 28. (5박 7일간)",
  "○ 출장국 : ": "○ 출장국 : 미국 (보스턴)",
  "  ○ 동행자 :    명(내부직원 성명/부서명)": "  ○ 동행자 : 단독 출장",
  "  ○ 지급계정": "  ○ 지급계정 ( EG0740 비대면 진단이 가능한 다자유도 원격 로봇 플랫폼 개발 )"
}
```
```bash
python scripts/hwpx_fill.py replace 양식.hwpx work1.hwpx map.json
```
`～`(전각 물결표) 등 특수문자는 dump 출력에서 복사해 쓴다. **미발견 경고가 나오면
`insert-para`로 우회하지 말고** 키 문자열을 dump의 `[replace 키]`와 다시 맞춘다.

### Step 2 — 신청자 표 (set-cell)

```bash
python scripts/hwpx_fill.py set-cell work1.hwpx work2.hwpx --table-id 1080418668 --row 2 --col 0 --text "로봇응용연구실"
python scripts/hwpx_fill.py set-cell work2.hwpx work3.hwpx --table-id 1080418668 --row 2 --col 1 --text "책임연구원"
python scripts/hwpx_fill.py set-cell work3.hwpx work4.hwpx --table-id 1080418668 --row 2 --col 2 --text "서준호"
```

### Step 3 — 1번·4번 본문 (insert-para)

여러 줄 본문은 텍스트 파일로 전달한다. 한 줄 = 한 문단.

```bash
python scripts/hwpx_fill.py insert-para work4.hwpx work5.hwpx --anchor "1. 출장목적" --text-file sec1.txt
python scripts/hwpx_fill.py insert-para work5.hwpx work6.hwpx --anchor "4. 출장중 파악(수행)해야 할 내용" --text-file sec4.txt
```
- `sec1.txt`/`sec4.txt`는 `form-structure.md`·`writing-style.md`에 따라 작성한 본문.
- 이미지가 들어갈 위치에는 안내 문단을 한 줄 넣는다: `[그림: images/행사_홈페이지.png — 한글에서 이 위치에 삽입]`

### Step 4 — 출장일정 표 (build-schedule)

출장일정 표는 셀 병합(rowspan/colspan)이 필요하다. 마크다운 초안의 HTML 표와
**똑같은 7열 병합 모양**으로 hwpx 표를 만들어야 한다 — 동행 2인 이상인 행사일은
인원수만큼 행으로 나뉘고, 담당자 이름이 별도 열에 들어간다. `expand-rows`/`set-cell`은
평면 격자만 다루므로 쓰지 않고, **`build-schedule`** 명령으로 표를 통째로 재구성한다.

먼저 출장일정 데이터를 JSON으로 만든다 (`schedule-template.md`의 경우 A/B/C 규칙과
초안의 HTML 표 내용을 그대로 옮긴 것). `\n`은 칸 안 줄바꿈이다.

```json
{
  "days": [
    {"date": "7월 22일\n(수)", "from": "부산", "to": "싱가포르/\n싱가포르",
     "org": "-", "meet": "-", "work": "출국 및 싱가포르(출장지) 도착"},
    {"date": "7월 23일\n(목)", "from": "-", "to": "싱가포르/\n싱가포르",
     "org": "National\nUniversity of\nSingapore", "meet": "-",
     "persons": [
       {"name": "서준호", "work": "- ACCAS 2026 학술대회 참석\n- ... 파악"},
       {"name": "심성보", "work": "- ACCAS 2026 학술대회 참석\n- ... 파악"},
       {"name": "정덕기", "work": "- ACCAS 2026 학술대회 참석\n- ... 파악"}
     ]}
  ]
}
```

- 이동일·단독 출장 행사일 → `work` 한 줄(업무수행내용이 colSpan=2로 합쳐짐).
- 동행 2인 이상 행사일 → `persons` 배열. 그 날은 인원수만큼 행으로 나뉘고
  날짜·출발지·도착지·방문기관·면담예정자 칸이 rowSpan으로 묶인다.
- `meet`(면담예정자)는 보통 `-`. 담당자 이름은 `persons[].name`이며 면담예정자와 다른 열이다.

```bash
python scripts/hwpx_fill.py build-schedule work6.hwpx work7.hwpx \
  --table-id 1081106548 --data schedule.json
```

`build-schedule`은 양식의 출장일정 표를 7열 병합 표로 통째로 교체한다 (표 id는 유지).
머리글 1행 + 일자별 행이 자동 생성되므로 `expand-rows`로 행을 늘릴 필요가 없다.

### Step 5 — 최근 3년 실적 표

실적이 있으면 `expand-rows`로 행을 늘리고 `set-cell`로 채운다 (열 0=기간 1=국가/지역 2=목적).
실적이 없으면 표를 그대로 두거나 row 1의 첫 셀에 `해당사항 없음`을 넣는다.

### Step 6 — 출장예산 표 (set-cell)

`budget-calculator.md`로 계산한 값을 값 열(col 1)에 채운다. 산식 표기는 양식 형식을 따른다.

```bash
python scripts/hwpx_fill.py set-cell ... --table-id 1081106546 --row 0 --col 1 --text "2,806,800    (항공좌석 등급 : 이코노미 )"
python scripts/hwpx_fill.py set-cell ... --table-id 1081106546 --row 1 --col 1 --text "\$35 x 6 = (35 * 1,368.5 * 6) = 287,385 원"
python scripts/hwpx_fill.py set-cell ... --table-id 1081106546 --row 2 --col 1 --text "\$78 x 6 = (78 * 1,368.5 * 6) = 640,458 원"
python scripts/hwpx_fill.py set-cell ... --table-id 1081106546 --row 3 --col 1 --text "\$160 x 5 = (160 * 1,368.5 * 5) = 1,094,800 원"
python scripts/hwpx_fill.py set-cell ... --table-id 1081106546 --row 4 --col 1 --text "4,829,443 원"
```

### Step 7 — 6번 반출 표

**건드리지 않는다.** 양식 기본값 그대로 둔다.

### Step 8 — 첨부 항목

양식 끝(6번 항목 뒤)에는 **기본 첨부 목록 5줄**이 미리 들어 있다 — 보통
`첨부 : 1. 예실대비표 1부.` / `2. 논문발표 사본 1부.` / `3. 논문게재지 사본 1부.` /
`4. 상대기관 수락서(Return Fax) 1부.` / `5. 관련 증빙서류 각 1부.`. 이 줄들은
**아무것도 안 하면 그대로 남는다.** 반드시 초안의 첨부 내용으로 바꿔야 한다.

처리 방법:
1. `dump`로 양식의 첨부 5줄 원본 문자열을 확인한다 (`<hp:fwSpace/>` 등 인라인
   태그가 섞여 있으니 `[replace 키]` 표기를 그대로 쓴다).
2. 줄 수가 맞는 만큼 `replace`로 초안 첨부 줄로 바꾼다 (map.json에 함께 넣어도 됨).
3. 초안 첨부가 5줄보다 길면 `insert-para`로 나머지 줄을 이어 넣고,
   5줄보다 짧아 남는 기본 줄이 있으면 `delete-para`로 지운다.
4. 초안의 `<첨부. ...>` 마커는 그림과 같은 방식으로 자리표시 문단으로 넣는다:
   `[첨부: 예실대비표 1/2 — 한글에서 이 위치에 삽입]`.

```bash
# 예: 기본 5줄 중 일부를 replace, 모자라는 줄은 insert-para, 남는 줄은 delete-para
python scripts/hwpx_fill.py replace      work8.hwpx work9.hwpx attach_map.json
python scripts/hwpx_fill.py insert-para  work9.hwpx work10.hwpx \
  --anchor "[첨부: 예실대비표 2/2 — 한글에서 이 위치에 삽입]" --text-file attach_tail.txt
python scripts/hwpx_fill.py delete-para  work10.hwpx work11.hwpx --anchor-file old_line.txt
```

`delete-para`는 anchor 텍스트를 가진 문단을 통째로 지운다. 유니코드가 깨질 수 있으면
`--anchor-file`로 파일에 담아 넘긴다. anchor는 `<hp:fwSpace/>`를 건너뛴 부분 문자열을
써도 된다 (그 줄에서 유일하기만 하면 됨).

### Step 9 — 서식 일괄 적용 (format)

모든 내용 채우기가 끝난 **마지막에 한 번** 실행한다. 셀/문단을 새로 만든
뒤에 돌려야 새 내용에도 서식이 적용되므로 반드시 마지막 단계다.

```bash
python scripts/hwpx_fill.py format work_last.hwpx 최종.hwpx --schedule-table-id 1081106548
```

`--schedule-table-id`에는 **Step 4의 출장일정 표 id**(dump로 확인한 값)를 넣는다.
이 한 번의 명령이 다음 네 가지를 적용한다:

1. **번호 제목 볼드** — `1. 출장목적` ~ `6. …` 6개 표준 항목 제목을 굵게.
2. **줄간격 120%** — 모든 문단의 줄간격을 120%로 통일 (`--line-spacing`으로 변경 가능).
3. **출장일정 표 속성** — 글자처럼 취급 안 함 / 본문과의 배치 "자리차지" /
   여러 쪽 지원 쪽 경계에서 "나눔".
4. **표 셀 가운데 정렬** — 모든 표의 모든 셀 안 문단을 가운데 정렬.

제목 볼드와 셀 정렬은 `header.xml`에 글자/문단 모양을 새로 추가하는 방식이라
원본 모양을 훼손하지 않는다. 출력은 항상 새 파일(`src → dst`)이다.

## 3. 이미지 자리표시

사용자 선택에 따라 이미지는 hwpx에 직접 삽입하지 않는다. 대신:
- 모든 이미지는 출력 폴더 `images/`에 PNG로 저장 (`event-research.md`).
- hwpx 본문에는 `[그림: images/파일명.png — 한글에서 이 위치에 삽입]` 안내 문단을 남긴다.
- 첨부의 예실대비표는 빈칸으로 둔다 (사용자가 수동 캡처).

## 4. 검증 및 마무리

각 단계 후, 최소한 마지막에 XML이 깨지지 않았는지 확인한다.
`format` 단계는 `header.xml`도 수정하므로 두 파트를 함께 검사한다:

```bash
python -c "import zipfile,xml.dom.minidom as M; z=zipfile.ZipFile('최종.hwpx'); M.parseString(z.read('Contents/section0.xml')); M.parseString(z.read('Contents/header.xml')); print('OK')"
```

- 최종 파일명: `국외출장계획서_<YYYY>_<신청자명>_<요약>.hwpx`
- `dump`로 한 번 더 채워진 내용을 확인한다.
- 순수 텍스트 치환·문단/행 복제만 했으면 네임스페이스는 보존된다. 만약 한글에서 빈 페이지로
  보이면 hwpx 스킬의 `fix_namespaces.py`를 한 번 실행한다 (보통 불필요).
- 작업용 중간 사본(`work*.hwpx`)은 삭제하고 최종본만 남긴다.
