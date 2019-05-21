#include "OpenGL.h"

#include <string>
#include <vector>

// Includes to create the cube
#include "ISceneNode.h"
#include "ModelManager.h"
#include "DrawableProxy.h"
#include "DrawableCubeSolution.h"
#include "DrawableSphereSolution.h"
#include "DrawableFloorSolution.h"

// Material includes
#include "SolidColorMaterialSolution.h"
#include "ShadedMaterial.h"
#include "MaterialProxy.h"
#include "MaterialManager.h"
#include "ShaderConstantMaterial.h"
#include "Color.h"

#include "BlankTexture2D.h"
#include "TextureBinding.h"
#include "TextureBindManager.h"
#include "TextureBindManagerOpenGL.h"
#include "TextureDataImage.h"
#include "SamplerApplicator.h"
#include "SimpleShaderMaterial.h"
#include "TexParam2DNoMipMap.h"
#include "TexParam2DMipMap.h"

// Includes for the camera
#include "ExaminerCameraNode.h"
#include "PerspectiveTransformSolution.h"
#include "LookAtTransformSolution.h"
#include "ShaderConstantModelView.h"

// Lights
#include "PointLight.h"
#include "DirectionalLight.h"
#include "LightManager.h"
#include "ShaderConstantLights.h"

#include "RenderTargetProxy.h"
#include "RenderTarget.h"
#include "RenderManager.h"
#include "ClearFrameCommand.h"
#include "SwapCommand.h"

// Includes for walking the scene graph
#include "DebugRenderVisitor.h"
#include "PrintSceneVisitor.h"

// Interaction
std::vector<IMouseHandler*> mouseHandlers;
std::vector<IKeyboardHandler*> keyboardHandlers;

// Includes Windows
#include <Windows.h>

// Includes Time
#include <time.h>


using namespace Crawfis::Graphics;
using namespace Crawfis::Math;
using namespace std;


ISceneNode* rootSceneNode;
IVisitor* renderVisitor;
ExaminerCameraNode* examiner;

int windowGUID;
int windowWidth;
int windowHeight; 


// 01/14/2019
int number_screenshot = 12000;
string classes = "musical_symbol_quarter_rest";
string texture_dir = "C:\\Users\\san34\\Desktop\\2018_summer\\project\\music_simulation_software\\Scores\\Output\\0213_Symbol\\"+ classes +"\\";
vector<string> all_textures_name;


ISceneNode* CreateFrameBuffer(Crawfis::Graphics::ISceneNode * scene);

void CreateGLUTWindow(std::string windowTitle)
{
	
	windowWidth = 400;
	windowHeight = 400;
	
	/*
	windowWidth = 1200;
	windowHeight = 800;
	*/
	glutInitDisplayMode(GLUT_RGB);
	glutInitWindowSize(windowWidth, windowHeight);
	windowGUID = glutCreateWindow(windowTitle.c_str());
}

void InitializeOpenGLExtensions()
{
	GLenum err = glewInit();
	if (GLEW_OK != err)
	{
		/* Problem: glewInit failed, something is seriously wrong. */
		fprintf(stderr, "Error: %s\n", glewGetErrorString(err));
		throw "Error initializing GLEW";
	}

	fprintf(stdout, "Status: Using GLEW %s\n", glewGetString(GLEW_VERSION));
}

void InitializeDevices()
{
	CreateGLUTWindow("Music Simulation");
	InitializeOpenGLExtensions();
	glDisable(GL_CULL_FACE);
}

void CreateLights()
{
	/*
	Random Factor:
		PointLight position
		@random LightPosition
		random range:
			@x: -2.0~2.0
			@y: 1.5~2.5
			@z: -2.0~2.0
	*/
	Vector3 LightPosition((rand() % 400 / 100.0 - 2.0), (rand()%100/100.0+1.5), (rand() % 400 / 100.0 - 2.0));
	
	PointLight* pointLight = new PointLight("light0-pt");
	pointLight->setPosition(LightPosition);
	LightManager::Instance()->SetLight(0, pointLight);
	DirectionalLight* dirLight = new DirectionalLight("light1-dir");
	dirLight->setDirection(Vector3(10, 1, 1));
	LightManager::Instance()->SetLight(1, dirLight);
	
}
void CreateGoldMaterial()
{
	VertexRoutine* vertexRoutine = new VertexRoutine("..\\Media\\Shaders\\VertexLight.glsl");
	FragmentRoutine* fragmentRoutine = new FragmentRoutine("..\\Media\\Shaders\\SolidColorSolution.frag");
	IShaderProgram* shaderProgram = new ShaderProgramWithMatrices(vertexRoutine, fragmentRoutine);

	Color gold(0.8314f, 0.6863f, 0.2169f, 1.0f);
	ShadedMaterial* shinyGold = new ShadedMaterial(shaderProgram);
	shinyGold->setAmbientReflection(0.01f*gold);
	shinyGold->setDiffuseReflection(0.7f*gold);
	shinyGold->setSpecularReflection(0.25f*gold);
	shinyGold->setShininess(100.0f);

	ShaderConstantMaterial* materialConstant = new ShaderConstantMaterial("frontMaterial");
	materialConstant->setValue(shinyGold);
	ShaderConstantLights* lightConstant = new ShaderConstantLights();
	ShaderConstantCollection* shaderConstantList = new ShaderConstantCollection();
	shaderConstantList->AddConstant(materialConstant);
	shaderConstantList->AddConstant(lightConstant);
	shaderProgram->setShaderConstant(shaderConstantList);

	MaterialManager::Instance()->RegisterMaterial("ShinyGold", shinyGold);
}


