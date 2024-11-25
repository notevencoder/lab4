import json
import numpy as np
import requests
import datetime
import matplotlib.pyplot as plt
from collections import Counter


def convert_time(time_str):
    time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time


def get_issue_created_time(issue):
    time_str = issue['fields']['created']
    time = convert_time(time_str)
    return time


def get_issue_resolution_time(issue):
    time_str = issue['fields']['resolutiondate']
    time = convert_time(time_str)
    return time


def get_issue_item_to_time(issue, field, to):
    time_list = []
    for history in issue['changelog']['histories']:
        for item in history['items']:
            if item['field'] == field and (item['toString'] == to or item['to'] == to):
                time_list.append(convert_time(history['created']))
    return time_list


def timedelta_to_sec(time):
    return time.total_seconds()


def timedelta_to_min(time):
    return time.total_seconds() / 60


def timedelta_to_hours(time):
    return time.total_seconds() / 3600


def timedelta_to_days(time):
    return time.total_seconds() / (3600 * 24)


def summ_elements(list):
    list_summ = []
    s = 0
    for elem in list:
        s = s + elem
        list_summ.append(s)
    return list_summ


def make_lists_name_num(list_users, count):
    counted_values = Counter(list_users)
    arr = counted_values.most_common(count)
    list_names = []
    list_nums = []
    for elem in arr:
        list_names.append(elem[0])
        list_nums.append(elem[1])
    return list_names, list_nums


def get_resolved_time_for_assignee(issue, username):
    l_start = get_issue_item_to_time(issue, 'assignee', username)
    if l_start == []:
        time_start = get_issue_created_time(issue)
    else:
        time_start = l_start[-1]

    l_stop = get_issue_item_to_time(issue, 'status', 'Resolved')
    if l_stop == []:
        time_stop = get_issue_resolution_time(issue)
    else:
        time_stop = l_stop[-1]

    return timedelta_to_hours(time_stop - time_start)


def status_statistic(issue):
    sum_time_open = datetime.timedelta(0)
    sum_time_in_progress = datetime.timedelta(0)
    sum_time_resolved = datetime.timedelta(0)
    sum_time_reopened = datetime.timedelta(0)
    sum_time_patch_available = datetime.timedelta(0)

    time_start = get_issue_created_time(issue)
    for history in issue['changelog']['histories']:
        for item in history['items']:
            if item['field'] == 'status':
                time_stop = convert_time(history['created'])
                time = time_stop - time_start
                status = item['fromString']
                if status == 'Open':
                    sum_time_open = sum_time_open + time
                elif status == 'In Progress':
                    sum_time_in_progress = sum_time_in_progress + time
                elif status == 'Resolved':
                    sum_time_resolved = sum_time_resolved + time
                elif status == 'Reopened':
                    sum_time_reopened = sum_time_reopened + time
                elif status == 'Patch Available':
                    sum_time_patch_available = sum_time_patch_available + time
                time_start = time_stop

    return sum_time_open, sum_time_in_progress, sum_time_resolved, sum_time_reopened, sum_time_patch_available


def graph1():
    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'created,resolutiondate'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    list_data = []
    for elem in data['issues']:
        created_t = get_issue_created_time(elem)
        closed_t_list = get_issue_item_to_time(elem, 'status', 'Closed')
        if closed_t_list == []:
            closed_t = get_issue_resolution_time(elem)
        else:
            closed_t = closed_t_list[-1]
        time = closed_t - created_t
        list_data.append(timedelta_to_days(time))

    count = len(data['issues'])
    max_el = max(list_data)
    plt.hist(list_data, color='blue', edgecolor='black', bins=25)
    plt.title('1. Гистограмма времени решения к количеству задач')
    plt.xlabel('Время решения (дни)')
    plt.xticks(np.arange(0, int(max_el), int(max_el / 20)))
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_data.sort()
    middle_index = int(count / 1.4)
    first_patr = list_data[:middle_index]
    max_el = max(first_patr)
    plt.hist(first_patr, color='purple', edgecolor='black', bins=25)
    plt.title('1. Гистограмма времени решения к количеству задач')
    plt.xlabel('Время решения (дни)')
    plt.xticks(np.arange(0, int(max_el), int(max_el / 20)))
    plt.ylabel('Количество задач')
    plt.tight_layout()
    return plt


