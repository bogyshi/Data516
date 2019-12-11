#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <chrono>
#include <limits>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <device_functions.h>
#include <cuda_runtime.h>
#include <cuda_runtime_api.h>    // includes cuda.h and cuda_runtime_api.h
#include <algorithm>
#include <iterator>

#include <cuda.h>         // helper functions for CUDA error check

#ifdef _WIN32
#  define WINDOWS_LEAN_AND_MEAN
#  define NOMINMAX
#  include <windows.h>
#endif


#define SIZE 1024
#define SIZE2 89478484 

const int maximumSize = 1024 * 1024 * 1.5;
const int parameterSize = 48;
const int numCols = parameterSize;
//const int numRows = 10000;
const int numFiles = 168;
const int numRows = 1891422; // 1903771 - 12349

const int totalSize = 1024 * 1024 * 1;
const int totalCols = 256;
const int truSize = numRows;
const float LR = 10;
const int maxIters = 200;
const int checkPoint = maxIters/2;
const int maxAddress = numRows * numCols;

void readInData(float* data)
{
	std::ifstream rf("B:\\Github2\\Data512\\finalProject\\data\\inData2.bin", std::ios::in | std::ios::binary);
	rf.read((char*)&data[0], sizeof(float)*numRows*numCols);
	rf.close();
}

void readOutData(float * outputs)
{
	std::ifstream rf("B:\\Github2\\Data512\\finalProject\\data\\outData.bin", std::ios::in | std::ios::binary);
	rf.read((char*)&outputs[0], sizeof(int) * numRows);
	rf.close();
}

bool isNumber(const std::string& s) //https://stackoverflow.com/questions/29169153/how-do-i-verify-a-string-is-valid-double-even-if-it-has-a-point-in-it
{
	char* end = 0;
	double val = strtod(s.c_str(), &end);
	return end != s.c_str() && *end == '\0' && val != HUGE_VAL;
}

void setOutputs(float * output)
{
	std::fstream fin,badRows;
	std::string pathName = "B:\\Github2\\Data512\\finalProject\\data\\outputs.csv";
	badRows.open("B:\\Github2\\Data512\\finalProject\\data\\badRows.txt", std::fstream::in);
	fin.open(pathName, std::fstream::in);
	std::string v;
	std::vector<int> skipIndexes;
	while (badRows >> v)
	{
		skipIndexes.push_back(atoi(v.c_str()));
	}
	std::string result, line, temp, word;
	char* buffer = new char[3];
	int counter = 0;
	int colCounter = 0;
	bool skipCond;;

	while (fin >> temp)
	{
		std::stringstream s(temp);
		colCounter = 0;
		skipCond = std::find(std::begin(skipIndexes), std::end(skipIndexes), counter) == std::end(skipIndexes);
		while (std::getline(s, word, ','))
		{
			if (colCounter == 1 && skipCond)
			{
				output[counter] = atoi(word.c_str());
			}
			colCounter++;
		}
		counter++;
	}
}

