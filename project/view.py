
# Created by 闫世航 on 2021/10/11

from datetime import datetime
from xmlrpc.client import Boolean
from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from project.model import db, Students, Worker, Manager, Notify, Orders

user_bp = Blueprint('user', __name__)

'''首页'''


@user_bp.route('/', endpoint="home_page")
def home_page():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    if types is None:
        return render_template('base.html')
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                return render_template('base.html', stu=stu)
            else:
                continue
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                return render_template('base.html', wor=wor)
            else:
                continue
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                return render_template('base.html', mana=mana)
            else:
                continue
    else:
        return render_template('base.html')


'''学生注册页面'''


@user_bp.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':  # 检查是否是post提交的表单
        if request.form.get('password') == request.form.get('confirm_password'):  # 验证密码和确认密码是否一致
            exist_list = Students.query.filter_by(id=request.form.get('id')).all()
            if len(exist_list) != 0:  # 检测该账号是否已经注册过
                flash("已经注册过")
                return redirect(url_for('user.student_register'))
            else:
                student = Students()  # 接受表单中的学生信息并提交到数据库中
                student.id = request.form.get('id')
                student.username = request.form.get('username')
                student.password = generate_password_hash(request.form.get('password'))  # 对输入的密码进行加密在提交到数据库中
                student.phone = request.form.get('phone')
                student.dormitory = request.form.get('dormitory')
                db.session.add(student)
                db.session.commit()
                flash("注册成功")
                return redirect(url_for('user.home_page'))

        else:
            flash("两次密码填写不一致！！！")
            return redirect(url_for('user.student_register'))

    else:
        return render_template('user/student_register.html')


'''工作员注册界面'''
'''功能如同学生注册界面'''


@user_bp.route('/worker/register', methods=['GET', 'POST'])
def worker_register():
    if request.method == 'POST':  # 检查是否是post提交的表单
        if request.form.get('password') == request.form.get('confirm_password'):  # 验证密码和确认密码是否一致
            exist_list = Students.query.filter_by(id=request.form.get('id')).all()
            if len(exist_list) != 0:  # 检测该账号是否已经注册过
                flash("已经注册过")
                return redirect(url_for('user.worker_register'))
            else:
                worker = Worker()  # 接受表单中的学生信息并提交到数据库中
                worker.id = request.form.get('id')
                worker.username = request.form.get('username')
                worker.password = generate_password_hash(request.form.get('password'))  # 对输入的密码进行加密在提交到数据库中
                worker.phone = request.form.get('phone')
                db.session.add(worker)
                db.session.commit()
                flash("已成功提交申请，等待管理员审核")
                return redirect(url_for('user.home_page'))

        else:
            flash("两次密码填写不一致！！！")
            return redirect(url_for('user.worker_register'))

    else:
        return render_template('user/worker_register.html')


'''管理员注册界面'''
'''功能如同学生注册界面'''


@user_bp.route('/manager/register', methods=['GET', 'POST'])
def manager_register():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):
            exist_list = Manager.query.filter_by(id=request.form.get('id')).all()
            if len(exist_list) != 0:
                flash("已经注册过")
                return redirect(url_for('user.manager_register'))
            else:
                manager = Manager()
                manager.id = request.form.get('id')
                manager.username = request.form.get('username')
                manager.password = generate_password_hash(request.form.get('password'))
                manager.phone = request.form.get('phone')
                db.session.add(manager)
                db.session.commit()
                flash("注册成功")
                return redirect(url_for('user.home_page'))

        else:
            flash("两次密码填写不一致！！！")
            return redirect(url_for('user.manager_register'))

    else:
        return render_template('user/manager_register.html')


'''学生登陆页面'''


@user_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student = Students.query.filter(Students.isdelete == False).all()  # 提取数据库中所有的学生到一个列表中
        num = 0
        for stu in student:  # 遍历列表所有的学生，检测密码是否正确，如果正确则渲染学生的首页
            if request.form.get('id') == stu.id:
                num = 1
                # n = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
                flag = check_password_hash(stu.password, request.form.get('password'))
                if flag is True:
                    flash("登陆成功，欢迎使用")
                    response = redirect(url_for('user.home_page'))
                    response.set_cookie('login_id', str(stu.id))
                    response.set_cookie('types', "student")
                    return response
                else:
                    flash("用户名或者密码错误，请重新输入")
                    return redirect(url_for('user.student_login'))

            else:
                continue
        if num == 0:
            flash("输入的id未注册，请重新输入")
            return redirect(url_for('user.student_login'))

    return render_template('user/student_login.html')


