from manim import *
from qiskit.circuit.library import IGate, XGate, YGate, ZGate, HGate, SGate, RXGate, RYGate, RZGate, CXGate, CZGate

#I = IGate().to_matrix()
#X = XGate().to_matrix()
#Y = YGate().to_matrix()
#Z = ZGate().to_matrix()
#H = HGate().to_matrix()
#S = SGate().to_matrix()
RX = lambda t:RXGate(t).to_matrix()
RY = lambda t:RYGate(t).to_matrix()
RZ = lambda t:RZGate(t).to_matrix()
#CX = CXGate().to_matrix()
#CZ = CZGate().to_matrix()

class GeoMatrix(VGroup):
    CONFIG = {
        "origin": ORIGIN,
        "scale": 1,
        "square_color": WHITE,
        "circle_color": WHITE,
        "arrow_color": RED
    }
    def __init__(self, matrix=[[1,0],[0,1]], origin=ORIGIN, **kwargs):
        self.matrix = np.array(matrix)
        self.shape = self.matrix.shape
        self.coordinates = np.empty([*self.shape, 3])
        digest_config(self, kwargs)
        super().__init__(**kwargs)
        self.init_coordinates()
        self.init_squares()
        self.init_circles()
        self.init_arrows()
        
    def init_coordinates(self):
        M, N = self.shape
        s = self.scale
        for i in range(M):
            for j in range(N):
                c = self.origin+(i+0.5-M/2)*s*RIGHT+(j+0.5-N/2)*s*DOWN
                self.coordinates[i][j] = c
        
    def init_squares(self):
        M, N = self.shape
        for i in range(M):
            for j in range(N):
                square = Square()
                square.move_to(self.coordinates[i][j])
                square.set_stroke(self.square_color)
                square.scale(self.scale/2)
                self.add(square)
    
    def init_circles(self):
        M, N = self.shape
        for i in range(M):
            for j in range(N):
                mij = self.matrix[i][j]
                cij = self.coordinates[i][j]
                circle = Circle()
                circle.move_to(cij)
                circle.set_stroke(self.circle_color)
                circle.scale(self.scale/2*abs(mij))
                self.add(circle)
                
    def init_arrows(self):
        M, N = self.shape
        for i in range(M):
            for j in range(N):
                mij = self.matrix[i][j]
                cij = self.coordinates[i][j]
                if mij == 0:
                    end = cij
                else:
                    end = cij+RIGHT*0.5*self.scale
                arrow = Arrow()
                arrow.put_start_and_end_on(cij, end)
                arrow.set_stroke(self.arrow_color)
                arrow.set_fill(self.arrow_color)
                arrow.rotate(np.angle(mij), about_point=cij)
                self.add(arrow)

def decimal_in_text(text1, decimal_number, text2):
    g = VGroup(TextMobject(text1), decimal_number, TextMobject(text2))
    g[0].next_to(decimal_number,LEFT,buff=0.05)
    g[2].next_to(decimal_number,RIGHT,buff=0.05)
    return g
    
class GeoMatrixTest(Scene):
    def construct(self):
        theta = ValueTracker(0)
        
        rx_value = DecimalNumber(0).add_updater(lambda v: v.set_value(theta.get_value()))
        rx_tg = decimal_in_text("$R_x$(", rx_value, ")")
        rx = GeoMatrix().add_updater(lambda m: m.become(GeoMatrix(RX(theta.get_value())).shift(LEFT*2.5)))
        rx_tg.next_to(rx, UP*1.5)
        
        ry_value = rx_value.copy()
        ry_tg = decimal_in_text("$R_y$(", ry_value, ")")
        ry = GeoMatrix().add_updater(lambda m: m.become(GeoMatrix(RY(theta.get_value()))))
        ry_tg.next_to(ry, UP*1.5)
        
        rz_value = rx_value.copy()
        rz_tg = decimal_in_text("$R_z$(", rz_value, ")")
        rz = GeoMatrix().add_updater(lambda m: m.become(GeoMatrix(RZ(theta.get_value())).shift(RIGHT*2.5)))
        rz_tg.next_to(rz, UP*1.5)
        
        self.play(ShowCreation(VGroup(rx_tg, rx, ry_tg, ry, rz_tg, rz)))
        self.play(theta.set_value, 2*PI, run_time=5)