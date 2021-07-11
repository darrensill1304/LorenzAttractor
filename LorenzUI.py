from tkinter import *
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from LorenzModel import run_lorenz


class LorenzUI:
    input_width = 10

    def __init__(self):
        self.root = Tk()
        self.root.title("Lorenz Attractor")
        self.root.geometry("1290x960")

        self.chart_fr = Frame(self.root)

        self.figure = plt.Figure()
        self.figure.tight_layout()
        self.ax = self.figure.add_subplot(projection="3d")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_fr)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.input_fr = Frame(self.root, relief=RAISED, bd=2)

        self.init_x_lbl = Label(self.input_fr, text="Initial X")
        self.init_x_input = Entry(self.input_fr, width=self.input_width)
        self.init_y_lbl = Label(self.input_fr, text="Initial Y")
        self.init_y_input = Entry(self.input_fr, width=self.input_width)
        self.init_z_lbl = Label(self.input_fr, text="Initial Z")
        self.init_z_input = Entry(self.input_fr, width=self.input_width)

        self.rho_lbl = Label(self.input_fr, text="Rho")
        self.rho_input = Entry(self.input_fr, width=self.input_width)
        self.sigma_lbl = Label(self.input_fr, text="Sigma")
        self.sigma_input = Entry(self.input_fr, width=self.input_width)
        self.beta_lbl = Label(self.input_fr, text="Beta")
        self.beta_input = Entry(self.input_fr, width=self.input_width)
        self.time_lbl = Label(self.input_fr, text="Sim Time")
        self.time_input = Entry(self.input_fr, width=self.input_width)

        self.is_animated = IntVar(value=1)
        self.is_animation_playing = False
        self.animate_chk = Checkbutton(self.input_fr, text="Animate?", variable=self.is_animated)
        self.run_btn = Button(self.input_fr, text="Run", command=self.generate_model)
        self.stop_btn = Button(self.input_fr, text="Pause", command=self.toggle_pause)
        self.reset_btn = Button(self.input_fr, text="Reset Defaults", command=self.set_defaults)

        self.root.rowconfigure(0, minsize=50, weight=1)
        self.root.columnconfigure(0, minsize=800, weight=1)

        self.init_x_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.init_x_input.grid(row=0, column=1, padx=5, pady=5)
        self.init_y_lbl.grid(row=1, column=0, padx=5, pady=5)
        self.init_y_input.grid(row=1, column=1, padx=5, pady=5)
        self.init_z_lbl.grid(row=2, column=0, padx=5, pady=5)
        self.init_z_input.grid(row=2, column=1, padx=5, pady=5)

        self.rho_lbl.grid(row=4, column=0, padx=5, pady=5)
        self.rho_input.grid(row=4, column=1, padx=5, pady=5)
        self.sigma_lbl.grid(row=5, column=0, padx=5, pady=5)
        self.sigma_input.grid(row=5, column=1, padx=5, pady=5)
        self.beta_lbl.grid(row=6, column=0, padx=5, pady=5)
        self.beta_input.grid(row=6, column=1, padx=5, pady=5)
        self.time_lbl.grid(row=7, column=0, padx=5, pady=5)
        self.time_input.grid(row=7, column=1, padx=5, pady=5)

        self.animate_chk.grid(row=8, column=0, padx=5, pady=5)
        self.run_btn.grid(row=9, column=0, padx=5, pady=5)
        self.stop_btn.grid(row=9, column=1, padx=5, pady=5)
        self.reset_btn.grid(row=10, column=0, padx=5, pady=5)

        self.chart_fr.grid(row=0, column=0, sticky="nse")
        self.input_fr.grid(row=0, column=1, sticky="nsew")

        self.set_defaults()

    @staticmethod
    def __set_default(field, value):
        field.delete(0, END)
        field.insert(0, value)

    def set_defaults(self):
        self.__set_default(self.init_x_input, 1.0)
        self.__set_default(self.init_y_input, 1.0)
        self.__set_default(self.init_z_input, 1.0)
        self.__set_default(self.rho_input, 28.0)
        self.__set_default(self.sigma_input, 10.0)
        self.__set_default(self.beta_input, 2.666667)
        self.__set_default(self.time_input, 40.0)
        self.animate_chk.select()

    def generate_model(self):
        x = float(self.init_x_input.get())
        y = float(self.init_y_input.get())
        z = float(self.init_z_input.get())
        rho = float(self.rho_input.get())
        sigma = float(self.sigma_input.get())
        beta = float(self.beta_input.get())
        t = float(self.time_input.get())
        dt = 0.01  # TODO Needed as Input?

        self.model = run_lorenz([x, y, z], t, dt, rho, sigma, beta)

        if self.is_animated.get():
            self.__plot_animated()
        else:
            self.__plot_static()

    def __plot_animated(self):
        self.ax.clear()
        self.ax.set_xlim3d([min(self.model[0]), max(self.model[0])])
        self.ax.set_ylim3d([min(self.model[1]), max(self.model[1])])
        self.ax.set_zlim3d([min(self.model[2]), max(self.model[2])])

        n_frames = len(self.model[0])
        line, = self.ax.plot(self.model[0, 0:1], self.model[1, 0:1], self.model[2, 0:1])

        self.ani = animation.FuncAnimation(self.figure, self.__animate, n_frames, fargs=(self.model, line),
                                           interval=1, blit=False)
        self.is_animation_playing = True
        self.canvas.draw()

    def __animate(self, num, data, line):
        line.set_data(data[:2, :num])
        line.set_3d_properties(data[2, :num])

    def toggle_pause(self):
        if self.is_animation_playing:
            self.ani.event_source.stop()
            self.is_animation_playing = False
        else:
            self.ani.event_source.start()
            self.is_animation_playing = True

    def __plot_static(self):
        self.ax.clear()
        self.ax.plot(self.model[0, :], self.model[1, :], self.model[2, :])
        self.canvas.draw()

    def run(self):
        self.root.mainloop()