import gzip
import io
import os
import re

config = {
    "LOG_DIR": "./logi" 
    }

def main():
    log_names = sorted(os.listdir(config.get('LOG_DIR')))
    if not log_names: return print(f'Logs not found')
    log_name = log_names[-1]
    log_path = f'{config.get("LOG_DIR")}/{log_name}'
    pattern = re.compile(r'\"[A-Z]+ (\S+) .* (\d+\.\d+)\n')
    data = {}
    all_count = 0

    def read_log(iterable_entity):
        nonlocal all_count
        for line in iterable_entity:
            result = pattern.findall(line)
            all_count += 1
            if not len(result): continue
            url, time = result[0]
            if url not in data: data[url] = []
            data[url].append(float(time))

    if os.path.splitext(log_path)[1] == '.gz':
        with gzip.open(log_path, 'r') as archive:
            with io.TextIOWrapper(archive, encoding='utf-8') as decoder:
                read_log(decoder)
    else:
        with open(log_path, 'r') as file:
            read_log(file)


    for key in data:
        count = len(data[key])
        print(f'URL: {key}'
              f'\tcount: {count}'
              f'\n\tpercуте: {count/all_count * 100}'
              f'\n\tmean: {sum(data[key])/count}'
              f'\n\tmax: {max(data[key])}')
        sorted(data[key])
        if count%2!=0:
            print(f'\n\tmedian: {float(data[key][count//2])}')
        else:
            print(f'\n\tmedian: {float((data[key][int((count-1)/2)]+data[key][int(count/2)])/2.0)}')
        
        
                


if __name__ == "__main__":
    main()