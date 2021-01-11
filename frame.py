from CU import *

windows = tk.Tk()
windows.title('Calc')

config = tk.IntVar()
registerConfig = tk.IntVar()

radioButtonFrame = tk.Frame(windows)
for m, num in modules:
    tk.Radiobutton(radioButtonFrame, text=m, value=num, variable=config).pack(side='left')
radioButtonFrame.pack()

input1Frame = tk.Frame(windows)
tk.Label(input1Frame, text='输入').pack(side='left')
input1 = tk.Entry(input1Frame, width=50)
input1.pack(side='left', fill='both')
tk.Label(input1Frame, text='真值位数').pack(side='left')
bit_length_input = tk.Entry(input1Frame, width=5)
bit_length_input.pack(side='left')
input1Frame.pack()

registerFrame = tk.Frame(windows)
for m, num in register_modules:
    tk.Radiobutton(registerFrame, text=m, value=num, variable=registerConfig).pack(side='left')
registerFrame.pack()


pretext = []
for i in register_modules:
    pretext.append(i[0]+': ')
Register_Var = [tk.StringVar() for _ in register_modules]
Register_Label = [tk.Label(windows, textvariable=Register_Var[i]) for i in range(len(register_modules))]
for i in Register_Label:
    i.pack()
for i in range(len(pretext)):
    Register_Var[i].set(pretext[i])


def process():
    calc(textArea, config.get(), registerConfig.get(), input1.get(), int(bit_length_input.get()))


def process2():
    r = next_step()
    if r is not None:
        for i in range(len(r)):
            Register_Var[i].set(pretext[i] + r[i])

        textArea.insert(tk.END, '\n')


buttonFrame = tk.Frame(windows)
tk.Button(buttonFrame, text='输入', command=process).pack(side='left')
tk.Button(buttonFrame, text='运行一步', command=process2).pack(side='right')
buttonFrame.pack()
textArea = tk.Text(windows, width=40, height=40)
textArea.pack()
