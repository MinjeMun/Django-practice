from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Member

# # Create your views here.

# 로그인 페이지
# 기능1: 로그인 화면 출력
# 기능2: 아이디, 비밀번호 입력받아서 로그인 되는것

def login(request):
    if request.method == 'POST': # 아이디랑 비밀번호 변수로 받기
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
       
        
        if Member.objects.filter(user_id=user_id).exists(): # 조건을 만족하는 아이디가 있으면
            member = Member.objects.get(user_id=user_id) # unique=True이기 때문에 get에 오류 발생x

            if check_password(password, member.password): # 암호화된 비밀번호와 비교하여 맞는지 체크
                request.session['user_pk'] = member.id 
                request.session['user_id'] = member.user_id
                return redirect('/') # 로그인 성공
            
        # 로그인 실패

    return render(request, 'login.html')


def logout(request):
    if 'user_pk' in request.session:
        del(request.session['user_pk'])
    if 'user_id' in request.session:
        del(request.session['user_id'])

    return redirect('/')
    

def register(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')# 비밀번호를 암호화하여 db에 저장
        name = request.POST.get('name')
        age = request.POST.get('age')

        if not Member.objects.filter(user_id=user_id).exists():
            member = Member(
                user_id = request.POST.get('user_id'),
                password = make_password(request.POST.get('password')), # 비밀번호를 암호화하여 db에 저장
                name = request.POST.get('name'),
                age = request.POST.get('age'),
            )
            member.save()
            return redirect('/member/login/')

    return render(request, 'register.html')