'''工作员登录'''
'''功能与学生登陆一致'''


@user_bp.route('/worker/login', methods=['GET', 'POST'], endpoint="worker_login")
def worker_login():
    if request.method == 'POST':
        worker = Worker.query.filter(Worker.isdelete == False, Worker.application == True).all()  # 提取数据库中所有的学生到一个列表中
        num = 0
        for wor in worker:  # 遍历列表所有的学生，检测密码是否正确，如果正确则渲染学生的首页
            if request.form.get('id') == wor.id:
                num = 1
                # n = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
                flag = check_password_hash(wor.password, request.form.get('password'))
                if flag is True:
                    flash("登陆成功，欢迎使用")
                    response = redirect(url_for('user.home_page'))
                    response.set_cookie('login_id', str(wor.id))
                    response.set_cookie('types', "worker")
                    return response
                else:
                    flash("用户名或者密码错误，请重新输入")
                    return redirect(url_for('user.worker_login'))

            else:
                continue
        if num == 0:
            flash("输入的id未注册，请重新输入")
            return redirect(url_for('user.worker_login'))

    return render_template('user/worker_login.html')


'''管理员登录'''
'''功能与学生登陆一致'''


@user_bp.route('/manager/login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        manager = Manager.query.filter().all()
        worker = Worker.query.filter(Worker.isdelete == False, Worker.application == False).all()
        n = len(worker)
        num = 0
        for mana in manager:
            if request.form.get('id') == mana.id:
                num = 1
                # n = hashlib.sha256(request.form.get('password').encode('utf-8')).hexdigest()
                flag = check_password_hash(mana.password, request.form.get('password'))
                if flag is True:
                    if n > 0:
                        flash("新增" + str(n) + "名工作员申请需要审核")
                        response = redirect(url_for('user.home_page'))
                        response.set_cookie('login_id', str(mana.id))
                        response.set_cookie('types', "manager")
                        return response
                    else:
                        response = redirect(url_for('user.home_page'))
                        response.set_cookie('login_id', str(mana.id))
                        response.set_cookie('types', "manager")
                        return response
                else:
                    flash("用户名或者密码错误，请重新输入")
                    return redirect(url_for('user.manager_login'))

            else:
                continue
        if num == 0:
            flash("输入的用户名未注册，请重新输入")
            return redirect(url_for('user.manager_login'))

    return render_template('user/manager_login.html')


'''登出'''


@user_bp.route('/logout')
def logout():
    response = redirect(url_for('user.home_page'))  # 重定向首页
    response.delete_cookie('login_id')  # 删除当前的cookie值“login_id”
    response.delete_cookie('types')  # 删除当前的cookie值“types”
    return response


'''筛选框功能'''


@user_bp.route('/select', methods=['GET', 'POST'], endpoint='select')
def select():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))

    student = Students.query.filter(Students.isdelete == False).all()
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 将数据库中存在的、有订单的学生信息放在student_list列表中，并在select.html中渲染出来
    student_list = Students.query.filter(Students.dormitory.contains(request.form.get('filter')),
                                         Students.isdelete == False, Students.order == True).all()
    num = str(len(student_list))
    key = request.form.get('filter')
    if types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', stu=stu, student_list=student_list, key=key)
            else:
                continue
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', wor=wor, student_list=student_list, key=key)
            else:
                continue
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', mana=mana, student_list=student_list, key=key)
            else:
                continue
    else:
        flash("请先登录")
        return redirect(url_for('user.home_page'))


'''工作员在筛选页面处理学生地需求'''


@user_bp.route('/deal/need', endpoint="deal_need", methods=['GET', 'POST'])
def deal_need():
    if request.method == 'POST':
        if request.form.get(request.form.get('id')) == 'yes':
            student = Students.query.filter(Students.id == request.form.get('id')).first()
            student.order = False
            db.session.commit()
            # 由于需要将最初工作员填写的筛选条件再次传入deal_select路由，所以通过设置response然后在cookie中保留此筛选条件。
            response = redirect(url_for('user.deal_select'))
            response.set_cookie('filter', str(request.form.get('key')))
            return response
        else:
            student = Students.query.filter(Students.id == request.form.get('id')).first()
            student.order = True
            db.session.commit()
            response = redirect(url_for('user.deal_select'))
            response.set_cookie('filter', str(request.form.get('key')))
            return response
    return redirect(url_for('user.select'))


'''
工作员送达后，在筛选页面选择已送达，然后点击已提交的按钮后显示的页面（此页面与select页面相同，但是删去了已送达的信息。
此页面相当于重定向了select页面，但由于传参机制不同，故将select页面重写。
'''


