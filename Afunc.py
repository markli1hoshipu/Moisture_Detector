# data in txt is in form
# before after date 
# 287 321 2024-03-23

# data in program is in form
# {date:[[be,af],[be,af],[be,af]]}

from datetime import datetime

def get_past_data(past_data_src = 'past_data.txt'):
    try:
        with open(past_data_src, 'r') as file:
            file_content = file.read()
        re = {}
        for line in file_content.splitlines():
            cont = line.split(' ')
            if len(cont) != 3:
                continue
            date = cont[-1]
            bef = int(cont[0]); aft = int(cont[1])
            if date in re:
                re[date].append([bef,aft])
            else:
                re[date] = [[bef,aft]]
        return re
        
    except FileNotFoundError:
        return "file is not found"
    except Exception as e:
        return f"error appeared{e}"

def write_data(data, dest='past_data.txt'):
    sorted_data = dict(sorted(data.items()))
    restr = ''
    for date in sorted_data.keys():
        pairs = sorted_data[date]
        for pair in pairs:
            restr += (str(pair[0]) + ' ' + str(pair[1]) + ' ' + date + '\n')
    try:
        with open(dest, 'w') as dest_file:
            dest_file.write(restr)
        print(f"data is written to {dest}")
    except Exception as e:
        print(f"error in writing data：{e}")
    return

def graph_data_change(past_data_src = 'past_data.txt'):
    data = get_past_data(past_data_src)
    time = []; moisture_change = []
    for t, changes in data.items():
        for each in changes:
            time.append(t)
            moisture_change.append(each[1]-each[0])
    '''
    plt.plot(time, moisture_change)
    plt.xlabel('Time')
    plt.ylabel('Moisture Change')
    plt.title('Moisture Change over Time')
    plt.grid(True)
    plt.show()
    '''
    return time, moisture_change

def graph_data_before(past_data_src = 'past_data.txt'):
    data = get_past_data(past_data_src)
    time = []; moisture = []
    for t, changes in data.items():
        for each in changes:
            time.append(t)
            moisture.append(each[0])
    '''
    plt.plot(time, moisture)
    plt.xlabel('Time')
    plt.ylabel('Moisture level before watering')
    plt.title('Moisture level before watering over Time')
    plt.grid(True)
    plt.show()
    '''
    return time, moisture

def graph_data_after(past_data_src = 'past_data.txt'):
    data = get_past_data(past_data_src)
    time = []; moisture = []
    for t, changes in data.items():
        for each in changes:
            time.append(t)
            moisture.append(each[1])
    '''
    plt.plot(time, moisture)
    plt.xlabel('Time')
    plt.ylabel('Moisture level after watering')
    plt.title('Moisture level after watering over Time')
    plt.grid(True)
    plt.show()
    '''
    return time, moisture

def input(input_data, good_change = 10, max_change = 20, past_data_src = 'past_data.txt'):
    # good_change is percentage
    past_data = get_past_data(past_data_src)
    sum_after = 0; count_after = 0
    sum_change = 0; count_change =0
    for _, l in past_data.items():
        for pair in l:
            sum_after += pair[1]
            sum_change += pair[1] - pair[0]
            count_after += 1
            count_change += 1
    avg_after = sum_after / count_after
    avg_change = sum_change / count_change
    
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    re = ''; ct = 1
    re += f'The previous average moisture level after watering is {avg_after}% .\n'
    re += f'The previous average change in moisture level per watering is {avg_change}% .\n'
    re += f'The average change in moisture level per watering shall be around 10%, and must not past 20%.\n'
    re += f'{date} data:\n'
    for date, l in input_data.items():
        for pair in l:
            re += f'\nfield{ct}: mositure level {pair[0]}% -> {pair[1]}%\n'
            temp = ''
            if pair[1] < avg_after*0.9:
                temp = f'\tThe moisture level is lower than 90% of pervious average, consider re-watering.\n'
            if pair[1] > avg_after*1.1:
                temp = f'\tThe moisture level is higher than 110% of pervious average, consider reduce watering next time.\n'
            re += temp
            temp = ''
            if pair[1] - pair[0] < 8:
                temp = f'\tThe change in moisture level is lower than 8%, consider watering less frequently.\n'
            if pair[1] - pair[0] > 12:
                temp = f'\t\tThe change in moisture level is higher than 12%, consider watering more frequently.\n'
            if pair[1] - pair[0] > 20:
                temp = f'\tThe change in moisture level is higher than 20%, strongly suggest watering more frequently.\n'
            re += temp
            ct += 1

    for date,l in input_data.items():
        if date not in past_data:
            past_data[date] = [] 
        past_data[date] += l

    write_data(past_data)
    return re
