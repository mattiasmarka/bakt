import numpy
from matplotlib import pyplot

def load_data(f):
    next(f)
    data = []
    for line in f:
         fields = line.strip().split(" ")
         if len(fields) == 0:
             break
         data.append([])
         for field in fields:
             try:
                num = int(field)
             except:
                try:
                    num = float(field)
                except:
                    num = field.strip()
             data[-1].append(num)
         data[-1] = data[-1][1:]
    return numpy.array(data)

with open("cpu_times.dat", "r") as f:
     cpu_data = load_data(f)

with open("gpu_times.dat", "r") as f:
     gpu_data = load_data(f)

nts = list(sorted(map(float, set(cpu_data[::, 3]))))

pyplot.plot(nts, [numpy.average(cpu_data[numpy.where(cpu_data[::, 3] == nt)]) / 60e9 for nt in nts], "k-", label="CPU")
pyplot.plot(nts, [numpy.average(gpu_data[numpy.where(gpu_data[::, 3] == nt)]) / 60e9 for nt in nts], "k--", label="GPU")

pyplot.savefig("times.jpg")