@user_bp.route('/deal/select', methods=['GET', 'POST'], endpoint='deal_select')
def deal_select():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                # 将数据库中存在的、有订单的学生信息放在student_list列表中，并在select.html中渲染出来
                student_list = Students.query.filter(Students.dormitory.contains(request.cookies.get('filter')),
                                                     Students.isdelete == False, Students.order == True).all()
                num = str(len(student_list))
                key = request.form.get('filter')
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', stu=stu, student_list=student_list, key=key)
            else:
                continue
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                student_list = Students.query.filter(Students.dormitory.contains(request.cookies.get('filter')),
                                                     Students.isdelete == False, Students.order == True).all()
                num = str(len(student_list))
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', wor=wor, student_list=student_list)
            else:
                continue
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                student_list = Students.query.filter(Students.dormitory.contains(request.cookies.get('filter')),
                                                     Students.isdelete == False, Students.order == True).all()
                num = str(len(student_list))
                flash("筛选结果如下:  共" + num + "人")
                return render_template('user/select.html', mana=mana, student_list=student_list)
            else:
                continue
    else:
        flash("请先登陆")
        return redirect(url_for('user.home_page'))


'''学生中心页面，用于渲染student_update.html页面'''


@user_bp.route('/student/center', methods=['GET', 'POST'], endpoint='student_center')
def student_center():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                return render_template('user/student_update.html', stu=stu)
            else:
                continue
    else:
        flash("请先登录学生账号")
        return redirect(url_for('user.home_page'))


'''学生中心页面，用于接收提交的用户修改后信息，并修改数据库中的相应信息'''


@user_bp.route('/student/update', methods=['GET', 'POST'], endpoint='student_update')
def student__update():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):  # 验证密码是否等于确认密码
            '''接受表单中的个人信息，并提交到数据库中'''
            student = Students.query.get(request.form.get('id'))
            student.id = request.form.get('id')
            student.username = request.form.get('username')
            # 判断密码是否改变，如果未改变则继续使用原来的密码，若发生改变则将密码加密后存入数据库
            if student.password != request.form.get('password'):
                student.password = generate_password_hash(request.form.get('password'))
            student.phone = request.form.get('phone')
            student.dormitory = request.form.get('dormitory')
            db.session.commit()
            flash("修改成功，请重新登陆")
            return redirect(url_for('user.home_page'))
    else:
        return redirect(url_for('user.home_page'))

    return redirect(url_for('home_page'))


'''功能如上面的学生中心一致'''


@user_bp.route('/worker_center', methods=['GET', 'POST'], endpoint='worker_center')
def worker_center():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    worker = Worker.query.filter(Worker.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                return render_template('user/worker_update.html', wor=wor)
            else:
                continue
    else:
        flash("请先登录工作员账号")
        return render_template('user/worker_update.html')


@user_bp.route('/worker_update', methods=['GET', 'POST'], endpoint='worker_update')
def worker__update():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):
            id = request.form.get('id')
            worker = Worker.query.get(id)
            worker.username = request.form.get('username')
            if worker.password != request.form.get('password'):
                worker.password = generate_password_hash(request.form.get('password'))
            worker.phone = request.form.get('phone')
            db.session.commit()
            flash("修改成功")
            return redirect(url_for('user.home_page'))
        else:
            flash("两次密码输入不一致")
            return redirect(url_for('user.home_page'))
    else:
        return redirect(url_for('user.home_page'))


'''管理员中心，用于渲染manage.html页面'''


@user_bp.route('/manager/center', methods=['GET', 'POST'], endpoint='manager_center')
def manager_center():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return render_template('base.html')
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                '''将学生和工作员的列表提交给manage.html页面，让其渲染出来'''
                student_list = Students.query.filter(Students.isdelete == False).all()
                worker_list = Worker.query.filter(Worker.isdelete == False).all()
                mana = Manager.query.filter_by(id=login_id).first()
                return render_template('user/manage.html', mana=mana, student_list=student_list,
                                       worker_list=worker_list)
            else:
                continue
    else:
        flash("请先登录管理员账号")
        return redirect(url_for('user.home_page'))


'''在管理员中心，通过管理员账号修改学生信息'''


@user_bp.route('/mstudent/update', endpoint="mstudent_update")
def mstudent_update():
    id = request.args.get('id')
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                info = Students.query.filter(Students.id == id).first()
                mana = Manager.query.filter_by(id=login_id).first()
                return render_template('user/mstudent_update.html', mana=mana, info=info)
            else:
                continue
    else:
        flash("请先登陆管理员账号")
        return redirect(url_for('home_page'))


