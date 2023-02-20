#version 460 core

layout (location = 0) in vec3 position;
uniform mat4 projMat;
uniform mat4 viewMat;
uniform mat4 modelMat;
//in vec3 color;

void main()
{
    gl_Position = projMat* viewMat* modelMat * vec4(position,1.0);
    //gl_Position = vec4(position, 1.0);
    //vertexColor = vec4(0.0f,1.0f,0.0f,1.0f);
}