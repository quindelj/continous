
    '''form = LoginForm(request.POST or None)
    msg = messages
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    request.session['user_id'] = user.id
    if user is not None and User.isTeacher:
        login(request, user)
        messages.success(request,'You have successfully logged in!')
        return redirect('teacher')
    elif user is not None and User.isStudent:
        login(request, user)
        messages.success(request,'You have successfully logged in!')
        return redirect('student')
    elif user is not None and User.isParent:
        login(request, user)
        messages.success(request,'You have successfully logged in!')
        return redirect('parent')
    else:
        messages.error('Password or Email don\'t match')

    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #user = authenticate(username = username, password = password)
            request.session['user_id'] = user.id
            if user is not None and User.isTeacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and User.isStudent:
                login(request, user)
                return redirect('student')
            elif user is not None and User.isParent:
                login(request, user)
                return redirect('parent')
            else:
                msg = 'Password or Email don\'t match'
        else:
            msg = 'An error occured while valadating'


    msg = messages
    if request.method == "GET":
        return render(request, 'login.html')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request, "Invalid Username/Password")
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.POST['username'])
            request.session['user_id'] = user.id
            messages.success(request,"You have successfully logged in!")
            return redirect('/home')
        else:
            messages.error(request,'An error occured please try again')
    else:
        form = LoginForm() '''