'''管理员修改学生的个人信息'''


@user_bp.route('/mmstudent/update', methods=['GET', 'POST'], endpoint='mmstudent_update')
def mmstudent__update():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):
            student = Students.query.get(request.form.get('id'))
            student.id = request.form.get('id')
            student.username = request.form.get('username')
            if student.password != request.form.get('password'):
                student.password = generate_password_hash(request.form.get('password'))
            student.phone = request.form.get('phone')
            student.dormitory = request.form.get('dormitory')
            if request.form.get('order') == 'True':
                student.order = Boolean(True)
            elif request.form.get('order') == 'False':
                student.order = Boolean(False)
            else:
                student.order = None
            db.session.commit()
            flash("修改成功")
            return redirect(url_for('user.manager_center'))
    else:
        return redirect(url_for('user.manager_center'))

    return redirect(url_for('manager_center'))


'''管理员删除学生的按功能'''


@user_bp.route('/mstudent/delete', endpoint="mstudent_delete")
def mstudent_delete():
    id = request.args.get('id')
    user = Students.query.get(id)
    user.isdelete = True
    db.session.commit()
    return redirect(url_for('user.manager_center'))


'''管理员修改工作员信息的功能'''


@user_bp.route('/mworker/update', endpoint="mworker_update")
def mworker_update():
    id = request.args.get('id')
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                info = Worker.query.filter(Worker.id == id).first()
                mana = Manager.query.filter_by(id=login_id).first()
                info_password = info.password
                return render_template('user/mworker_update.html', mana=mana, info=info)
            else:
                continue
    else:
        flash("请先登陆管理员账号")
        return redirect(url_for('home_page'))


@user_bp.route('/mmworker/update', methods=['GET', 'POST'], endpoint='mmworker_update')
def mmworker__update():
    if request.method == 'POST':
        if request.form.get('password') == request.form.get('confirm_password'):
            worker = Worker.query.get(request.form.get('id'))
            worker.username = request.form.get('username')
            if worker.password != request.form.get('password'):
                worker.password = generate_password_hash(request.form.get('password'))
            worker.phone = request.form.get('phone')
            if request.form.get('application') == "True":
                worker.application = Boolean(True)
            elif request.form.get('application') == 'False':
                worker.application = Boolean(False)
            else:
                worker.application = None
            db.session.commit()
            flash("修改成功")
            return redirect(url_for('user.manager_center'))
        else:
            flash("两次密码不一致")
            return redirect(url_for('user.manager_center'))
    else:
        return redirect(url_for('user.manager_center'))

    # return redirect(url_for('manager_center'))


'''管理员删除工作员的功能'''


@user_bp.route('/mworker/delete', endpoint="mworker_delete")
def mworker_delete():
    id = request.args.get('id')
    user = Worker.query.get(id)
    user.isdelete = True
    db.session.commit()
    return redirect(url_for('user.manager_center'))


'''学生提交需求的功能，并重新渲染need页面'''


@user_bp.route('/need', endpoint="need")
def need():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter(Students.id == login_id).first()
                return render_template('user/need.html', stu=stu)
            else:
                continue
    else:
        flash("请先登陆学生账号")
        return redirect(url_for('home_page'))


'''
接受学生提交的需求的功能
并将需求添加到数据库中
'''


@user_bp.route('/accept/need', endpoint="accept_need", methods=['GET', 'POST'])
def accept_need():
    if request.method == 'POST':
        if request.form.get('id'):
            user_order = Students.query.filter_by(id=request.form.get('id')).first()
            user_order.order = True
            db.session.commit()
            order = Orders()
            db.session.add(order)
            db.session.commit()
            flash("订单提交成功")
            return redirect(url_for('user.home_page'))
    return redirect(url_for('user.home_page'))


'''工作员、管理员发布通知的功能'''


@user_bp.route('/set/notify', endpoint="set_notify", methods=['GET', 'POST'])
def set_notify():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                return render_template('user/notify.html', wor=wor)
            else:
                continue
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                return render_template('user/notify.html', mana=mana)
            else:
                continue
    else:
        flash("只有工作员和管理员可以访问该页面")
        return redirect(url_for('user.home_page'))


'''将工作员和管理员发布的通知同步到数据库中'''


