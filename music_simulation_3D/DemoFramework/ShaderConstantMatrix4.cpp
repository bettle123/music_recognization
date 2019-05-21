#include "ShaderConstantMatrix4.h"
#include "OpenGL.h"
#include <string>

Crawfis::Graphics::ShaderConstantMatrix4::ShaderConstantMatrix4(std::string constantName)
{
	this->constantName = constantName;
}

Crawfis::Graphics::ShaderConstantMatrix4::~ShaderConstantMatrix4() {}

void Crawfis::Graphics::ShaderConstantMatrix4::setValue(const Crawfis::Math::Matrix4& value)
{
	this->value = value;
}
void Crawfis::Graphics::ShaderConstantMatrix4::OnLink(unsigned int shaderID)
{
	constantLocation = glGetUniformLocation(shaderID, constantName.c_str());
}

void Crawfis::Graphics::ShaderConstantMatrix4::OnShaderEnabled(unsigned int shaderID)
{
	if( constantLocation >= 0)
		glUniformMatrix4fv(constantLocation, 1, false, &value[0]);
}
