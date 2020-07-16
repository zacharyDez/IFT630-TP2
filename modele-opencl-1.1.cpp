/*
 * Source originale : https://github.com/Dakkers/OpenCL-examples/blob/master/example00/main.cpp
 * Modifié par : Daniel-Junior Dubé
*/

#include <iostream>
#include <CL/cl.hpp>

int main() {

	// Obtention des plateformes.
	std::vector<cl::Platform> available_platforms;
	cl::Platform::get(&available_platforms);
	if (available_platforms.size() == 0) {
		std::cout << "No platforms found. Check OpenCL installation!" << std::endl;
		exit(1);
	}

	// Affichage des informations OpenCL (plateformes, versions et périphériques).
	for (auto &platform : available_platforms) {
		std::string platform_name = platform.getInfo<CL_PLATFORM_NAME>();
		std::string version = platform.getInfo<CL_PLATFORM_VERSION>();
		std::cout << "Found platform '" << platform_name << "' with version : '" << version << "'" << std::endl;

		std::vector<cl::Device> available_devices;
		platform.getDevices(CL_DEVICE_TYPE_ALL, &available_devices);
		for (auto &device : available_devices) {
			std::cout << "	With device: " << device.getInfo<CL_DEVICE_NAME>() << std::endl;
		}
	}

	// Obtention de la platforme d'exécution du programme (premier disponible).
	cl::Platform default_platform = available_platforms[0];
	std::cout << "Using platform: " << default_platform.getInfo<CL_PLATFORM_NAME>() << std::endl;

	// Sélection du périphérique de calcul (premier disponible).
	std::vector<cl::Device> available_devices;
	default_platform.getDevices(CL_DEVICE_TYPE_ALL, &available_devices);
	cl::Device default_device = available_devices[0];
	std::cout << "Using device: " << default_device.getInfo<CL_DEVICE_NAME>() << std::endl;

	// Déclaration du contexte de calcul.
	cl::Context context({
		default_device
	});

	// Code source du programme GPU.
	cl::Program::Sources sources;

	// Chaîne de caractères contenant le programme pour appliquer `C = A + B` sur chaque élément de tableaux.
	// Note: «get_global_id» est une fonction prédéfinie pour les items de travail («Work-Item Functions»).
	// https://www.khronos.org/registry/OpenCL/specs/opencl-1.1.pdf
	// https://www.khronos.org/registry/OpenCL/specs/opencl-1.2.pdf
	// https://www.khronos.org/registry/OpenCL/specs/opencl-2.0.pdf
	std::string kernel_code =
			"   void kernel demo(global const int* A, global const int* B, global int* C) {             "
			"       C[get_global_id(0)] = A[get_global_id(0)] + B[get_global_id(0)];                    "
			"   }                                                                                       ";

	// Sauvegarde de la source.
	sources.push_back({
		kernel_code.c_str(),
		kernel_code.length()
	});

	// Déclaration du programme GPU en l'associant à un contexte de calcul.
	cl::Program program(context, sources);

	// Compilation du programme GPU.
	if (program.build({default_device}) != CL_SUCCESS) {
		std::cout << " Error building: " << program.getBuildInfo<CL_PROGRAM_BUILD_LOG>(default_device) << std::endl;
		exit(1);
	}

	// Création des tampons GPU.
	cl::Buffer buffer_A(context, CL_MEM_READ_WRITE, sizeof(int) * 10);
	cl::Buffer buffer_B(context, CL_MEM_READ_WRITE, sizeof(int) * 10);
	cl::Buffer buffer_C(context, CL_MEM_READ_WRITE, sizeof(int) * 10);

	int A[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
	int B[] = { 0, 1, 2, 0, 1, 2, 0, 1, 2, 0 };

	// Création de la queue de traitement GPU dans laquelle nous allons planifier des commandes.
	cl::CommandQueue queue(context, default_device);

	// Planification de l'initialisation des tableaux A et B (transfère du CPU vers le GPU).
	queue.enqueueWriteBuffer(buffer_A, CL_TRUE, 0, sizeof(int) * 10, A);
	queue.enqueueWriteBuffer(buffer_B, CL_TRUE, 0, sizeof(int) * 10, B);


	// --------------------------------------------------------------------------------
	// Exécution du noyau nommé «demo».
	// --------------------------------------------------------------------------------

	//     Première avec foncteurs-noyaux (non disponible en OpenCL 1.2 mais l'est en 1.1 et 2.x).
	//     {
	//cl::KernelFunctor demo(cl::Kernel(program, "demo"), queue, cl::NullRange, cl::NDRange(10), cl::NullRange);
	//demo(buffer_A, buffer_B, buffer_C);
	//     }

	//     Version générique.
	//     {
	cl::Kernel kernel_add = cl::Kernel(program, "demo");

	// Assignation des paramètres du noyau.
	kernel_add.setArg(0, buffer_A);
	kernel_add.setArg(1, buffer_B);
	kernel_add.setArg(2, buffer_C);

	// Paramètres de «enqueueNDRangeKernel» :
	//  - const Kernel &kernel  : Noyau à exécuter
	//  - const NDRange &offset : Décalages des indices globaux (cl::NullRange == aucun).
	//  - const NDRange &global : Dimension des items de travail (ex: «X», «X * Y», «X * Y * Z», etc.).
	//  - const NDRange &local  : Dimension des groupes de travail locaux (nombre de work-items par work-group).
	queue.enqueueNDRangeKernel(kernel_add, cl::NullRange, cl::NDRange(10), cl::NullRange);

	// Exemple d'une exécution en 2D.
	//queue.enqueueNDRangeKernel(kernel_add, cl::NullRange, cl::NDRange(800, 600), cl::NullRange);
	queue.finish();
	//     }

	// Déclaration du tampon d'extraction des données (CPU).
	int C[10];

	// Planification de l'écriture des résultat de `buffer_C` vers `C` (transfère du GPU vers le CPU).
	queue.enqueueReadBuffer(buffer_C, CL_TRUE, 0, sizeof(int) * 10, C);

	// Affichage des résultats à la console.
	std::cout << " result:" << std::endl;
	for(int i = 0; i < 10; i++) {
		std::cout << C[i] << " ";
	}

	// Fin.
	return 0;
}