void CreateWhiteMaterial()
{
	VertexRoutine* vertexRoutine = new VertexRoutine("..\\Media\\Shaders\\VertexLight.glsl");
	FragmentRoutine* fragmentRoutine = new FragmentRoutine("..\\Media\\Shaders\\SolidColorSolution.frag");
	IShaderProgram* shaderProgram = new ShaderProgramWithMatrices(vertexRoutine, fragmentRoutine);

	Color white(1.0f, 1.0f, 1.0f, 1.0f);
	ShadedMaterial* shinyWhite = new ShadedMaterial(shaderProgram);
	/*
	float random_ambient = 3;
	float random_diffuse = 1.5;
	float random_specular = 0.25;
	shinyWhite->setAmbientReflection(random_ambient*white);
	shinyWhite->setDiffuseReflection(random_diffuse*white);
	shinyWhite->setSpecularReflection(random_specular*white);
	shinyWhite->setShininess(20.0f);
	*/
	
	shinyWhite->setAmbientReflection(0.01f*white);
	shinyWhite->setDiffuseReflection(0.7f*white);
	shinyWhite->setSpecularReflection(0.25f*white);
	shinyWhite->setShininess(10.0f);
	
	ShaderConstantMaterial* materialConstant = new ShaderConstantMaterial("frontMaterial");
	materialConstant->setValue(shinyWhite);
	ShaderConstantLights* lightConstant = new ShaderConstantLights();
	ShaderConstantCollection* shaderConstantList = new ShaderConstantCollection();
	shaderConstantList->AddConstant(materialConstant);
	shaderConstantList->AddConstant(lightConstant);
	shaderProgram->setShaderConstant(shaderConstantList);

	MaterialManager::Instance()->RegisterMaterial("ShinyWhite", shinyWhite);
}
vector<string> get_all_files_names_within_folder(string folder)
{
	vector<string> names;
	string search_path = folder + "/*.*";
	WIN32_FIND_DATA fd;
	HANDLE hFind = ::FindFirstFile(search_path.c_str(), &fd);
	if (hFind != INVALID_HANDLE_VALUE) {
		do {
			// read all (real) files in current folder
			// , delete '!' read other 2 default folder . and ..
			if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
				names.push_back(fd.cFileName);
			}
		} while (::FindNextFile(hFind, &fd));
		::FindClose(hFind);
	}
	return names;
}

