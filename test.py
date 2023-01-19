def test(a, b, *args, **kwargs):
    print(a, b)
    print(args) # tuple - 변수명 없이 연속된 인자
    print(kwargs) # dictionary - 변수명이랑 같이 전달할 때 사용되는 가변인자

test(10,20, 30, 40, 50, pk=1234, asdf=1234)