@user_bp.route('/accept/notify', endpoint="accept_notify", methods=['GET', 'POST'])
def accept_notify():
    if request.method == 'POST':
        notify = Notify()
        notify.title = request.form.get('title')
        notify.content = request.form.get('content')
        db.session.add(notify)
        db.session.commit()
        flash("发布成功")
        return redirect(url_for('user.home_page'))


'''展示工作员和管理员发布的紧急通知'''


@user_bp.route('/show/notify', endpoint="show_notify", methods=['GET', 'POST'])
def show_notify():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        flash("请先登陆！")
        return redirect(url_for('user.home_page'))
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                notifies = Notify.query.filter().all()
                notify = notifies[-1]
                return render_template('user/notify_show.html', stu=stu, notify=notify)
            else:
                continue
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                notify = Notify.query.filter().first()
                return render_template('user/notify_show.html', wor=wor, notify=notify)
            else:
                continue
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                notify = Notify.query.filter().first()
                return render_template('user/notify_show.html', mana=mana, notify=notify)
            else:
                continue
    else:
        flash("请先登录")
        return redirect(url_for('user.home_page'))


'''可视化数据'''


@user_bp.route('/graph', endpoint="graph")
def graph():
    login_id = request.cookies.get('login_id', None)
    types = request.cookies.get('types', None)
    student = Students.query.filter(Students.isdelete == False).all()
    worker = Worker.query.filter(Worker.isdelete == False).all()
    manager = Manager.query.filter(Manager.isdelete == False).all()
    order_list = []  # 用来存2021年每月订单的名字：order_list(1)
    order_sum = []  # 2021年每月订单数目
    old_order_list = []  # 用来存2020年每月订单的名字：order_list(1)
    old_order_sum = []  # 2020年每月订单数目
    rate = []  # 2021年每月订单占当年的占比
    old_rate = []  # 2020年每月订单占当年的占比
    year_sum = 0  # 2021年当年订单总数
    old_sum = 0  # 2020年当年订单总数
    # 使用自定义的__result__函数求得上述变量的数据，并保存到上述变量中，__result__函数在最下方
    number = __result__(order_list, order_sum, old_order_list, old_order_sum, rate, old_rate, year_sum, old_sum)
    # 判断是否已登陆，若未登陆则自动返回首页
    if types is None:
        return redirect(url_for('user.home_page'))
    elif types == "student":
        for s in student:
            if s.id == login_id:
                stu = Students.query.filter_by(id=login_id).first()
                return render_template('user/graph.html', stu=stu, student=student, order_sum=number['order_sum'],
                                       old_order_sum=number['old_order_sum'], rate=number['rate'],
                                       old_rate=number['old_rate'])
    elif types == "worker":
        for w in worker:
            if w.id == login_id:
                wor = Worker.query.filter_by(id=login_id).first()
                return render_template('user/graph.html', wor=wor, student=student, order_sum=number['order_sum'],
                                       old_order_sum=number['old_order_sum'], rate=number['rate'],
                                       old_rate=number['old_rate'])
    elif types == "manager":
        for m in manager:
            if m.id == login_id:
                mana = Manager.query.filter_by(id=login_id).first()
                return render_template('user/graph.html', mana=mana, student=student, order_sum=number['order_sum'],
                                       old_order_sum=number['old_order_sum'], rate=number['rate'],
                                       old_rate=number['old_rate'])
    else:
        flash("请先登陆")
        return redirect(url_for('user.home_page'))


def __result__(order_list, order_sum, old_order_list, old_order_sum, rate, old_rate, year_sum, old_sum):
    for i in range(1, 13):
        order_list.append(str("order_list" + str(i)))
        order_list[i - 1] = Orders.query.filter(Orders.datetime <= datetime(2021, i, 28),
                                                Orders.datetime >= datetime(2021, i, 1)).all()
        order_sum.append(int(len(order_list[i - 1])))
        year_sum = year_sum + int(len(order_list[i - 1]))
    for i in range(1, 13):
        old_order_list.append(str("order_list" + str(i)))
        old_order_list[i - 1] = Orders.query.filter(Orders.datetime <= datetime(2020, i, 28),
                                                    Orders.datetime >= datetime(2020, i, 1)).all()
        old_order_sum.append(int(len(old_order_list[i - 1])))
        old_sum = old_sum + int(len(old_order_list[i - 1]))
    for i in range(1, 13):
        rate.append(100 * order_sum[i - 1] / year_sum)
        old_rate.append(100 * old_order_sum[i - 1] / old_sum)
    return {'order_sum': order_sum, 'old_order_sum': old_order_sum, 'rate': rate, 'old_rate': old_rate}