void CreateTexturedMaterial()
{

	ITextureDataObject* texture = new BlankTexture2D(1024, 1024);
	ITextureDataObject* redTexture = new BlankTexture2D(1024, 1024, Color(1, 0, 0, 1), GL_RGB);
	redTexture->setTextureParams(&TexParam2DNoMipMap::Instance);



	int random_index = rand() % all_textures_name.size();
	string texture_name = texture_dir+all_textures_name[random_index];
	//std::cout << texture_name << std::endl;
	ITextureDataObject* imageTexture = new TextureDataImage(texture_name, GL_RGB);
	imageTexture->setTextureParams(&TexParam2DMipMap::Instance);
	SamplerApplicator* uniformBinding = new SamplerApplicator("texture");
	TextureBinding* binding = TextureBindManager::Instance()->CreateBinding(imageTexture, uniformBinding);
	binding->Enable();
	binding->Disable();
	VertexRoutine* vertexRoutine = new VertexRoutine("..\\Media\\Shaders\\ShadedTextured-vert.glsl");
	FragmentRoutine* fragmentRoutine = new FragmentRoutine("..\\Media\\Shaders\\Textured.frag");
	IShaderProgram* shaderProgram = new ShaderProgramWithMatrices(vertexRoutine, fragmentRoutine);
	SimpleShaderMaterial* texturedMaterial = new SimpleShaderMaterial(shaderProgram);
	texturedMaterial->setShaderConstant(uniformBinding);
	texturedMaterial->AddTexture(binding);

	ShadedMaterial* white = new ShadedMaterial(shaderProgram);
	
	/*
	//Random factor
		@ambient: 1.5~2.5
		@diffuse: 1.4~1.6
		@specular: 0.5~1.5
	*/
	float random_ambient = rand() % 100 / 100.0 + 1.5;
	float random_diffuse = rand() % 20 / 100.0+ 1.4;
	float random_specular = rand() % 100 / 100.0 + 0.5;



	white->setAmbientReflection(random_ambient*Colors::White);
	white->setDiffuseReflection(random_diffuse*Colors::White);
	white->setSpecularReflection(random_specular*Colors::White);
	white->setShininess(20.0f);

	ShaderConstantMaterial* materialConstant = new ShaderConstantMaterial("frontMaterial");
	materialConstant->setValue(white);
	ShaderConstantLights* lightConstant = new ShaderConstantLights();
	ShaderConstantCollection* shaderConstantList = new ShaderConstantCollection();
	shaderConstantList->AddConstant(materialConstant);
	shaderConstantList->AddConstant(lightConstant);
	shaderProgram->setShaderConstant(shaderConstantList);

	MaterialManager::Instance()->RegisterMaterial("Textured", texturedMaterial);
}
ISceneNode* CreateSceneGraph()
{
	// Create a simple scene
	// Perspective
	// LookAt camera
	// Drawable floor
	//
	DrawableFloor* floor = new DrawableFloor(10,10);
	ModelManager::Instance()->RegisterModel("2D Plane", floor);
	DrawableProxy* floorNode = new DrawableProxy("2D Plane", "2D Plane");
	/*															
	// Add a material
	SolidColorMaterialSolution* scarlet = new SolidColorMaterialSolution(Colors::White);
	MaterialManager::Instance()->RegisterMaterial("Scarlet", scarlet);
	*/
	CreateLights();
	//CreateGoldMaterial();
	//CreateWhiteMaterial();
	CreateTexturedMaterial();

	MaterialProxy* materialNode = new MaterialProxy("Plane Material(Light and Texture)", "Textured", floorNode);
	TransformMatrixNodeSolution* floorTransform = new TransformMatrixNodeSolution("Plane Transformation", materialNode);

	/*
	Random factor: Scale, Translate, Rotate
	@Scale random_scale
		@x: [2, 6]
		@y: 1
		@z: [8, 12]
	@Rotate random_rotate
		@x: [0, 0.314]
		@y: [0, 3.14]
		@z: [0, 0.314]
	@Translate random_translate
		@x: [-0.1, 0.1]
		@y: [-0.1, 0.1]
		@z: [-0.1, 0.1]
	*/
	Vector3 random_scale((rand() % 400/100.0+2.0), 1.0, (rand() % 400 / 100.0 + 8.0));
	Vector3 random_rotate((rand() % 314 / 1000.0), (rand() % 314 / 100.0), (rand() % 314 / 1000.0));
	Vector3 random_translate((rand() % 20 / 100.0 -0.1), (rand() % 20 / 100.0 - 0.1), (rand() % 20 / 100.0 - 0.1));
	// for debug setting
	//floorTransform->Scale(3.0, 1.0, 10.0);
	
	
	// Scale
	floorTransform->Scale(random_scale[0], random_scale[1], random_scale[2]);
	// Rotate
	floorTransform->Rotate(3.14, Vector3(1, 0, 0));
	floorTransform->Rotate(random_rotate[1], Vector3(0, 1, 0));
	floorTransform->Rotate(random_rotate[0], Vector3(0, 0, 1));
	floorTransform->Rotate(random_rotate[2], Vector3(-1, 0, 0));
	// Translate
	floorTransform->Translate(random_translate[0], random_translate[1], random_translate[2]);
	
	GroupNode* group = new GroupNode("Group Transformation");
	group->AddChild(floorTransform);
	
	examiner = new ExaminerCameraNode("Examiner", group);
	examiner->setWidth(windowWidth);
	examiner->setHeight(windowHeight);
	examiner->DollyRandom();
	examiner->PanRandom();
	return examiner;
}

void takeScreenshot(const char* screenshotFile)
{
	ILuint imageID = ilGenImage();
	ilBindImage(imageID);
	ilutGLScreen();
	ilEnable(IL_FILE_OVERWRITE);
	ilSaveImage(screenshotFile);
	ilDeleteImage(imageID);
	printf("Screenshot saved to: %s\n", screenshotFile);
}


