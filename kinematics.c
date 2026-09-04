#include <stdio.h>
#include <math.h>

#define PI                      3.14159265358979323846
#define GRAVITY                 9.81
#define HORIZONTAL_ACCELERATION 0.0
#define VERTICAL_ACCELERATION   -GRAVITY

// ==PROJECTILE MOTION==

// HORIZONTAL
double horizontal_initial_velocity(double initial_speed, double angle, char angle_choice);
double horizontal_velocity(double initial_velocity, double time);
double horizontal_displacement(double initial_velocity, double time);

// VERTICAL
double vertical_initial_velocity(double initial_speed, double angle, char angle_choice);
double vertical_velocity_with_time(double initial_vertical_velocity, double time);
double vertical_velocity_with_dist_v(double initial_vertical_velocity, double vertical_displacement);
double vertical_displacement(double initial_vertical_velocity, double time);

// ==FRICTION==
double static_friction_max(double mu_s, double n);
double kinetic_friction(double mu_k, double n);
double normal_force(double mass, double gravity, double angle_deg);
double coefficient_of_friction(double force, double n);

int main(void) {
    return 0;
}

// HORIZONTAL
double horizontal_initial_velocity(double initial_speed, double angle, char angle_choice) {
    if (angle_choice == 'd') {
        return initial_speed * cos(angle * (PI / 180.0));
    }
    // Default to radians
    return initial_speed * cos(angle);
}

double horizontal_velocity(double initial_velocity, double time) {
    return initial_velocity + (HORIZONTAL_ACCELERATION * time);
}

double horizontal_displacement(double initial_velocity, double time) {
    return (initial_velocity * time) + (0.5 * HORIZONTAL_ACCELERATION * time * time);
}

// VERTICAL
double vertical_initial_velocity(double initial_speed, double angle, char angle_choice) {
    if (angle_choice == 'd') {
        return initial_speed * sin(angle * (PI / 180.0));
    }
    // Default to radians
    return initial_speed * sin(angle);
}

double vertical_velocity_with_time(double initial_vertical_velocity, double time) {
    return initial_vertical_velocity + (VERTICAL_ACCELERATION * time);
}

double vertical_velocity_with_dist_v(double initial_vertical_velocity, double vert_disp) {
    double v_squared = (initial_vertical_velocity * initial_vertical_velocity) + (2.0 * VERTICAL_ACCELERATION * vert_disp);
    if (v_squared < 0.0) {
        return NAN; // Return NAN if height is unreachable
    }
    return sqrt(v_squared);
}

double vertical_displacement(double initial_vertical_velocity, double time) {
    return (initial_vertical_velocity * time) + (0.5 * VERTICAL_ACCELERATION * time * time);
}

// ==FRICTION==
double static_friction_max(double mu_s, double n) {
    return mu_s * n;
}
double kinetic_friction(double mu_k, double n) {
    return mu_k * n;
} 
double normal_force(double mass, double gravity, double angle_deg) {
    double angle_rad = angle_deg * (PI / 180.0);
    return mass * gravity * cos(angle_rad);
}
double coefficient_of_friction(double force, double n) {
    if (n == 0.0) {
        return NAN; // Return NAN if normal force is zero
    }
    return force / n;
}

// ==MOMENTUM AND IMPULSE==
double momentum(double mass, double velocity) {
    return mass * velocity;
}

double impulse(double force, double time) {
    return force * time;
}

double elastic_collision_velocity(double m1, double v1, double m2, double v2) {
    return ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2;
}

double inelastic_collision_velocity(double m1, double v1, double m2, double v2) {
    return (m1 * v1 + m2 * v2) / (m1 + m2);
}

double restitution_coefficient(double v1_initial, double v1_final, double v2_initial, double v2_final) {
    double relative_velocity_initial = v1_initial - v2_initial;
    double relative_velocity_final = v2_final - v1_final;
    if (relative_velocity_initial == 0.0) {
        return NAN; // Return NAN or error indicator if initial relative velocity is zero
    }
    return relative_velocity_final / relative_velocity_initial;
}

// ==ROTATIONAL MOTION==
double frequency(double period) {
    if (period == 0.0) {
        return NAN; // Return NAN or error indicator if period is zero
    }
    return 1.0 / period;
}

double tangential_velocity(double angular_velocity, double radius) {
    return angular_velocity * radius;
}

double tangential_acceleration(double angular_acceleration, double radius) {
    return angular_acceleration * radius;
}

double centripetal_acceleration(double tangential_velocity, double radius) {
    if (radius == 0.0) {
        return NAN; // Return NAN or error indicator if radius is zero
    }
    return (tangential_velocity * tangential_velocity) / radius;
}