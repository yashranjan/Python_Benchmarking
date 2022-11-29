import subprocess
import re
import time

loop, repeat, unit = 1, 1, 'sec'

class Point:
    def __init__(self, py='3.6', loop=0, repeat=0, time=0.0) -> None:
        self.py = py
        self.loop = loop
        self.repeat = repeat
        self.time = time

class DataPoint:
    def __init__(self, code='') -> None:
        self.code = code
        self.py_data = []
    
    def addPoint(self, py, loop, repeat, time):
        self.py_data.append(Point(py, loop, repeat, time))
    
    def __repr__(self) -> str:
        return 'For TestCode: {}\n {}\n'.format(self.code, '\n'.join(['{idx}. {i.py}=> Loops:{i.loop}, Rep:{i.repeat}, Time per loop:{i.time} {unit}'.format(idx=idx, i=i, unit=unit) for idx, i in enumerate(self.py_data)]))

def main():
    pat = r'[a-zA-Z0-9, ]+: [0-9]*.[0-9]*'
    timeit_tmp = 'python3.{ver} -m timeit -n {loop} -r {repeat} --unit={unit}'

    code1 = '''{} "import xml.etree.ElementTree as ET;tree = ET.parse('books.xml');"'''.format(timeit_tmp)
    code2 = '''{} "import xml.etree.ElementTree as ET;tree = ET.parse('mega.xml');"'''.format(timeit_tmp)

    data_dict = {
        'test_1':DataPoint(code1),
        'test_2':DataPoint(code2)
    }

    for test, test_data in data_dict.items():
        code = test_data.code
        for ver in ['6', '8', '9', '10', '11']:
            py_ver = 'Py3.{}'.format(ver)
            ver_code = code.format(ver=ver, loop=loop, repeat=repeat, unit=unit)
            
            res = subprocess.check_output(ver_code, shell=True)
            res = res.decode('utf-8')

            pat_res = re.findall(pat, res)
            if pat_res:
                time = pat_res[0].split(': ')[1]
                point_obj = Point(py_ver, loop, repeat, time)
                test_data.py_data.append(point_obj)

    for key, item in data_dict.items():
        print(item)


if __name__ == '__main__':
    st = time.time()
    main()
    print('Total Time Elapsed in main: {}s'.format(time.time() - st))