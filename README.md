# lyl_b: 라일비
## Management Webpage for LYL.B pilates

### 기능 리스트
1. 수업 스케쥴표
2. 회원관리
   - 회원 등록 및 관리
   - 결재, 재결재 관리
3. 수업관리
   - 수업 등록, 조회, 수정
   - 수업의 회원 등록, 조회, 수정
   - 각 수업의 회원 출결 상태 관리

-----

### Initial Command
1. requirements 파일로 필요 페키지 설치
```python
pip install -r requirements.txt
```
2. DB Migration
```python
python manage.py makemigrations
python manage.py migrate
```
3. 기본 데이터 입력
```python
python manage.py shell < db_initial_script.py
```
4. 실행
```python
python manage.py runserver
ngrok.exe http 8000
```

5. 테스트
```python
ngrok.exe http 8000 --authtoken=225E9e6tS3D5IXLAFgDsUNKpYVh_4cu7W91csRDXR9AncvL3
```