from CU import *

windows = tk.Tk()
windows.title('Calc')

config = tk.IntVar()

radioButtonFrame = tk.Frame(windows)
for m, num in modules:
    tk.Radiobutton(radioButtonFrame, text=m, value=num, variable=config).pack(side='left')
radioButtonFrame.pack()

input1Frame = tk.Frame(windows)
tk.Label(input1Frame, text='input1').pack(side='left')
input1 = tk.Entry(input1Frame, width=50)
input1.pack(fill='both')
input1Frame.pack()

input2Frame = tk.Frame(windows)
tk.Label(input2Frame, text='input2').pack(side='left')
input2 = tk.Entry(input2Frame, width=50)
input2.pack(fill='both')
input2Frame.pack()

R1Var = tk.StringVar()
R2Var = tk.StringVar()
R1 = tk.Label(windows, textvariable=R1Var)
R2 = tk.Label(windows, textvariable=R2Var)
R1.pack()
R2.pack()
R1Var.set('R1:')
R2Var.set('R2:')


def process():
    try:
        num1 = int(input1.get())
        num2 = int(input2.get())
        if (num1 > 0 and num1 >= bit10) or (num2 > 0 and num2 >= bit10):
            raise Exception('exists one input is too large')
        if (num1 < 0 and num1 < -bit10) or (num2 < 0 and num2 < -bit10):
            raise Exception('exists one input is too small')
    except Exception as e:
        print(e)
        pass
    else:
        calc(textArea, config.get(), input1.get(), input2.get())
        # if r is not None:
        #     R1Var.set('R1:' + r[0])
        #     R2Var.set('R2:' + r[1])
        #     # print(r[0], r[1])


def process2():
    r = next_step()
    if r is not None:
        R1Var.set('R1:' + r[0])
        R2Var.set('R2:' + r[1])
        textArea.insert(tk.END, '\n')
    # print(r[0], r[1])


buttonFrame = tk.Frame(windows)
tk.Button(buttonFrame, text='send', command=process).pack(side='left')
tk.Button(buttonFrame, text='next step', command=process2).pack(side='right')
buttonFrame.pack()
textArea = tk.Text(windows, width=40, height=40)
textArea.pack()