def graph2():
    list_open = []
    list_in_progress = []
    list_resolved = []
    list_resolved_day = []
    list_reopened = []
    list_patch_available = []
    list_patch_available_day = []

    payload = {'jql': 'project=KAFKA AND status=Closed ORDER BY createdDate', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    for elem in data['issues']:
        t_open, t_in_prog, t_res, t_reo, t_patch = status_statistic(elem)

        if t_open != datetime.timedelta(0):
            list_open.append(timedelta_to_days(t_open))
        if t_in_prog != datetime.timedelta(0):
            list_in_progress.append(timedelta_to_days(t_in_prog))
        if t_res != datetime.timedelta(0):
            list_resolved.append(timedelta_to_sec(t_res))
            list_resolved_day.append(timedelta_to_days(t_res))
        if t_reo != datetime.timedelta(0):
            list_reopened.append(timedelta_to_days(t_reo))
        if t_patch != datetime.timedelta(0):
            list_patch_available_day.append(timedelta_to_days(t_patch))
            list_patch_available.append(timedelta_to_hours(t_patch))

    # print(list_open)
    # print(list_resolved)
    # print(list_reopened)
    # print(list_in_progress)
    # print(list_patch_available)

    ###### Open
    plt.hist(list_open, color='blue', edgecolor='black', bins=30)
    plt.title('2. Диаграмма Open 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_open.sort()
    middle_index = int(len(list_open) / 1.2)
    first_patr = list_open[:middle_index]
    plt.hist(first_patr, color='blue', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Open 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Resolved
    plt.hist(list_resolved_day, color='green', edgecolor='black', bins=30)
    plt.title('2. Диаграмма Resolved 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_resolved.sort()
    middle_index = int(len(list_resolved) / 1.6)
    first_patr = list_resolved[:middle_index]
    plt.hist(first_patr, color='green', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Resolved 2')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    middle_index = int(len(list_resolved) / 1.8)
    second_patr = list_resolved[:middle_index]
    plt.hist(second_patr, color='green', edgecolor='black', bins=80)
    plt.title('2. Диаграмма Resolved 3')
    plt.xlabel('Время решения (секунды)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Reopened
    plt.hist(list_reopened, color='yellow', edgecolor='black', bins=175)
    plt.title('2. Диаграмма Reopened')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    #### In Progress
    plt.hist(list_in_progress, color='purple', edgecolor='black', bins=50)
    plt.title('2. Диаграмма In Progress 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_in_progress.sort()
    second_patr = list_in_progress[:len(list_in_progress) - 4]
    plt.hist(second_patr, color='purple', edgecolor='black', bins=80)
    plt.title('2. Диаграмма In Progress 2')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    ###### Patch Available
    plt.hist(list_patch_available_day, color='orange', edgecolor='black', bins=30)
    plt.title('2. Диаграмма Patch Available 1')
    plt.xlabel('Время решения (дни)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()

    list_patch_available.sort()
    middle_index = int(len(list_patch_available) / 1.3)
    second_patr = list_patch_available[:middle_index]
    plt.hist(second_patr, color='orange', edgecolor='black', bins=40)
    plt.title('2. Диаграмма Patch Available 2')
    plt.xlabel('Время решения (часы)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()


def graph3():
    # за последние 90 дней
    NUM_DAYS = 90

    list_open_by_day = []
    list_dates = []
    current_date = datetime.date.today()

    for i_day in range(0, -NUM_DAYS, -1):
        jql_str = f'project=KAFKA AND created>startOfDay("{i_day}d") AND created<startOfDay("{i_day + 1}d")'
        payload = {'jql': jql_str, 'maxResults': '1000',
                   'fields': 'created'}
        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        list_open_by_day.append(data['total'])
        date = current_date + datetime.timedelta(days=i_day)
        list_dates.append(date)

    list_open_by_day.reverse()
    list_dates.reverse()

    plt.plot(list_open_by_day, linewidth=3.0, color='red')

    close_list_dates = []
    payload = {'jql': f'project=KAFKA AND status=Closed', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    for elem in data['issues']:
        l_time = get_issue_item_to_time(elem, 'status', 'Closed')
        if l_time != []:
            close_list_dates.append(l_time[-1].date())

    close_list_dates.sort()
    close_list_dates.reverse()
    counter = Counter(close_list_dates)

    list_close_by_day = []

    for i in range(NUM_DAYS):
        date = current_date - datetime.timedelta(days=i)
        k = counter[date]
        list_close_by_day.append(k)

    list_close_by_day.reverse()

    plt.plot(list_close_by_day, linewidth=3.0, color='green')
    plt.title(f'3. Графики открытых и закрытых задач за последние {NUM_DAYS} дней')
    plt.xlabel('Дата')
    plt.ylabel('Количество задач')

    x_list = []
    for i in range(NUM_DAYS):
        x_list.append(i)

    plt.xticks(x_list, labels=list_dates, rotation=90, size=8)
    plt.show()

    summary_list_open = summ_elements(list_open_by_day)
    summary_list_close = summ_elements(list_close_by_day)

    plt.plot(summary_list_open, linewidth=3.0, color='red')
    plt.plot(summary_list_close, linewidth=3.0, color='green')
    plt.title(f'3. Графики накопления открытых и закрытых задач за последние {NUM_DAYS} дней')
    plt.xlabel('Дата')
    plt.ylabel('Количество задач')
    plt.xticks(x_list, labels=list_dates, rotation=90, size=8)
    plt.show()


def graph4():
    payload = {'jql': 'project=KAFKA AND NOT assignee=null AND NOT reporter=null', 'maxResults': '1',
               'fields': 'reporter,assignee'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    total = int(data['total'])

    list_users = []

    for start_at in range(0, total, 1000):
        payload = {'jql': 'project=KAFKA AND NOT assignee=null AND NOT reporter=null', 'maxResults': '1000',
                   'startAt': f'{start_at}',
                   'fields': 'reporter,assignee'}

        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        for elem in data['issues']:
            reporter = elem['fields']['reporter']['key']
            assignee = elem['fields']['assignee']['key']
            if reporter == assignee:
                list_users.append(reporter)

    list_users_30, list_numbers_30 = make_lists_name_num(list_users, 30)

    plt.plot(list_numbers_30, list_users_30, linewidth=3.0, color='green')
    plt.title(f'График пользователи и задачи')
    plt.ylabel('Пользователь')
    plt.xlabel('Количество задач')
    plt.show()

    plt.plot(list_numbers_30, linewidth=3.0, color='green')
    plt.title(f'График пользователи и задачи')
    plt.xlabel('Пользователь')
    plt.ylabel('Количество задач')
    x_list = []
    for i in range(30):
        x_list.append(i)
    plt.xticks(x_list, labels=list_users_30, rotation=45, size=8)
    plt.show()


def graph5(username):
    #username = 'nehanarkhede'
    list_5 = []
    payload = {'jql': 'project=KAFKA AND status=Closed AND NOT assignee=null', 'maxResults': '1000',
               'fields': 'assignee'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)
    for elem in data['issues']:
        assignee = elem['fields']['assignee']['key']
        list_5.append(assignee)

    counted_values = Counter(list_5)
    print(counted_values)

    ##################

    payload = {'jql': f'project=KAFKA AND status=Closed AND assignee={username}', 'maxResults': '1000',
               'expand': 'changelog',
               'fields': 'resolutiondate,created'}

    response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
    data = json.loads(response.text)

    times_list = []

    for elem in data['issues']:
        times_list.append(get_resolved_time_for_assignee(elem, username))

    plt.hist(times_list, bins=100, edgecolor='black', color='blue')

    plt.title(f'Гистограмма: пользователь {username}')
    plt.xlabel('Время решения (часы)')
    plt.ylabel('Количество задач')
    plt.tight_layout()
    plt.show()


def graph6():
    list_x = ['Trivial', 'Minor', 'Major', 'Critical', 'Blocker']
    list_y = []
    for prio in list_x:
        payload = {'jql': f'project=KAFKA AND priority = {prio}', 'maxResults': '1', 'fields': 'priority'}
        response = requests.get('https://issues.apache.org/jira/rest/api/2/search', params=payload)
        data = json.loads(response.text)
        list_y.append(int(data['total']))


    plt.plot(list_y, linewidth=3.0, color='green')
    plt.title(f'График количество задач по степени серьезности')
    plt.xlabel('Приоритет')
    plt.ylabel('Количество задач')
    x_list = [0, 1, 2, 3, 4]
    plt.grid(True)
    plt.yticks(list_y)
    plt.xticks(x_list, labels=list_x)
    plt.show()