void getDataDim()
{
	std::fstream fin;
	// Open an existing file 
	int counter = 1;
	int numRows = 0;
	std::string pathName = "B:\\Github2\\Data512\\finalProject\\data\\pivotData\\block";
	std::string result, line, temp, word;
	char* buffer = new char[3];
	result = pathName + "blockSpillsep.csv";
	fin.open(result, std::fstream::in);

	bool isgood = fin.good();
	bool begFile = false;
	int colCounter=0;
	int numBadRows = 0;
	std::vector<int> badRows;
	while (fin >> temp) {
		numRows++;
	}
	fin.close();

	while (counter < numFiles)
	{
		sprintf(buffer, "%d", counter);
		result = pathName + buffer + "sep.csv";
		fin.open(result, std::fstream::in);
		bool isgood = fin.good();
		begFile = true;
		while (fin >> temp) {
			std::stringstream s(temp);
			colCounter = 0;
			while (std::getline(s, word, ',')) {
				if (begFile)
				{
					break;
				}
				else if (colCounter>1 && (word.empty() || !isNumber(word))) //https://stackoverflow.com/questions/4654636/how-to-determine-if-a-string-is-a-number-with-c
				{
					badRows.push_back(numRows);
					numBadRows++;
					break;
				}
				colCounter++;
			}
			if (begFile == true)
			{
				begFile = false;
			}
			else
			{
				numRows++;
			}
		}
		fin.close();
		printf("%s\n", result.c_str());

		counter++;
	}
	std::ofstream fout("B:\\Github2\\Data512\\finalProject\\data\\badRows.txt");
	for (int x : badRows)
	{
		fout << x << "\n";
	}

	printf("Num total rows: %d\n", numRows);
	printf("Num bad rows: %d\n", badRows.size());
	printf("Num good rows: %d\n", numRows-numBadRows);


}
void read_record(std::vector<std::string> header, float * data)
{

	std::ifstream skipRows;
	skipRows.open("B:\\Github2\\Data512\\finalProject\\data\\badRows.txt", std::fstream::in);
	std::string v;
	std::vector<int> skipIndexes;
	while (skipRows>>v)
	{
		skipIndexes.push_back(atoi(v.c_str()));
	}

	// File pointer 
	std::fstream fin;

	// Open an existing file 
	int counter = 1;
	std::string pathName = "B:\\Github2\\Data512\\finalProject\\data\\pivotData\\block";
	std::string result,line,temp,word;
	char * buffer = new char[3];
	bool haveHeader = false;
	bool begOfFile = false;
	int i = 0;
	int whatRow=0;
	bool skipCond;
	int colCounter = 0;
	int address = 0;
	while (counter < numFiles)
	{
		sprintf(buffer, "%d", counter);
		result = pathName + buffer + "sep.csv";
		fin.open(result, std::fstream::in);
		begOfFile = true;
		while (fin >> temp) 
		{
			// used for breaking words 
			std::stringstream s(temp);
			// read every column data of a row and 
			// store it in a string variable, 'word'
			colCounter = 0;
			skipCond = std::find(std::begin(skipIndexes), std::end(skipIndexes), whatRow) == std::end(skipIndexes);
			if (skipCond)
			{
				while (std::getline(s, word, ',')) 
				{
					if (begOfFile == true)
					{
						if (haveHeader == false) {
							header.push_back(word);
						}
					}
					else if(colCounter>1)
					{
						address = i + (colCounter - 2) * numRows;
						data[address] = stof(word);
					}
					colCounter++;
				}
			}
			


			if (haveHeader == false)
			{
				haveHeader = true;
			}
			if (begOfFile == true)
			{
				begOfFile = false;
			}
			else
			{
				if(skipCond)                                                                          
					i++;
				whatRow++;
			}
		}
		fin.close();
		printf("%s\n",result.c_str());
		counter++;
	}
	//std::free(buffer);

	//roll2 = stoi(row[0]);

}

__global__ void vectorAdd2(int* a, int* b, int* c, int n)
{
	//int j = (blockIdx.y * blockDim.y) + threadIdx.y;
	int iw = threadIdx.x;
	int j = blockDim.x;
	int z = blockIdx.x;
	int iy = threadIdx.y;
	int jy = blockDim.y;
	int zy = blockIdx.y;
	int i = (blockIdx.x * blockDim.x) + threadIdx.x;

	if (i < n)
	{
		c[i] = (a[i] + b[i]) % 1024;
	}
}

//cudaMallocManaged(&b, truSize * sizeof(int));
//cudaMallocManaged(&c, truSize * sizeof(int));


__global__ void logRegression(float * outs, float * ins, float * theta,float * weightChanges)
{

	int i = (blockIdx.x * blockDim.x) + threadIdx.x;
	int j = 0;
	double total = 0.0;
	//int addr = (numRows * j) + i;
	if (i < (numRows))
	{
		for (j = 0; j < numCols; j++)
		{
			total += theta[j] * ins[j*numRows+i];
		}
		float l = outs[i] - (1.0 / (1 + exp(-1 * total)));
		for (j = 0; j < numCols; j++)
		{
			float toadd = ((ins[(numRows * j) + i]) * l) / numRows;
			atomicAdd(&weightChanges[j], toadd);
		}
	}

}

__global__ void vectorAdd(int* cols, int numCols, int n)
{
	//int j = (blockIdx.y * blockDim.y) + threadIdx.y;
	//int iw = threadIdx.x;
	//int j = blockDim.x;
	//int z = blockIdx.x;
	//int iy = threadIdx.y;
	//int jy = blockDim.y;
	//int zy = blockIdx.y;
	int i = (blockIdx.x * blockDim.x) + threadIdx.x;
	int j = 0;
	if (i < n)
	{
		for (j = 1; j < numCols; j++)
		{
			cols[i] += cols[j * truSize + i];
		}
	}
}

