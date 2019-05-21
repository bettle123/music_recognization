#pragma once

#include "IShaderRoutine.h"
#include <string>

namespace Crawfis
{
	namespace Graphics 
	{
		class GeometryRoutine : public IShaderRoutine
		{
		public:
			GeometryRoutine(std::string sourceCode)
			{
				this->sourceCode = sourceCode;
				created = false;
				guid = 0;
			}
			//
			// Get the shader id (Guid).
			// If the routine has not been created or compiled,
			// perform that before returning the guid.
			//
			virtual unsigned int getGUID() const
			{
				if( !created )
				{
					CreateRoutine();
				}
				return guid;
			}
		private:
			void CreateRoutine() const
			{
			}
		private:
			unsigned int guid;
			bool created;
			std::string sourceCode;
		};
	}
}
