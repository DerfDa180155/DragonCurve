#version 330 core

in vec2 in_Position;
in float in_vNumber;

uniform float scaler;
uniform vec2 middle;

out float v_Number;

void main() {
    gl_Position = vec4((in_Position-middle)*scaler, 0.0, 1.0);
    v_Number = in_vNumber;
}