int main()
{

	
	float * data = new float[numRows*numCols]; 
	float* output = new float[numRows];
	float * parameters = new float[numCols];
	float* toAdjust = new float[numCols];
	int i = 0;
	int j = 0;
	float insertVal = 0.0;
	float tochange = 0.0;
	int numIters = 0;
	float totalMilliseconds = 0;
	float milliseconds = 0;
	bool debug = false;
	int NT;
	int numThreadsArr[9] = {1024,512,256, 128, 64, 32,16,8,4};
	int toAvgPrf[9] = { 0,0,0,0,0,0,0,0,0};
	bool printRes = false;
	int roundCounter = 0;
	int whichAmt = 0;
	int numRounds = 20;
	cudaError_t somtin;
	std::vector<std::string> header;


	//getDataDim(); // only need to do this once 1903771 - 12349;

	//34847,34961
	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);

	cudaMallocManaged(&parameters, sizeof(float) * numCols);
	cudaMallocManaged(&toAdjust, sizeof(double) * numCols);
	cudaMallocManaged(&output, sizeof(float) * numRows);
	cudaMallocManaged(&data, sizeof(float)*numRows*numCols);
	/*
	// we are missing some data at the end, but we will forget about it for now
	read_record(header, data);
	std::ofstream mydata2("B:\\Github2\\Data512\\finalProject\\data\\inData2.bin", std::ios::out | std::ios::binary);
	for (i = 0; i < 10; i++)
	{
		printf("last 10 vals of data from file: pos %d = %f", 10 - i, data[(numRows * numCols - 1) - i]);
	}
	mydata2.write((char*)&data[0], sizeof(float) * numRows * numCols);
	mydata2.close();
	*/
	readInData(data);
	for (i = 0; i < 10; i++)
	{
		printf("last 10 vals of data after write: pos %d = %f", 10 - i, data[(numRows * numCols - 1) - i]);
	}
	/*
	setOutputs(output);
	std::ofstream myOutdata2("B:\\Github2\\Data512\\finalProject\\data\\outData.bin", std::ios::out | std::ios::binary);
	myOutdata2.write((char*)&output[0], sizeof(int) * numRows);
	myOutdata2.close();
	*/
	readOutData(output);
	while (roundCounter < numRounds)
	{
		whichAmt = 0;
		for (int numThreadsFA : numThreadsArr)
		{
			NT = numThreadsFA;
			dim3 numThreads(NT);
			dim3 gridDim((numRows * numCols / NT) + 1, 1);

			// to view array contents, do "arrayName,numView" e.g. data,1
			for (i = 0; i < numCols; i++)
			{
				parameters[i] = -0.01;
				toAdjust[i] = 0.0;
			}

			numIters = 0;
			totalMilliseconds = 0;
			while (numIters < maxIters)
			{
				cudaEventRecord(start);
				logRegression << <gridDim, numThreads >> > (output, data, parameters, toAdjust);
				cudaEventRecord(stop);

				somtin = cudaEventSynchronize(stop);
				cudaEventElapsedTime(&milliseconds, start, stop);
				totalMilliseconds += milliseconds;
				for (i = 0; i < numCols; i++)
				{
					tochange = LR * toAdjust[i] / numRows;
					parameters[i] -= tochange;
					toAdjust[i] = 0;
					if ((numIters % checkPoint == 0) && printRes)
					{
						printf("At iteration %d, parameters[% d] = % f\n", numIters, i, parameters[i]);
					}
				}
				numIters++;
			}
			if (printRes)
			{
				for (i = 0; i < numCols; i++)
				{
					printf("At iteration %d, parameters[% d] = % f\n", numIters, i, parameters[i]);
				}
			}
			printf("Time to do %d calculations with %d threads is: %f(ms)\n", maxIters, NT, totalMilliseconds);

			toAvgPrf[whichAmt] += totalMilliseconds;
			whichAmt++;
		}
		roundCounter++;
	}
	for (int tc = 0; tc < 9; tc++)
	{
		printf("Avg time to do %d calculations with %d threads over %d rounds is %f (ms)\n", maxIters, numThreadsArr[tc],numRounds, toAvgPrf[tc]/numRounds);
	}
			/*
	


	//cudaDeviceSynchronize(stop);
	//auto stop = high_resolution_clock::now();
	//auto duration = duration_cast<microseconds>(stop - start);


	for (i = 0; i < 13; i++)
	{
		printf("c[% d] = % d\n", i, allCols[i]);
	}

	for (i = truSize - 10; i < truSize; i++)
	{
		printf("c[% d] = % d\n", i, allCols[i]);
	}
	cudaFree(allCols);

	int nDevices;

	cudaGetDeviceCount(&nDevices);
	for (int i = 0; i < nDevices; i++) {
		cudaDeviceProp prop;
		cudaGetDeviceProperties(&prop, i);
		printf("Device Number: %d\n", i);
		printf("  Device name: %s\n", prop.name);
		printf("  Memory Clock Rate (KHz): %d\n",
			prop.memoryClockRate);
		printf("  Memory Bus Width (bits): %d\n",
			prop.memoryBusWidth);
		printf("  Peak Memory Bandwidth (GB/s): %f\n\n",
			2.0 * prop.memoryClockRate * (prop.memoryBusWidth / 8) / 1.0e6);
	}
	*/
	/*
	1024 threads
	base = 0.65ms
	10x = 6.5ms
	20x = 13ms
	30x= 19.5

	512 threads
	base = 0.62ms
	10x = 6.02ms
	20x = 12.05ms
	30x = 18.22ms

	1 threads
	base = 18ms
	10x = 183ms
	20x = 354ms
	30x = 523ms

	2 threads

	base = 9ms
	30x = 263ms

	1024 threads, multiplication, 256 columns, 56.5ms
					addition (+), ... , 42.8
					addition (+=) 36.9
	*/


	return 0;
}


