from manim import *
import random
import numpy as np

class Qubit(ThreeDScene):
    def construct(self):
        
        axis = ThreeDAxes().scale(0.5)
        sphere = Sphere().set_fill(BLACK)
        arrow = Arrow().put_start_and_end_on(ORIGIN, UP).set_fill(RED).set_stroke(RED)
        arrow.rotate(axis=RIGHT, angle=PI/2, about_point=ORIGIN)

        ket_0 = TextMobject(r"$\ket{0}$").next_to(axis, np.array([0,0,1]))
        ket_1 = TextMobject(r"$\ket{1}$").next_to(axis, -np.array([0,0,1]))
        ket_p = TextMobject(r"$\ket{+}$").next_to(axis, RIGHT)
        ket_m = TextMobject(r"$\ket{-}$").next_to(axis, LEFT)
        ket_pi = TextMobject(r"$\ket{+i}$").next_to(axis, UP)
        ket_mi = TextMobject(r"$\ket{-i}$").next_to(axis, DOWN)
        axis_name_group = VGroup(ket_0, ket_1, ket_p, ket_m, ket_pi, ket_mi)
        
        qubit = TextMobject(r"$\alpha \ket{0} + \beta \ket{1}$")
        
        gate_list = [TextMobject(r'H').to_corner(UP),
                      TextMobject(r'$R_z(\frac{\pi}{2})$').to_corner(UP),
                      TextMobject(r'$R_x(\frac{\pi}{2})$').to_corner(UP),
                      TextMobject(r'$R_y(\frac{\pi}{2})$').to_corner(UP)]
        
        rotation_list = [(PI, [1,0,1]),
                         (PI/2, [0,0,1]),
                         (PI/2, [1,0,0]),
                         (PI/2, [0,1,0])]
                         
        
        self.set_camera_orientation(phi=75*DEGREES, theta=0)
       
        self.wait()
        self.play(ShowCreation(axis))
        
        self.begin_ambient_camera_rotation(rate = 0.05)
        
        self.add_fixed_orientation_mobjects(ket_0, ket_1, ket_p, ket_m, ket_pi, ket_mi)
        self.play(ShowCreation(axis_name_group),
                  ShowCreation(sphere),
                  ShowCreation(arrow))
        
        i = 0
        i_last = len(gate_list)
        self.add_fixed_in_frame_mobjects(gate_list[0])
        self.play(Write(gate_list[0]),
                  Rotate(arrow, 
                         about_point=ORIGIN,
                         angle=rotation_list[i][0], 
                         axis=np.array(rotation_list[i][1])))
        
        i += 1
        while i < i_last:
            self.add_fixed_in_frame_mobjects(gate_list[i])
            self.play(FadeOut(gate_list[i-1]),
                      FadeIn(gate_list[i]),
                      Rotate(arrow, 
                             about_point=ORIGIN,
                             angle=rotation_list[i][0], 
                             axis=np.array(rotation_list[i][1])))
            i += 1
        
        self.play(Uncreate(gate_list[-1]),
                  Uncreate(axis_name_group),
                  Uncreate(axis),
                  Uncreate(sphere),
                  Uncreate(arrow))
        self.stop_ambient_camera_rotation()
        self.wait()
