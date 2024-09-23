#version 330 core

in vec3 v_Color;
in float v_Number;

uniform vec3 startColor;
uniform vec3 endColor;
uniform int amount;

out vec4 f_Color;

vec3 tempColor;
vec3 tempColor2;
vec3 finalColor;

void main() {
    tempColor = (endColor-startColor)/amount;
    tempColor2 = tempColor*v_Number;
    finalColor = startColor + tempColor2;
    f_Color = vec4(finalColor/255, 1.0);
}