/*


const int maximumSize = 1024 * 1024 * 1.5;
const int parameterSize = 2;
const int numCols = parameterSize;
const int numRows = 10000;
const int numFiles = 168;

const int totalSize = 1024 * 1024 * 1;
const int NT = SIZE;
const int totalCols = 256;
const int truSize = numRows;
const float LR = 0.1;
const int maxIters = 2000;
const int checkPoint = 1000;

void read_record()
{

	// File pointer 
	std::fstream fin;

	// Open an existing file 
	int counter = 1;
	std::string pathName = "B:\\Github2\\Data512\\finalProject\\data\\pivotData\\block";
	std::string result, line, temp, word;
	std::vector<std::string> row;
	char* buffer = new char[3];
	while (counter < numFiles)
	{
		sprintf(buffer, "%d", counter);
		result = pathName + buffer + "sep.csv";
		fin.open(result, std::fstream::in);
		bool isgood = fin.good();
		while (fin >> temp) {

			row.clear();

			// used for breaking words 
			std::stringstream s(temp);

			// read every column data of a row and 
			// store it in a string variable, 'word' 
			while (std::getline(s, word, ',')) {
				printf("%s\n", word.c_str());
			}
		}
		fin.close();
		printf("%s\n", result.c_str());
		counter++;
	}
	std::free(buffer);

	//roll2 = stoi(row[0]);

}

__global__ void vectorAdd2(int* a, int* b, int* c, int n)
{
	//int j = (blockIdx.y * blockDim.y) + threadIdx.y;
	int iw = threadIdx.x;
	int j = blockDim.x;
	int z = blockIdx.x;
	int iy = threadIdx.y;
	int jy = blockDim.y;
	int zy = blockIdx.y;
	int i = (blockIdx.x * blockDim.x) + threadIdx.x;

	if (i < n)
	{
		c[i] = (a[i] + b[i]) % 1024;
	}
}

//cudaMallocManaged(&b, truSize * sizeof(int));
//cudaMallocManaged(&c, truSize * sizeof(int));


__global__ void logRegression(float* outs, float* ins, float* theta, float* weightChanges)
{

	int i = (blockIdx.x * blockDim.x) + threadIdx.x;
	int j = 0;
	double total = 0.0;
	for (j = 0; j < numCols; j++)
	{
		total += theta[j] * ins[(numRows * j) + i];
	}
	float l = outs[i] - (1.0 / (1 + exp(-1 * total)));
	for (j = 0; j < numCols; j++)
	{
		float toadd = ((ins[(numRows * j) + i]) * l) / numRows;
		atomicAdd(&weightChanges[j], toadd);
	}

}

__global__ void vectorAdd(int* cols, int numCols, int n)
{
	//int j = (blockIdx.y * blockDim.y) + threadIdx.y;
	//int iw = threadIdx.x;
	//int j = blockDim.x;
	//int z = blockIdx.x;
	//int iy = threadIdx.y;
	//int jy = blockDim.y;
	//int zy = blockIdx.y;
	int i = (blockIdx.x * blockDim.x) + threadIdx.x;
	int j = 0;
	if (i < n)
	{
		for (j = 1; j < numCols; j++)
		{
			cols[i] += cols[j * truSize + i];
		}
	}
}

int main()
{

	//read_record();

	float* data = new float[numRows * numCols];
	float* output = new float[numRows];
	float* parameters = new float[numCols];
	float* toAdjust = new float[numCols];
	int i = 0;
	int j = 0;
	float insertVal = 0.0;
	float tochange = 0.0;
	int numIters = 0;

	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);

	cudaMallocManaged(&parameters, sizeof(float) * numCols);
	cudaMallocManaged(&toAdjust, sizeof(double) * numCols);
	cudaMallocManaged(&output, sizeof(float) * numRows);
	cudaMallocManaged(&data, sizeof(float) * numRows * numCols);

	dim3 numThreads(NT);
	dim3 gridDim((numRows * numCols / NT) + 1, 1);

	// to view array contents, do "arrayName,numView" e.g. data,10
	for (i = 0; i < numCols; i++)
	{
		if (i % 2 == 0)
		{
			insertVal = -0.2;
		}
		else
		{
			insertVal = 0.2;
		}
		for (j = 0; j < numRows; j++)
		{
			data[numRows * i + j] = insertVal;
		}
	}

	for (i = 0; i < numRows; i++)
	{
		output[i] = 1.0;
	}

	for (i = 0; i < numCols; i++)
	{
		parameters[i] = -0.01;
		toAdjust[i] = 0.0;
	}

	cudaEventRecord(start);
	while (numIters < maxIters)
	{
		logRegression << <gridDim, numThreads >> > (output, data, parameters, toAdjust);


		for (i = 0; i < numCols; i++)
		{
			tochange = LR * toAdjust[i] / numRows;
			parameters[i] -= tochange;
			toAdjust[i] = 0;
			if (numIters % checkPoint == 0)
			{
				printf("parameters[% d] = % f\n", i, parameters[i]);
			}

		}
		numIters++;
	}
	cudaEventRecord(stop);
	cudaEventSynchronize(stop);
	float milliseconds = 0;
	cudaEventElapsedTime(&milliseconds, start, stop);
	printf("Time to %d iterations is: %f(ms)\n", maxIters, milliseconds);
	cudaFree(parameters);
	cudaFree(toAdjust);
	cudaFree(output);
	cudaFree(data);


	/*



//cudaDeviceSynchronize(stop);
//auto stop = high_resolution_clock::now();
//auto duration = duration_cast<microseconds>(stop - start);


for (i = 0; i < 13; i++)
{
	printf("c[% d] = % d\n", i, allCols[i]);
}

for (i = truSize - 10; i < truSize; i++)
{
	printf("c[% d] = % d\n", i, allCols[i]);
}
cudaFree(allCols);

int nDevices;

cudaGetDeviceCount(&nDevices);
for (int i = 0; i < nDevices; i++) {
	cudaDeviceProp prop;
	cudaGetDeviceProperties(&prop, i);
	printf("Device Number: %d\n", i);
	printf("  Device name: %s\n", prop.name);
	printf("  Memory Clock Rate (KHz): %d\n",
		prop.memoryClockRate);
	printf("  Memory Bus Width (bits): %d\n",
		prop.memoryBusWidth);
	printf("  Peak Memory Bandwidth (GB/s): %f\n\n",
		2.0 * prop.memoryClockRate * (prop.memoryBusWidth / 8) / 1.0e6);
}
*/
/*
1024 threads
base = 0.65ms
10x = 6.5ms
20x = 13ms
30x= 19.5

512 threads
base = 0.62ms
10x = 6.02ms
20x = 12.05ms
30x = 18.22ms

1 threads
base = 18ms
10x = 183ms
20x = 354ms
30x = 523ms

2 threads

base = 9ms
30x = 263ms

1024 threads, multiplication, 256 columns, 56.5ms
				addition (+), ... , 42.8
				addition (+=) 36.9



	return 0;
}
*/