# Мой Виртуальный банк финальная работа
import os
import requests

# папка для пользовательских данных
users_data = os.path.join(os.getcwd(), 'users_data')

# постфикс для пользовательских файлов с данными 
data_file_postfix = '-regdata'

# информация о банке
def about_bank():
	info_dict = {'greeteng':'Здравствуйте, Вас приветствует банк VIRTUAL MONEY',
	'capitalization':'Капитализация банка 10000000$',
	'bank_name':'Банк Ковалева Дениса',
	'version':'Версия банка: 0.2',
	'autor':'Автор программы: Ковалев Д.В.'}
	print(info_dict['greeteng'])
	print(info_dict['capitalization'])
	print(info_dict['bank_name'])
	print(info_dict['version'])
	print(info_dict['autor'])

# регистрация клиента
def registration():
	user_mail = input('Введите электронную почту (будущий логин) ')
	user_work_folder = os.path.join(users_data, user_mail)
	if os.path.exists(str(user_work_folder)):
		print('Данный email уже используется! \n')
		registration()
	else:
		user_name = input('Введите ФИО > ')
		user_passwd = input('Введите пароль > ')
		os.mkdir(user_work_folder)
		user_data_file = user_mail + data_file_postfix
		file = open((os.path.join(user_work_folder, user_data_file)), 'w')
		file.write(user_mail + '\n' + user_name + '\n' + user_passwd)
		file.close()

# логин пользователя в системе
def user_login():
	user_mail = input('Логин (email) > ')
	user_work_folder = os.path.join(users_data, user_mail)
	if os.path.exists(user_work_folder):
		user_passwd = input('Введите пароль > ')
		user_data_file = os.path.join(user_work_folder, user_mail+data_file_postfix)
		saved_passwd = read_user_data_file(user_data_file)[2]
		if user_passwd == saved_passwd:
			print('Вы вошли в систему...')
			global returned_user_info
			returned_user_info = read_user_data_file(user_data_file)
		else:
			print('Пароль не верен!')
			user_login()
	else:
		print('Нет такого пользователя или ошибка в логине...')
		user_login()
	return returned_user_info

# чтение файла с данными пользователя
def read_user_data_file(user_data_file):
	file = open(user_data_file)
	lines = file.readlines()
	user_data = []
	for elem in lines:
		user_data.append(elem.replace('\n',''))
	return user_data

# функция входа в банк
def enter_bank():
	print()
	print('Если Вы зарегистрированы в системе выполните вход, иначе пройдите регистрацию')
	print('1 - Войти, 2 - Регистрация ')
	reg_or_login = digit_choise(2)
	if reg_or_login == 1:
		print('Вход в систему ...')
		global loggedin_user
		loggedin_user = user_login()
	elif reg_or_login == 2:
		print('Процедура регистрации ...')
		registration()
		enter_bank()
	return loggedin_user

# личный кабинет пользователя
def personal_area(user):
	print('Добро пожаловать в личный кабинет,', user[1])
	print('Выберете операцию ...')
	print('1. Потребительский кредит')
	print('2. Бизнес кредит')
	print('3. Кредитная история')
	print('4. Криптовалюты')
	print('5. Все пользователи системы')
	print('6. Выход')
	operation = digit_choise(6)
	if operation == 1:
		credit_params = {'credit_name':'Потребительский кредит', 'percent':11.75, 'min_summ':10000, 'max_summ':300000, 'max_years':5}
		print_credit_params(credit_params)
		user_loan_answer = loan_request(credit_params)
		print('Ежемесячный платеж по кредиту %s руб. сроком на %s составит %s' % (user_loan_answer[0], user_loan_answer[1], user_loan_answer[2]))
		print('Оформить кредит? (1 - да, 2 - нет) --> ')
		get_loan = digit_choise(2)
		if get_loan == 1:
			print('Оформляем')
			credit_processing(user_loan_answer, user, credit_params)
		elif get_loan == 2:
			print('Выход в Личный Кабинет \n')
			personal_area(user)

	elif operation == 2:
		credit_params = {'credit_name':'Бизнес кредит', 'percent':18.25, 'min_summ':1000000, 'max_summ':10000000, 'max_years':25}
		print_credit_params(credit_params)
		user_loan_answer = loan_request(credit_params)
		print('Ежемесячный платеж по кредиту %s руб. сроком на %s составит %s' % (user_loan_answer[0], user_loan_answer[1], user_loan_answer[2]))
		print('Оформить кредит? (1 - да, 2 - нет) --> ')
		get_loan = digit_choise(2)
		if get_loan == 1:
			print('Оформляем')
			credit_processing(user_loan_answer, user, credit_params)
		elif get_loan == 2:
			print('Выход в Личный Кабинет \n')
			personal_area(user)

	elif operation == 3:
		print('3. Кредитная история')
		show_credit_history(user)
		personal_area(user)
	elif operation == 4:
		print('4. Криптовалюты')
		show_crypto()
		personal_area(user)
	elif operation == 5:
		print('5. Пользователи системы')
		list_users()
		personal_area(user)
	elif operation == 6:
		print('6. Выход')
		print('Досвидания!')
		#sys.exit(0)

