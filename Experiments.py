from manim import *
import numpy as np

class Pendulum(VGroup):
    CONFIG = {
        "theta_max": 10 * DEGREES,
        "theta_offset": 0,
        "theta_start": None,
        "length": 5,
        "origin": ORIGIN,
        "mass_config": {
            "radius": 0.5,
            "color": RED
        },
        "line_config": {
            "color": WHITE,
            "stroke_width": 3
        }
    }
    def __init__(self,**kwargs):
        digest_config(self,kwargs)
        super().__init__(**kwargs)
        self.mass = self.get_mass()
        self.string = self.get_string()
        self.vertical_line = self.string.copy()
        self.string.save_state()
        self.string.initial_state = self.string.copy()
        if self.theta_start == None:
            self.theta_start = self.theta_max
        self.mass.add_updater(lambda mob: mob.move_to(self.string.get_end()))
        self.rotate(self.theta_start)
        self.add(self.string,self.mass)

    def get_mass(self):
        return Dot(**self.mass_config)

    def get_string(self):
        return Line(
            self.origin,
            self.origin + DOWN * self.length,
            **self.line_config
        )

    def rotate(self,angle):
        self.string.rotate(angle, about_point=self.origin)

    def restore_string(self):
        self.string.restore()
        

    def get_angle(self):
        return angle_between(self.string.get_unit_vector(), DOWN) * 180 / PI

    def add_mass_updater(self):
        self.mass.add_updater(lambda mob: mob.move_to(self.string.get_end()))


class PendulumScene(Scene):
    CONFIG = {
        "total_time": 13,
        "dt_factor": 3,
        "gravity": 9.8
    }
    def construct(self):
        dt_calculate = 1 / self.camera.frame_rate
        roof = self.get_roof()
        roof.to_edge(UP)
        pendulum = Pendulum(
            origin=roof.get_bottom()
        )
        pendulum.restore_string()
        equation = TexMobject(r"\theta = \theta_{max}\cos\left(\sqrt{\frac{g}{L}}\cdot t\right)")
        equation.to_corner(DR)
        self.play(ShowCreation(roof))
        self.play(
            AnimationGroup(
                ShowCreation(pendulum.string),
                GrowFromCenter(pendulum.mass),
                lag_ratio=1
            )
        )
        self.play(
            Rotating(
                pendulum.string,
                radians=10*DEGREES,
                about_point=pendulum.origin,
                rate_func=smooth,
                run_time=1
            )
        )
        self.wait()
        self.play(
            Write(equation)
        )
        pendulum.add_updater(self.get_theta_func(pendulum))
        self.add(pendulum)
        self.wait(self.total_time)

    def get_theta_func(self,mob):
        func = lambda t: mob.theta_max * np.cos(
            t * np.sqrt(
                ( self.gravity / mob.length )
            )
        )
        def updater_func(mob,dt):
            mob.theta_offset += dt * self.dt_factor
            new_theta = func(mob.theta_offset)
            mob.restore_string()
            mob.rotate(new_theta)
        return updater_func

    def get_roof(self,size=0.2,**line_config):
        line = Line(
            ORIGIN, UR * size, **line_config
        )
        lines = VGroup(*[
            line.copy() for _ in range(30)
        ])
        lines.arrange(RIGHT,buff=0)
        down_line = Line(
            lines.get_corner(DL),
            lines.get_corner(DR),
            **line_config
        )
        return VGroup(lines, down_line)


class MmodNTracker(Scene):
    CONFIG = {
        "number_of_lines": 1000,
        "gradient_colors":[RED,YELLOW,BLUE],
        "end_value":100,
        "total_time":10,
    }
    def construct(self):
        circle = Circle().set_height(5)
        mod_tracker = ValueTracker(0)
        lines = self.get_m_mod_n_objects(circle,mod_tracker.get_value())
        lines.add_updater(
            lambda mob: mob.become(
                self.get_m_mod_n_objects(circle,mod_tracker.get_value())
                )
            )
        self.add(circle,lines)
        self.wait(3)
        self.play(
            mod_tracker.set_value,self.end_value,
            rate_func=linear,
            run_time=self.total_time
            )
        self.wait(3)

    def get_m_mod_n_objects(self,circle,x,y=None):
        if y==None:
            y = self.number_of_lines
        lines = VGroup()
        for i in range(y+1):
            start_point = circle.point_from_proportion((i%y)/y)
            end_point = circle.point_from_proportion(((i*x)%y)/y)
            line = Line(start_point,end_point).set_stroke(width=1)
            lines.add(line)
        lines.set_color_by_gradient(*self.gradient_colors)
        return lines

class NTest(ThreeDScene):

    def construct(self):

        self.set_camera_orientation(0.35*PI, 0.2*PI)
        axs = ThreeDAxes(x_min=0, x_max=2, y_min=0, y_max=2, z_min=0, z_max=2, number_line_config={"include_tip": True, "tip_height": 0.1})

        axs.scale(3)
        self.play(ShowCreation(axs))

        e1 = TexMobject(r"e_1").move_to([1, 1, 1])
        self.add_fixed_in_frame_mobjects(e1)

        self.play(Write(e1))
        self.wait(3)

        e2 = TexMobject(r"e_2").move_to([1, 1, 1])
        self.add_fixed_in_frame_mobjects(e2)

        self.play(Transform(e1, e2))

        self.wait(2)

class Gravity(Scene):
    CONFIG = {
        "g": 9.8,
        "radius": 3,
        "start_angle":-PI/4,
        "num_arrows":20,
        "dt_factor":1,
        "total_time":20,
    }
    def construct(self):
        self.dt = 1 / self.camera.frame_rate
        
        circle = Circle().set_height(self.radius*2)
        
        
        arrows = []
        N = self.num_arrows
        for i in range(N+1):
            arrow = Arrow(ORIGIN, self.radius*RIGHT)
            angle = self.start_angle+2*i*PI/N
            if angle > PI/2:
                angle = angle - 2*PI
            elif angle < -3*PI/2:
                angle = 2*PI + angle
            arrow.rotate(angle, about_point=ORIGIN)
            arrow.max_theta = -PI/2-angle
            arrow.time = 0
            arrow.add_updater(self.update_angle)
            arrows.append(arrow)
        self.add(circle, *arrows)
        self.wait(10)
    
    def update_angle(self, arrow, dt):
        g = self.g
        r = self.radius
        arrow.time += dt*self.dt_factor
        
        new_theta = arrow.max_theta * np.cos(arrow.time * np.sqrt(g/r))
        arrow.put_start_and_end_on(ORIGIN, ORIGIN+self.radius*RIGHT)
        arrow.rotate(-PI/2-new_theta, about_point=ORIGIN)