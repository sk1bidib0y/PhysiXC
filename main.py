from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, OptionList, Button, Static, Input, Button, Label
from textual.widgets.option_list import Option
from textual.containers import Container
import os
import ctypes
import math

# Link kinematics file
library_file = ""

if os.name == "nt":
  library_file = ".\\kinematics.dll"
else:
  library_file = "./kinematics.so"

kinematics = ctypes.CDLL(library_file)

# Load kinematics functions

"""Projectile Motion"""

# HORIZONTAL
kinematics.horizontal_initial_velocity.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_char]
kinematics.horizontal_initial_velocity.restype = ctypes.c_double

kinematics.horizontal_velocity.argtypes = [ctypes.c_double]
kinematics.horizontal_velocity.restype = ctypes.c_double

kinematics.horizontal_displacement.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.horizontal_displacement.restype = ctypes.c_double

# VERTICAL
kinematics.vertical_initial_velocity.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_char]
kinematics.vertical_initial_velocity.restype = ctypes.c_double

kinematics.vertical_velocity_with_time.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.vertical_velocity_with_time.restype = ctypes.c_double

kinematics.vertical_velocity_with_dist_v.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.vertical_velocity_with_dist_v.restype = ctypes.c_double

kinematics.vertical_displacement.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.vertical_displacement.restype = ctypes.c_double

"""Friction"""

# --- max static friction ---
kinematics.static_friction_max.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.static_friction_max.restype = ctypes.c_double

# --- kinetic friction ---
kinematics.kinetic_friction.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.kinetic_friction.restype = ctypes.c_double

# --- normal force ---
kinematics.normal_force.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
kinematics.normal_force.restype = ctypes.c_double

# --- coefficient of friction ---
kinematics.coefficient_of_friction.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.coefficient_of_friction.restype = ctypes.c_double

""""Momentum & Impulse"""
# momentum
kinematics.momentum.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.momentum.restype = ctypes.c_double

# impulse
kinematics.impulse.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.impulse.restype = ctypes.c_double

# velocity of elastic collision
kinematics.elastic_collision_velocity.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
kinematics.elastic_collision_velocity.restype = ctypes.c_double

# velocity of inelastic collision
kinematics.inelastic_collision_velocity.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
kinematics.inelastic_collision_velocity.restype = ctypes.c_double

# restitution coefficient
kinematics.restitution_coefficient.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
kinematics.restitution_coefficient.restype = ctypes.c_double


"""Rotational Motion"""
# frequency
kinematics.frequency.argtypes = [ctypes.c_double]
kinematics.frequency.restype = ctypes.c_double

# tangential velocity
kinematics.tangential_velocity.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.tangential_velocity.restype = ctypes.c_double

# tangential acceleration
kinematics.tangential_acceleration.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.tangential_acceleration.restype = ctypes.c_double

# centripetal acceleration
kinematics.centripetal_acceleration.argtypes = [ctypes.c_double, ctypes.c_double]
kinematics.centripetal_acceleration.restype = ctypes.c_double

LOGO = r"""
                ###################.              
                 #####           ##.              
                   ####.         ##.              
                    #####                         
                      ####.                       
                       #####                      
                         ##.                      
                       ###                        
                      ##.                         
                    ###                           
                   ###           ##.              
                 ##################.              
                ###################. 
"""