# оформление кредита
def credit_processing(user_loan_answer, user, credit_params):
	if credit_params['credit_name'] == 'Потребительский кредит':
		income = float(input('Введите Ваш ежемесячный заработок (руб.) --> '))
		exp = int(input('Введите Ваш стаж на последнем месте работы (год.) --> '))
		# аудит пользователя и получение ответа одобрен или нет кредит передаются пороговые значения для отказа
		audit_result = user_audit(income, exp, 50000, 3)
		if audit_result == 0:
			print('Вам одобрен кредит\n')
			create_credit_history(user_loan_answer, user, credit_params)
			personal_area(user)
		else:
			print('Вам ОТКАЗАНО!\n')
			personal_area(user)
	elif credit_params['credit_name'] == 'Бизнес кредит':
		income = float(input('Введите ежемесячный доход вашего бизнеса (руб.) --> '))
		exp = int(input('Введите срок вашего бизнеса (год.) --> '))
		# аудит пользователя и получение ответа одобрен или нет кредит передаются пороговые значения для отказа
		audit_result = user_audit(income, exp, 1000000, 5)
		if audit_result == 0:
			print('Вам одобрен кредит\n')
			create_credit_history(user_loan_answer, user, credit_params)
			personal_area(user)
		else:
			print('Вам ОТКАЗАНО!\n')
			personal_area(user)


# аудит пользовательских параметров для одобрения кредита
def user_audit(income, exp, min_income, min_exp):
	if income >= min_income:
		if exp >= min_exp:
			result = 0 # одобрен
		else:
			result = 1 # отклонен по сроку
	else:
		result = 2 # отклонен по доходу
	return result


# создание файла кредитной истории 
def create_credit_history(user_loan_answer, user, credit_params):
	user_work_folder = os.path.join(users_data, user[0])
	file = open((os.path.join(user_work_folder, 'credit_history.txt')), 'a')
	#file.write(str(credit_params)+str(user_loan_answer))
	str_to_file = 'вид кредита:%s, ставка:%s, сумма:%s, срок:%s, ежемесячный платеж:%s' % (credit_params['credit_name'], credit_params['percent'], user_loan_answer[0], user_loan_answer[1], user_loan_answer[2])
	file.write(str_to_file + '\n')
	file.close()

# выводит кредитную историю по пользователю
def show_credit_history(user):
	credit_history_file = os.path.join(users_data, user[0], 'credit_history.txt')
	if os.path.isfile(credit_history_file):
		file = open(credit_history_file)
		lines = file.readlines()
		print('Ваша кредитная история:\n')
		for elem in lines:
			print(elem)
		file.close()
		print()
	else:
		print('В системе нет кредитов\n')

# список всех пользователей в ситеме с логинами и ФИО
def list_users():
	users = os.listdir(users_data)
	for elem in users:
		print(elem, ':', read_user_data_file(os.path.join(users_data,str(elem),str(elem)+data_file_postfix))[1])
	print()

# выводит список всех криптовалют с которыми работает bittrex.com
def show_crypto():
	get_crypto = requests.get('https://api.bittrex.com/api/v1.1/public/getcurrencies')
	crypto_result_json = get_crypto.json()
	for counter in range(len(crypto_result_json['result'])):
		for key, value in crypto_result_json['result'][counter].items():
			print(key, value)
		print('-'*50)


# печать параметров кредита
def print_credit_params(credit_params):
	print(credit_params['credit_name'])
	print('Процентная ставка по кредиту %s ' % (credit_params['percent']))
	print('Cумма кредита от %s до %s руб.' % (credit_params['min_summ'], credit_params['max_summ']))
	print('Максимальный срок кредита %s лет' % (credit_params['max_years']))

# функция пользовательского выбора принимает количество вариантов ответов
def digit_choise(variants):
	global choise
	choise = input('--> ')
	if choise.isdigit() and int(choise) in range(1,variants+1):
		choise = int(choise)
	else:
		print('не верные парметры выбора, попробуйте еще раз')
		digit_choise(variants)
	return choise

# расчет аннуитентного ежемесячного платежа
def annuity_payment(cred_sum, percent, years):
	month_percent = percent / 100 / 12
	pay = cred_sum *(month_percent+(month_percent/((1 + month_percent) ** (years * 12) - 1))) 
	return int(round(pay,0))

# проверка введенного цифрового значения на валидность и принадлежность к диаппазону
def check_values_for_credit(input_val, min_val, max_val):
	if input_val.isdigit() and int(input_val) >= min_val and int(input_val) <= max_val:
		return True
	else:
		return False

# запрос параметров для расчета ежемесячного платежа по кредиту у пользователя вовзращает размер платежа
def loan_request(credit_params):
	global user_annuity_amount, user_cred_sum, user_cred_years
	user_cred_sum = input('Введите желаемую сумму кредита (от %s до %s)--> ' % (credit_params['min_summ'], credit_params['max_summ']))
	if check_values_for_credit(user_cred_sum, credit_params['min_summ'], credit_params['max_summ']):
		user_cred_sum = int(user_cred_sum)
		user_cred_years = input('Введите срок кредита (от %s до %s)--> ' % (1,credit_params['max_years']))
		if check_values_for_credit(user_cred_years, 1, credit_params['max_years']):
			user_cred_years = int(user_cred_years)
			user_annuity_amount = annuity_payment(user_cred_sum, credit_params['percent'], user_cred_years)
		else:
			print('Ошибка: Срок кредита недопустимое значение!')
			loan_request(credit_params)
	else:
		print('Ошибка: Сумма кредита недопустимое значение!')
		loan_request(credit_params)
	return user_cred_sum, user_cred_years, user_annuity_amount


# вызов инфо о банке
about_bank()

# вход или регистрация в банке возвращает данные залогиненного пользователя
loggedin_user = enter_bank()
personal_area(loggedin_user)