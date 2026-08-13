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
        return -1.0; // Return -1 or error indicator if height is unreachable
    }
    return sqrt(v_squared);
}

double vertical_displacement(double initial_vertical_velocity, double time) {
    return (initial_vertical_velocity * time) + (0.5 * VERTICAL_ACCELERATION * time * time);
}

// Friction calculation
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
        return -1.0; // Return -1 or error indicator if normal force is zero
    }
    return force / n;
}
