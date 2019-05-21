#pragma once

#include "ICommand.h"
#include "OpenGL.h"
#include "Color.h"

namespace Crawfis
{
	namespace Graphics
	{
		class ClearFrameCommand : public Collections::IGenericCommand
		{
		public:
			ClearFrameCommand(Color& clearColor = Colors::Transparent, float clearDepth = 1.0f)
			{
				this->clearColor = clearColor;
				this->clearDepth = clearDepth;
			}
			virtual void Execute()
			{
				glClearColor(clearColor.r, clearColor.g, clearColor.b, clearColor.a);
				glClearDepthf(clearDepth);
				glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
			}
		private:
			Color clearColor;
			float clearDepth;
		};
	}
}