"""Primary Screens (Main Menu, Kinematics)"""
class MainMenuScreen(Screen):
    # The initial main menu screen.
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="menu_container"):
            yield Static(LOGO, id="logo")
            yield OptionList(
                Option("Mechanical Science", id="phy"),
                None,
                Option("Electrical Science", id="math"),
                None,
                Option("Exit", id="exit"),
                id="menuList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "phy":
            self.app.push_screen(KinematicsScreen())
        elif event.option_id == "exit":
            self.app.exit()

class KinematicsScreen(Screen):
    # Screen for Kinematics calculations.
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="kinematics_container"):
            yield OptionList(
                Option("Projectile Motion", id="projectileChoice"),
                None,
                Option("Friction Calculations", id="frictionChoice"),
                None,
                Option("Momentum & Impulse", id="momentum&ImpulseChoice"),
                None,
                Option("Rotational Motion", id="rotationalChoice"),
                None,
                Option("Back to main menu", id="back"),
                id="kinematicsList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "projectileChoice":
            self.app.push_screen(ProjectileScreen())  # Push ProjectileScreen here!
        elif event.option_id == "frictionChoice":
            self.app.push_screen(FrictionScreen())
        elif event.option_id == "momentum&ImpulseChoice":
            self.app.push_screen(MomentumImpulseScreen())
        elif event.option_id == "rotationalChoice":
            self.app.push_screen(RotationalScreen())
        elif event.option_id == "back":
            self.app.pop_screen()

"""Tertiary Screens"""

"""Projectile Motion Calculations"""
# HORIZONTAL

class HIVScreen(Screen):
    TITLE = "Horizontal Initial Velocity Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Initial Horizontal Velocity", type="number", id="u_value")
            yield Input(placeholder="Enter Angle in Degrees", type="number", id="theta")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                u_text = self.query_one("#u_value", Input).value
                angle_text = self.query_one("#theta", Input).value

                # 3. Convert strings to floats
                ux = float(u_text)
                angle = float(angle_text)

                result = kinematics.horizontal_initial_velocity(ux, angle, b'd')

                self.query_one("#result_label", Label).update(f"uₓ = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class HDScreen(Screen):
    TITLE = "Horizontal Distance Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HDContainer"):
            yield Input(placeholder="Enter Initial Horizontal Velocity", type="number", id="ux_value")
            yield Input(placeholder="Enter Time Taken (seconds)", type="number", id="time")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                ux_text = self.query_one("#ux_value", Input).value
                time_text = self.query_one("#time", Input).value

                # 3. Convert strings to floats
                ux = float(ux_text)
                time = float(time_text)

                result = kinematics.horizontal_displacement(ux, time)

                self.query_one("#result_label", Label).update(f"sₓ = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

# VERTICAL
class VIVScreen(Screen):
    TITLE = "Vertical Initial Velocity Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="VIVContainer"):
            yield Input(placeholder="Enter Initial Vertical Velocity (m/s)", type="number", id="vy_value")
            yield Input(placeholder="Enter Angle in Degrees", type="number", id="theta")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                vy_text = self.query_one("#vy_value", Input).value
                angle_text = self.query_one("#theta", Input).value

                # 3. Convert strings to floats
                vy = float(vy_text)
                angle = float(angle_text)

                result = kinematics.vertical_initial_velocity(vy, angle, b'd')

                self.query_one("#result_label", Label).update(f"vᵧ = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class VVWTScreen(Screen):
    TITLE = "Vertical Velocity Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="VVWTContainer"):
            yield Input(placeholder="Enter Initial Vertical Velocity (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter Time Taken (seconds)", type="number", id="time")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                v_text = self.query_one("#v_value", Input).value
                time_text = self.query_one("#time", Input).value

                # 3. Convert strings to floats
                vy = float(v_text)
                time = float(time_text)

                result = kinematics.vertical_velocity_with_time(vy, time)

                self.query_one("#result_label", Label).update(f"vᵧ = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class VVWDVScreen(Screen):
    TITLE = "Vertical Velocity With Distance and Velocity Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Initial Vertical Velocity (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter Vertical Displacement (m)", type="number", id="v_dist")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                v_text = self.query_one("#v_value", Input).value
                dist_text = self.query_one("#v_dist", Input).value

                # 3. Convert strings to floats
                vx = float(v_text)
                dist = float(dist_text)

                result = kinematics.vertical_velocity_with_dist_v(vx, dist)

                if math.isnan(result):
                    self.query_one("#result_label", Label).update("[red]Height is unreachable![/red]")
                else:
                    self.query_one("#result_label", Label).update(f"vᵧ = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class VDScreen(Screen):
    TITLE = "Vertical Displacement Calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Initial Vertical Velocity (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter time taken (seconds)", type="number", id="time")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                v_text = self.query_one("#v_value", Input).value
                dist_text = self.query_one("#time", Input).value

                # 3. Convert strings to floats
                vx = float(v_text)
                time = float(dist_text)

                result = kinematics.vertical_displacement(vx, time)

                self.query_one("#result_label", Label).update(f"sᵧ = {result:.2f} m")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

"""Friction Calculations"""
class FSMaxScreen(Screen):
    TITLE = "Max Static Friction Calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Coefficient of Static Friction (μs)", type="number", id="mus_val")
            yield Input(placeholder="Enter Normal Force (N)", type="number", id="n_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                mus_text = self.query_one("#mus_val", Input).value
                n_text = self.query_one("#n_val", Input).value

                mus = float(mus_text)
                n = float(n_text)

                result = kinematics.static_friction_max(mus, n)

                self.query_one("#result_label", Label).update(f"Fₛ,ₘₐₓ = {result:.2f} N")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()


class FKScreen(Screen):
    TITLE = "Kinetic Friction Calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Coefficient of Kinetic Friction (μk)", type="number", id="muk_val")
            yield Input(placeholder="Enter Normal Force (N)", type="number", id="n_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                muk_text = self.query_one("#muk_val", Input).value
                n_text = self.query_one("#n_val", Input).value

                muk = float(muk_text)
                n = float(n_text)

                result = kinematics.kinetic_friction(muk, n)

                self.query_one("#result_label", Label).update(f"Fₖ = {result:.2f} N")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()


class FNScreen(Screen):
    TITLE = "Normal Force Calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Mass (kg)", type="number", id="mass_val")
            yield Input(placeholder="Enter Incline Angle (degrees, 0 for flat ground)", type="number", id="angle_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                mass_text = self.query_one("#mass_val", Input).value
                angle_text = self.query_one("#angle_val", Input).value

                mass = float(mass_text)
                angle = float(angle_text) if angle_text else 0.0

                result = kinematics.normal_force(mass, 9.81, angle)

                self.query_one("#result_label", Label).update(f"Fₙ = {result:.2f} N")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()


class MuSScreen(Screen):
    TITLE = "Coefficient of Static Friction (μs)"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Max Static Friction Force (N)", type="number", id="fs_val")
            yield Input(placeholder="Enter Normal Force (N)", type="number", id="n_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                fs_text = self.query_one("#fs_val", Input).value
                n_text = self.query_one("#n_val", Input).value

                fs = float(fs_text)
                n = float(n_text)

                if n == 0:
                    self.query_one("#result_label", Label).update("[red]Normal Force cannot be 0![/red]")
                    return

                result = kinematics.coefficient_of_friction(fs, n)

                self.query_one("#result_label", Label).update(f"μₛ = {result:.2f}")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()


class MuKScreen(Screen):
    TITLE = "Coefficient of Kinetic Friction (μk)"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="HIVContainer"):
            yield Input(placeholder="Enter Kinetic Friction Force (N)", type="number", id="fk_val")
            yield Input(placeholder="Enter Normal Force (N)", type="number", id="n_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                fk_text = self.query_one("#fk_val", Input).value
                n_text = self.query_one("#n_val", Input).value

                fk = float(fk_text)
                n = float(n_text)

                if n == 0:
                    self.query_one("#result_label", Label).update("[red]Normal Force cannot be 0![/red]")
                    return

                result = kinematics.coefficient_of_friction(fk, n)

                if math.isnan(result):
                    self.query_one("#result_label", Label).update("[red]Invalid input values![/red]")
                else:
                    self.query_one("#result_label", Label).update(f"μₖ = {result:.4f}")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

"""Momentum & impulse calculations"""
class MomentumScreen(Screen):
    TITLE = "Momentum calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="MomentumContainer"):
            yield Input(placeholder="Enter Mass (kg)", type="number", id="m_value")
            yield Input(placeholder="Enter Velocity (m/s)", type="number", id="v_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                m_text = self.query_one("#m_value", Input).value
                v_text = self.query_one("#v_value", Input).value

                # 3. Convert strings to floats
                m = float(m_text)
                v = float(v_text)

                result = kinematics.momentum(m, v)

                self.query_one("#result_label", Label).update(f"p = {result:.2f} kg⋅m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class ImpulseScreen(Screen):
    TITLE = "Impulse calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="ImpulseContainer"):
            yield Input(placeholder="Enter Force (N)", type="number", id="F_value")
            yield Input(placeholder="Enter Time (s)", type="number", id="t_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                F_text = self.query_one("#F_value", Input).value
                t_text = self.query_one("#t_value", Input).value
                #v_text = self.query_one("#v_value", Input).value

                # 3. Convert strings to floats
                F = float(F_text)
                t = float(t_text)

                result = kinematics.impulse(F, t)

                self.query_one("#result_label", Label).update(f"J = {result:.2f} N⋅s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class ECVScreen(Screen):
    TITLE = "Elastic Collision Velocity calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="ECVContainer"):
            yield Input(placeholder="Enter Mass 1 (kg)", type="number", id="m_value")
            yield Input(placeholder="Enter Velocity 1 (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter Mass 2 (kg)", type="number", id="m2_value")
            yield Input(placeholder="Enter Velocity 2 (m/s)", type="number", id="v2_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                mOne_text = self.query_one("#m_value", Input).value
                vOne_text = self.query_one("#v_value", Input).value
                mTwo_text = self.query_one("#m2_value", Input).value
                vTwo_text = self.query_one("#v2_value", Input).value

                # 3. Convert strings to floats
                mOne = float(mOne_text)
                vOne = float(vOne_text)
                mTwo = float(mTwo_text)
                vTwo = float(vTwo_text)

                result = kinematics.elastic_collision_velocity(mOne, vOne, mTwo, vTwo)

                self.query_one("#result_label", Label).update(f"v = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class ICVScreen(Screen):
    TITLE = "Inelastic Collision Velocity calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="ICVContainer"):
            yield Input(placeholder="Enter Mass 1 (kg)", type="number", id="m_value")
            yield Input(placeholder="Enter Velocity 1 (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter Mass 2 (kg)", type="number", id="m2_value")
            yield Input(placeholder="Enter Velocity 2 (m/s)", type="number", id="v2_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                mOne_text = self.query_one("#m_value", Input).value
                vOne_text = self.query_one("#v_value", Input).value
                mTwo_text = self.query_one("#m2_value", Input).value
                vTwo_text = self.query_one("#v2_value", Input).value

                # 3. Convert strings to floats
                mOne = float(mOne_text)
                vOne = float(vOne_text)
                mTwo = float(mTwo_text)
                vTwo = float(vTwo_text)

                result = kinematics.inelastic_collision_velocity(mOne, vOne, mTwo, vTwo)

                self.query_one("#result_label", Label).update(f"v = {result:.2f} m/s")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class ROScreen(Screen):
    TITLE = "Restitution coefficient calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="ROContainer"):
            yield Input(placeholder="Enter Mass 1 (kg)", type="number", id="m_value")
            yield Input(placeholder="Enter Velocity 1 (m/s)", type="number", id="v_value")
            yield Input(placeholder="Enter Mass 2 (kg)", type="number", id="m2_value")
            yield Input(placeholder="Enter Velocity 2 (m/s)", type="number", id="v2_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                mOne_text = self.query_one("#m_value", Input).value
                vOne_text = self.query_one("#v_value", Input).value
                mTwo_text = self.query_one("#m2_value", Input).value
                vTwo_text = self.query_one("#v2_value", Input).value

                # 3. Convert strings to floats
                mOne = float(mOne_text)
                vOne = float(vOne_text)
                mTwo = float(mTwo_text)
                vTwo = float(vTwo_text)

                result = kinematics.restitution_coefficient(mOne, vOne, mTwo, vTwo)

                self.query_one("#result_label", Label).update(f"e = {result:.2f}")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

"""Rotational Motion Calculations"""

class FrequencyScreen(Screen):
    TITLE = "Frequency calculation"
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="FrequencyContainer"):
            yield Input(placeholder="Enter Period (s)", type="number", id="p_value")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                # 2. Query the input widgets by ID and read .value
                f_text = self.query_one("#p_value", Input).value

                # 3. Convert strings to floats
                f = float(f_text)

                result = kinematics.frequency(f)

                self.query_one("#result_label", Label).update(f"f = {result} Hz")

            except ValueError:
                # Triggers if the user leaves the box empty or types letters!
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class TVScreen(Screen):
    TITLE = "Tangential velocity calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="TVContainer"):
            yield Input(placeholder="Enter Angular Velocity", type="number", id="av_val")
            yield Input(placeholder="Enter Radius", type="number", id="r_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                av_text = self.query_one("#av_val", Input).value
                r_text = self.query_one("#r_val", Input).value

                av = float(av_text)
                r = float(r_text)

                if r == 0:
                    self.query_one("#result_label", Label).update("[red]Radius cannot be 0![/red]")
                    return

                result = kinematics.tangential_velocity(av, r)

                if math.isnan(result):
                    self.query_one("#result_label", Label).update("[red]Invalid input values![/red]")
                else:
                    self.query_one("#result_label", Label).update(f"vₜ = {result:.4f}")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class TAScreen(Screen):
    TITLE = "Tangential acceleration calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="TAContainer"):
            yield Input(placeholder="Enter Angular Acceleration", type="number", id="aa_val")
            yield Input(placeholder="Enter Radius", type="number", id="r_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                aa_text = self.query_one("#aa_val", Input).value
                r_text = self.query_one("#r_val", Input).value

                aa = float(aa_text)
                r = float(r_text)

                if r == 0:
                    self.query_one("#result_label", Label).update("[red]Radius cannot be 0![/red]")
                    return

                result = kinematics.tangential_acceleration(aa, r)

                if math.isnan(result):
                    self.query_one("#result_label", Label).update("[red]Invalid input values![/red]")
                else:
                    self.query_one("#result_label", Label).update(f"aₜ = {result:.4f}")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()

class CAScreen(Screen):
    TITLE = "Centripetal acceleration calculation"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="CAContainer"):
            yield Input(placeholder="Enter Tangential Velocity", type="number", id="tv_val")
            yield Input(placeholder="Enter Radius", type="number", id="r_val")
            yield Button("Calculate", id="calc_button", variant="primary")
            yield Button("Go Back", id="back_button", variant="default")
            yield Label("", id="result_label")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calc_button":
            try:
                tv_text = self.query_one("#tv_val", Input).value
                r_text = self.query_one("#r_val", Input).value

                tv = float(tv_text)
                r = float(r_text)

                if r == 0:
                    self.query_one("#result_label", Label).update("[red]Radius cannot be 0![/red]")
                    return

                result = kinematics.centripetal_acceleration(tv, r)

                if math.isnan(result):
                    self.query_one("#result_label", Label).update("[red]Invalid input values![/red]")
                else:
                    self.query_one("#result_label", Label).update(f"aₙ = {result:.4f}")

            except ValueError:
                self.query_one("#result_label", Label).update("[red]Please enter valid numbers![/red]")

        elif event.button.id == "back_button":
            self.app.pop_screen()


"""
Secondary Screens (Projectile Motion, Friction, Momentum & Impulse, Rotational Motion)
"""

class ProjectileScreen(Screen):
    # Screen for Projectile Motion Calculations.
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("")
        with Container(id="kinematics_container"):
            yield OptionList(
                Option("Horizontal Initial Velocity", id="HIV"),
                None,
                Option("Horizontal Velocity", id="HV"),
                None,
                Option("Horizontal Distance (Range)", id="HD"),
                None,
                None,
                Option("Vertical Initial Velocity", id="VIV"),
                None,
                Option("Vertical Velocity (Time)", id="VVT"),
                None,
                Option("Vertical Velocity (Distance and Velocity)", id="VVDV"),
                None,
                Option("Vertical Distance", id="VD"),
                None,
                Option("Back to main menu", id="back"),
                id="kinematicsList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "HIV":
            self.app.push_screen(HIVScreen())  # Push your specific solver screen!
        elif event.option_id == "HV":
            self.notify("In projectile Motion, Aₓ = 0, thus Vₓ = Uₓ!")
        elif event.option_id == "HD":
            self.app.push_screen(HDScreen())
        elif event.option_id == "VIV":
            self.app.push_screen(VIVScreen())
        elif event.option_id == "VVT":
            self.app.push_screen(VVWTScreen())
        elif event.option_id == "VVDV":
            self.app.push_screen(VVWDVScreen())
        elif event.option_id == "VD":
                self.app.push_screen(VDScreen())
        elif event.option_id == "back":
            self.app.pop_screen()  # Fixed ID check


class FrictionScreen(Screen):
    # Screen for Friction Calculations.
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("")
        with Container(id="kinematics_container"):
            yield OptionList(
                Option("Max Static Friction Force (Fs,max)", id="FSMAX"),
                None,
                Option("Kinetic Friction Force (Fk)", id="FK"),
                None,
                Option("Normal Force (Flat / Angled)", id="FN"),
                None,
                Option("Coefficient of Static Friction (μs)", id="MUS"),
                None,
                Option("Coefficient of Kinetic Friction (μk)", id="MUK"),
                None,
                Option("Applied Force Threshold (Impending Motion)", id="AFT"),
                None,
                Option("Back to main menu", id="back"),
                id="kinematicsList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "FSMAX":
            self.app.push_screen(FSMaxScreen())
        elif event.option_id == "FK":
            self.app.push_screen(FKScreen())
        elif event.option_id == "FN":
            self.app.push_screen(FNScreen())
        elif event.option_id == "MUS":
            self.app.push_screen(MuSScreen())
        elif event.option_id == "MUK":
            self.app.push_screen(MuKScreen())
        elif event.option_id == "AFT":
            self.notify("To move an object, F_applied must exceed Fs,max (μs * N)!")
        elif event.option_id == "back":
            self.app.pop_screen()

class MomentumImpulseScreen(Screen):
    # Screen for Projectile Motion Calculations.
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("")
        with Container(id="momentum_impulse_container"):
            yield OptionList(
                Option("Momentum", id="momentum"),
                None,
                Option("Impulse", id="impulse"),
                None,
                Option("Elastic collision velocity", id="ECV"),
                None,
                Option("Inelastic collision velocity", id="ICV"),
                None,
                Option("Restitution coefficient", id="RO"),
                None,
                Option("Back to main menu", id="back"),
                id="kinematicsList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "momentum":
            self.app.push_screen(MomentumScreen())
        elif event.option_id == "impulse":
            self.app.push_screen(ImpulseScreen())
        elif event.option_id == "ECV":
            self.app.push_screen(ECVScreen())
        elif event.option_id == "ICV":
            self.app.push_screen(ICVScreen())
        elif event.option_id == "RO":
            self.app.push_screen(ROScreen())
        elif event.option_id == "back":
            self.app.pop_screen()  # Fixed ID check

class RotationalScreen(Screen):
    # Screen for Projectile Motion Calculations.
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("")
        with Container(id="rotational_container"):
            yield OptionList(
                Option("Frequency", id="freq"),
                None,
                Option("Tangential velocity", id="TV"),
                None,
                Option("Tangential acceleration", id="TA"),
                None,
                Option("Centripetal acceleration", id="CA"),
                None,
                Option("Back to main menu", id="back"),
                id="kinematicsList"
            )
        yield Footer()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id == "freq":
            self.app.push_screen(FrequencyScreen())
        elif event.option_id == "TV":
            self.app.push_screen(TVScreen())
        elif event.option_id == "TA":
            self.app.push_screen(TAScreen())
        elif event.option_id == "CA":
            self.app.push_screen(CAScreen())
        elif event.option_id == "back":
            self.app.pop_screen()  # Fixed ID check


class Solver(App[None]):
    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def on_mount(self) -> None:
        # When the app starts, push the main menu screen.
        self.push_screen(MainMenuScreen())

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = Solver()
    app.run()