import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0,np.pi, 0.1)

cos = np.cos(x)
cos2 = np.power(np.cos(x),2)
sin = np.sin(x)
sin2 = np.power(np.sin(x),2)

handles=[]
line, = plt.plot(x/np.pi, cos, label='cos')
handles.append(line)
line, = plt.plot(x/np.pi, cos2, label='cos2')
handles.append(line)
line, = plt.plot(x/np.pi, sin, label='sin')
handles.append(line)
line, = plt.plot(x/np.pi, sin2, label='sin2')
handles.append(line)

plt.xlabel('x [pi]')
plt.ylabel('y=f(x)')

plt.legend(handles=handles)
plt.show()
