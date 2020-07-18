#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <CL/cl.hpp>
#include <math.h>


std::vector<int> read_file(std::string filename)
{
    std::ifstream file;
    file.open(filename);
    std::string line;

    std::getline(file, line);

    int count = 0;

    for(int i = 0; line[i]; ++i)
    {
        if(!isspace(line[i]))
            count++;   
    }

    file.close();
    file.open(filename);

    int matrix[count*count];

    for(int i = 0; i < count*count; i++)
    {
        file >> matrix[i];
    }


    file.close();

    std::vector<int> final_matrix;

    for(int elem : matrix)
        final_matrix.push_back(elem);

    return final_matrix;
}

int main()
{

    std::vector<int> matrix1 = read_file("matrice1");
    std::vector<int> matrix2 = read_file("matrice2");

    // Obtention des plateformes.
    std::vector<cl::Platform> available_platforms;
	cl::Platform::get(&available_platforms);
	if (available_platforms.size() == 0) {
		std::cout << "No platforms found. Check OpenCL installation!" << std::endl;
		exit(1);
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

	// Note: «get_global_id» est une fonction prédéfinie pour les items de travail («Work-Item Functions»).
	// https://www.khronos.org/registry/OpenCL/specs/opencl-1.1.pdf
	// https://www.khronos.org/registry/OpenCL/specs/opencl-1.2.pdf
	// https://www.khronos.org/registry/OpenCL/specs/opencl-2.0.pdf
	std::string kernel_code =
			"	void multiply(int n, __global float *A, __global float *B, __global float *C) {						"
			"   	int gid1 = get_global_id(0);																	"
			"   	int gid2 = get_global_id(1);																	"
			"		float value = 0;																				"
            "   	for(int k = 0; k < n; ++k)																		"
			"		{																								"
			"			float elementA = A[gid2 * n + k];															"
			"			float elementB = B[k * n + gid1];															"	
			"			value += elementA * elementB;																"
			"		}																								"	
			"		C[gid2 * n + gid1] = value;																		"
			"	}																									";


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

	int size = matrix1.size();

	// Création des tampons GPU.
	cl::Buffer buffer_A(context, CL_MEM_READ_WRITE, sizeof(int) * size);
	cl::Buffer buffer_B(context, CL_MEM_READ_WRITE, sizeof(int) * size);
	cl::Buffer buffer_C(context, CL_MEM_READ_WRITE, sizeof(int) * size);


	// Création de la queue de traitement GPU dans laquelle nous allons planifier des commandes.
	cl::CommandQueue queue(context, default_device);

	// Planification de l'initialisation des tableaux A et B (transfère du CPU vers le GPU).
	int* A = &matrix1[0];
	int* B = &matrix2[0];

	queue.enqueueWriteBuffer(buffer_A, CL_TRUE, 0, sizeof(int) * size, A);
	queue.enqueueWriteBuffer(buffer_B, CL_TRUE, 0, sizeof(int) * size, B);


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
	kernel_add.setArg(0, sqrt(size));
	kernel_add.setArg(1, buffer_A);
	kernel_add.setArg(2, buffer_B);
	kernel_add.setArg(3, buffer_C);

	// Paramètres de «enqueueNDRangeKernel» :
	//  - const Kernel &kernel  : Noyau à exécuter
	//  - const NDRange &offset : Décalages des indices globaux (cl::NullRange == aucun).
	//  - const NDRange &global : Dimension des items de travail (ex: «X», «X * Y», «X * Y * Z», etc.).
	//  - const NDRange &local  : Dimension des groupes de travail locaux (nombre de work-items par work-group).
	std::cout << "Je cause le seg fault, you mad?" << std::endl;
	queue.enqueueNDRangeKernel(kernel_add, cl::NullRange, cl::NDRange(size, size), cl::NullRange);

	// Exemple d'une exécution en 2D.
	//queue.enqueueNDRangeKernel(kernel_add, cl::NullRange, cl::NDRange(800, 600), cl::NullRange);
	queue.finish();
	//     }

	// Déclaration du tampon d'extraction des données (CPU).
	int C[size];

	// Planification de l'écriture des résultat de `buffer_C` vers `C` (transfère du GPU vers le CPU).
	queue.enqueueReadBuffer(buffer_C, CL_TRUE, 0, sizeof(int) * size, C);

	// Affichage des résultats à la console.
	std::cout << " result:" << std::endl;
	for(int i = 0; i < size; i++) {
		std::cout << C[i] << " ";
	}


    return 0;
}
