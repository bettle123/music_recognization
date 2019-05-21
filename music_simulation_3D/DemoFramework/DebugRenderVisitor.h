#pragma once

#include "IVisitor.h"
#include "IDrawableNode.h"
#include "ITransformNode.h"
#include "IStateNode.h"
#include "GroupNode.h"
#include "OpenGL.h"

namespace Crawfis
{
	namespace Graphics
	{
		class DebugRenderVisitor : public IVisitor
		{
		public:
			virtual void Visit(IDrawableNode* drawable)
			{
				drawable->Draw();
				GLenum error = ::glGetError();
				if( error != 0)
					printf("OpenGL reported an error while traversing the drawable %s\n", drawable->ToString());
			}
			virtual void Visit(ITransformNode* transform)
			{
				transform->Apply();
				GLenum error = ::glGetError();
				if( error != 0)
					printf("OpenGL reported an error while applying the transformation %s\n", transform->ToString());
				transform->AcceptSubject(this);
				transform->Unapply();
				error = ::glGetError();
				if( error != 0)
					printf("OpenGL reported an error while unapplying the transformation %s\n", transform->ToString());
			}
			virtual void Visit(IStateNode* state)
			{
				state->Apply();
				GLenum error = ::glGetError();
				if( error != 0)
					printf("OpenGL reported an error while applying the state %s\n", state->ToString());
				state->AcceptSubject(this);
				state->Unapply();
				error = ::glGetError();
				if( error != 0)
					printf("OpenGL reported an error while unapplying the state %s\n", state->ToString());
			}
			virtual void Visit(GroupNode* group)
			{
				group->AcceptChildren(this);
			}
		};
	}
}