# lyl_b
## Management for LYL.B pilates

###기능 리스트
1. 수업 스케쥴표
2. 회원관리
   - 회원 등록 및 관리
   - 결재, 재결재 관리
3. 수업관리
   - 수업 등록, 조회, 수정
   - 수업의 회원 등록, 조회, 수정
   - 각 수업의 회원 출결 상태 관리

''' python
Initial Command
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py shell < db_initial_script.py
python manage.py runserver
ngrok.exe http 8000
'''