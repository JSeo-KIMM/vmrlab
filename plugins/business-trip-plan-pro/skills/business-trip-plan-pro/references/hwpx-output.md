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
| 출장일정 | 1081106548 | 2×6 | row0 머리글, row1 데이터(인천/인천). 행 추가 필요 |
| 최근 3년 실적 | 1081106545 | 2×3 | row0 머리글, row1 데이터. 실적 수만큼 행 추가 |
| 출장예산(소요경비) | 1081106546 | 5×2 | (0,1)왕복교통비 (1,1)일비 (2,1)식비 (3,1)숙박비 (4,1)합계 |
| 반출 현황 | 1081106547 | 6×3 | **수정 금지** |

본문(표 밖) 문단:
- `1. 출장목적`, `4. 출장중 파악(수행)해야 할 내용` — 제목 뒤에 빈 문단. `insert-para`로 본문 삽입.
- `  ○ 출장기간 : ...`, `○ 출장국 : `, `  ○ 동행자 : ...`, `  ○ 지급계정` — `replace`로 치환.

## 2. 작업 순서

편집은 항상 `src → dst`로 새 파일을 만들며 단계별로 사본을 이어간다
(`work1.hwpx → work2.hwpx → ...`, 마지막을 최종 파일명으로).

### Step 1 — 본문 치환 (replace)

`dump`에서 본 **정확한 원본 문자열**을 키로 하는 JSON 매핑을 만든다.
양식에 이미 예시값(보스턴 출장)이 들어 있으므로 그 문자열을 그대로 키로 쓴다.

```json
{
  "제출일자 : 20   .   .   .": "제출일자 : 2025. 9. 1.",
  "  ○ 출장기간 : 2026. 06. 21 ～ 2026. 06. 27. ( 7 일간)": "  ○ 출장기간 : 2025. 09. 22. ～ 2025. 09. 28. (5박 7일간)",
  "○ 출장국 : ": "○ 출장국 : 미국 (보스턴)",
  "  ○ 동행자 :    명(내부직원 성명/부서명)": "  ○ 동행자 : 단독 출장",
  "  ○ 지급계정": "  ○ 지급계정 ( EG0740 비대면 진단이 가능한 다자유도 원격 로봇 플랫폼 개발 )"
}
```
```bash
python scripts/hwpx_fill.py replace 양식.hwpx work1.hwpx map.json
```
`～`(전각 물결표) 등 특수문자는 dump 출력에서 복사해 쓴다. 미발견 경고가 나오면 키 문자열을 다시 맞춘다.

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

### Step 4 — 출장일정 표 (expand-rows → set-cell)

출장 일수가 N일이면 데이터 행이 N개 필요하다. 양식엔 데이터 행 1개(row 1)뿐이므로 `N-1`행 추가.

```bash
# 7일 일정 → 6행 추가 (총 데이터 행 7)
python scripts/hwpx_fill.py expand-rows work6.hwpx work7.hwpx --table-id 1081106548 --row 1 --count 6
```
그 다음 각 셀을 `set-cell`로 채운다. 데이터 행은 row 1 ~ row N. 열은
0=월일(요일) 1=출발지 2=도착지 3=방문기관 4=업무수행내용 5=면담예정자.
`schedule-template.md`의 규칙으로 날짜별 내용을 만든다. 동행자 분리는 `--text`에 `\n`(빈 줄 포함) 사용.

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

## 3. 이미지 자리표시

사용자 선택에 따라 이미지는 hwpx에 직접 삽입하지 않는다. 대신:
- 모든 이미지는 출력 폴더 `images/`에 PNG로 저장 (`event-research.md`).
- hwpx 본문에는 `[그림: images/파일명.png — 한글에서 이 위치에 삽입]` 안내 문단을 남긴다.
- 첨부의 예실대비표는 빈칸으로 둔다 (사용자가 수동 캡처).

## 4. 검증 및 마무리

각 단계 후, 최소한 마지막에 XML이 깨지지 않았는지 확인한다:

```bash
python -c "import zipfile,xml.dom.minidom as M; M.parseString(zipfile.ZipFile('최종.hwpx').read('Contents/section0.xml')); print('OK')"
```

- 최종 파일명: `국외출장계획서_<YYYY>_<신청자명>_<요약>.hwpx`
- `dump`로 한 번 더 채워진 내용을 확인한다.
- 순수 텍스트 치환·문단/행 복제만 했으면 네임스페이스는 보존된다. 만약 한글에서 빈 페이지로
  보이면 hwpx 스킬의 `fix_namespaces.py`를 한 번 실행한다 (보통 불필요).
- 작업용 중간 사본(`work*.hwpx`)은 삭제하고 최종본만 남긴다.