void DisplayFrame()
{
	rootSceneNode->Accept(renderVisitor);
	/*
	for (int i = 0; i < 3000; i++) {
		// same eye position
		// create a new scene every time
		// if we just want to random the texture and light,
		// we will not need the line of the code
		ISceneNode* scene = CreateSceneGraph();
		rootSceneNode = CreateFrameBuffer(scene);
		rootSceneNode->Accept(renderVisitor);

		// screenshot
		//string output = "..//Output//picture//test//";
		string output = "..//Output//picture//0331_OpenGL_RGB//"+classes+"//0331_";
		string medium = std::to_string(number_screenshot);
		string last = ".png";
		output = output + medium + last;
		takeScreenshot(output.c_str());
		number_screenshot++;
		
		delete scene;
		delete rootSceneNode;
	}
	*/
	
	
}

void ReshapeWindow(int newWidth, int newHeight)
{
	windowWidth = newWidth;
	windowHeight = newHeight;
	examiner->setWidth(windowWidth);
	examiner->setHeight(windowHeight);
	glViewport(0, 0, windowWidth, windowHeight);
	glutPostRedisplay();
}

ISceneNode* CreateFrameBuffer(Crawfis::Graphics::ISceneNode * scene)
{
	IRenderTarget* screen = new RenderTarget();
	RenderManager::Instance()->RegisterRenderTarget("Screen", screen);
	//screen->setEnableCommand(new ClearFrameCommand(Colors::IndianRed));
	screen->setEnableCommand(new ClearFrameCommand(Colors::White));
	//screen->setEnableCommand(new ClearFrameCommand(Colors::Grey));
	screen->setDisableCommand(new SwapCommand(true));
	RenderTargetProxy* frameBuffer = new RenderTargetProxy("Screen Display", "Screen", scene);
	return frameBuffer;
}
void KeyboardController(unsigned char key, int x, int y)
{
	printf("Key Pressed: %c\n", key);
	std::vector<IKeyboardHandler*>::iterator handlerIterator;
	for (handlerIterator = keyboardHandlers.begin(); handlerIterator != keyboardHandlers.end(); handlerIterator++)
	{
		(*handlerIterator)->KeyPress(key, x, y);
	}
	glutPostRedisplay();
}

void NumPadController(int key, int x, int y)
{
	std::vector<IKeyboardHandler*>::iterator handlerIterator;
	for (handlerIterator = keyboardHandlers.begin(); handlerIterator != keyboardHandlers.end(); handlerIterator++)
	{
		(*handlerIterator)->NumPadPress(key, x, y);
	}
	glutPostRedisplay();
}

void MousePressController(int button, int state, int ix, int iy)
{
	std::vector<IMouseHandler*>::iterator handlerIterator;
	for (handlerIterator = mouseHandlers.begin(); handlerIterator != mouseHandlers.end(); handlerIterator++)
	{
		(*handlerIterator)->MouseEvent(button, state, ix, iy);
	}
	glutPostRedisplay();
}

void MouseMotionController(int ix, int iy)
{
	std::vector<IMouseHandler*>::iterator handlerIterator;
	for (handlerIterator = mouseHandlers.begin(); handlerIterator != mouseHandlers.end(); handlerIterator++)
	{
		(*handlerIterator)->MouseMoved(ix, iy);
	}
	glutPostRedisplay();
}

void IdleCallback()
{
}
void InitializeDevIL()
{
	::ilInit();
	::iluInit();
	::ilutInit();
	::ilOriginFunc(IL_ORIGIN_LOWER_LEFT);
	::ilEnable(IL_ORIGIN_SET);
}

int main(int argc, char **argv)
{
	all_textures_name = get_all_files_names_within_folder(texture_dir);
	srand(time(NULL));
	glutInit(&argc, argv);
	InitializeDevices();
	InitializeDevIL();
	TextureBindManagerOpenGL::Init();

	MatrixStack::Init();
	ISceneNode* scene = CreateSceneGraph();
	rootSceneNode = CreateFrameBuffer(scene);

	renderVisitor = new DebugRenderVisitor();
	PrintSceneVisitor* printScene = new PrintSceneVisitor();
	rootSceneNode->Accept(printScene);
	

	keyboardHandlers.push_back(examiner);
	mouseHandlers.push_back(examiner);

	glutDisplayFunc(DisplayFrame);
	glutReshapeFunc(ReshapeWindow);
	glutKeyboardFunc(KeyboardController);
	glutSpecialFunc(NumPadController);
	glutMouseFunc(MousePressController);
	glutMotionFunc(MouseMotionController);

	glutMainLoop();

	return 0;
}